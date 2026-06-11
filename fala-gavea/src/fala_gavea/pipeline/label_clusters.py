"""Generate cluster labels via Ollama LLM from representative posts."""
from __future__ import annotations

import os

import httpx
import numpy as np
import pandas as pd

OLLAMA_URL = os.environ.get("FALA_GAVEA_OLLAMA_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.environ.get("FALA_GAVEA_OLLAMA_MODEL", "qwen3:8b")

_LABEL_PROMPT = """\
Você recebeu os seguintes relatos de cidadãos do mesmo grupo temático.
Gere um label curto (2 a 4 palavras) em português que capture o tema principal desses relatos.
Responda APENAS com o label, sem explicação, sem pontuação extra.

Relatos:
{posts}

Label:"""


def _pick_representatives(group_df: pd.DataFrame, n: int = 5) -> list[str]:
    """Return n texts closest to the cluster centroid in UMAP space."""
    coords = group_df[["x", "y"]].values
    centroid = coords.mean(axis=0)
    dists = np.linalg.norm(coords - centroid, axis=1)
    idx = np.argsort(dists)[:n]
    return group_df.iloc[idx]["text"].tolist()


def label_clusters(df: pd.DataFrame) -> dict[int, str]:
    """Call Ollama once per cluster to generate a short label.

    Returns {cluster_id: label_str}. Noise cluster (-1) gets "Não classificado".
    """
    labels: dict[int, str] = {-1: "Não classificado"}
    cluster_ids = [c for c in df["cluster_id"].unique() if c != -1]

    for cid in sorted(cluster_ids):
        group = df[df["cluster_id"] == cid]
        samples = _pick_representatives(group)
        prompt = _LABEL_PROMPT.format(posts="\n".join(f"- {t}" for t in samples))
        try:
            resp = httpx.post(
                f"{OLLAMA_URL}/chat/completions",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
                timeout=30,
            )
            resp.raise_for_status()
            label = resp.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            label = f"Cluster {cid}"
        labels[cid] = label

    return labels
