from __future__ import annotations
import numpy as np
import pandas as pd
from gavealab_poc.embeddings import embed


def build_umap_df(
    claims_tree: dict,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
) -> pd.DataFrame:
    """Project claim embeddings to 2D via UMAP.

    Returns a DataFrame with columns:
        x, y          -- UMAP coordinates
        claim         -- claim text
        topic         -- topic name
        subtopic      -- subtopic name
        territory     -- territory group (or 'desconhecido')
    """
    import umap

    rows: list[dict] = []
    for topic, subtopics in claims_tree.items():
        for subtopic, claims in subtopics.items():
            for c in claims:
                rows.append({
                    "claim": c.get("claim", ""),
                    "topic": topic,
                    "subtopic": subtopic,
                    "territory": c.get("territory") or "desconhecido",
                })

    if not rows:
        return pd.DataFrame(columns=["x", "y", "claim", "topic", "subtopic", "territory"])

    texts = [r["claim"] for r in rows]
    embeddings = embed(texts)  # shape (N, 1024), L2-normalised

    reducer = umap.UMAP(
        n_neighbors=min(n_neighbors, len(rows) - 1),
        min_dist=min_dist,
        metric="cosine",
        random_state=42,
    )
    coords = reducer.fit_transform(embeddings)  # (N, 2)

    df = pd.DataFrame(rows)
    df["x"] = coords[:, 0]
    df["y"] = coords[:, 1]
    return df
