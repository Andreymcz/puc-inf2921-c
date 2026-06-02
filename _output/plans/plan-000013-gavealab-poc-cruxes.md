# Plan 000013 | FEATURE-X | 2026-06-01 22:44 | GaveaLab PoC -- Divergent opinion (cruxes) detection | Review: light
# DONE | 2026-06-02 01:00 UTC |
plan_format_version: 1
source: research-000014

## Revision note
Revised 2026-06-01 23:28 UTC (research-000014): replaced pure-LLM crux detection with
embedding-based approach (multilingual-e5-large + cosine distance). LLM (Ollama) called only
for narrow one-sentence crux label per divergent subtopic pair — reduces LLM calls significantly.
Adds `sentence-transformers` and `numpy` to pyproject.toml.

Revised 2026-06-01 23:10 UTC: render() receives workspace; result persisted via
session.save_result("cruxes", ...); speaker replaced by territory as grouping signal
(sample CSV has territory asfalto/favela instead of speaker names).

## Brief (verbatim)
Implement divergent opinion detection: for each subtopic that has claims from 2+ territory groups,
ask the LLM to synthesize a "crux claim" that best splits participants into agree/disagree groups.
(Wave 2, parallel with plan-000012. Depends on plan-000011.)

## Context note on grouping
The sample CSV (`tttc-poc/data/sample-gavealab.csv`) has `territory` (asfalto/favela)
instead of named speakers. The crux analysis groups by territory when no other identifier
is available, falling back to commentId if territory is absent.

## Approach (v2 — embedding-based, research-000014)

Instead of sending all claims to the LLM and asking it to find cruxes (open-ended, expensive),
we use a three-step pipeline:

1. **Embed** each claim with `sentence-transformers` (`intfloat/multilingual-e5-large`).
2. **Divergence detection**: per subtopic, compute the centroid embedding for each territory
   group; if the cosine distance between centroids exceeds a threshold (0.25), the subtopic
   is flagged as divergent.
3. **Label generation**: only for divergent subtopics, ask Ollama to generate a single
   one-sentence crux label — a narrow, well-specified task that 14B models handle reliably.

This reduces LLM calls to O(divergent_subtopics) instead of O(all_subtopics_with_2+_groups),
and makes divergence detection principled rather than prompt-dependent.

**Embedding model**: `intfloat/multilingual-e5-large` (560MB, excellent pt-BR quality).
Model is downloaded on first run and cached by HuggingFace. Use `"passage: "` prefix for
claims and `"query: "` prefix for queries (E5 convention).

## Files
- `gavealab-poc/pyproject.toml` (update — add sentence-transformers, numpy)
- `gavealab-poc/gavealab_poc/embeddings.py` (create — singleton embedding model)
- `gavealab-poc/gavealab_poc/pipeline/cruxes.py` (create — embedding-based crux detection)
- `gavealab-poc/gavealab_poc/pages/cruxes.py` (replace stub)

## Steps

### Step 1 — pyproject.toml: add dependencies

Add to `[project] dependencies`:
```
"sentence-transformers>=3.0",
"numpy>=1.26",
```

### Step 2 — gavealab_poc/embeddings.py (singleton, cached)

```python
from __future__ import annotations
from functools import lru_cache
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "intfloat/multilingual-e5-large"

@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(EMBED_MODEL)

def embed(texts: list[str], prefix: str = "passage: ") -> "np.ndarray":
    import numpy as np
    model = get_model()
    prefixed = [prefix + t for t in texts]
    return np.array(model.encode(prefixed, normalize_embeddings=True))
```

### Step 3 — gavealab_poc/pipeline/cruxes.py

```python
from __future__ import annotations
import json
import numpy as np
from gavealab_poc.embeddings import embed
from gavealab_poc.llm import chat
from gavealab_poc.workspace import AnalysisSession
from gavealab_poc.pipeline.topics import _extract_json

# Cosine distance threshold above which a subtopic is considered divergent.
# (distance = 1 - cosine_similarity; 0.25 ~= moderate divergence)
DIVERGENCE_THRESHOLD = 0.25

SYSTEM_PROMPT = (
    "You are a JSON generator. You MUST respond with ONLY valid JSON. "
    "No text before or after the JSON."
)

LABEL_PROMPT_TMPL = (
    "Two groups of citizens disagree about the topic '{topic} / {subtopic}'.\n\n"
    "Group A ({group_a}) says:\n{claims_a}\n\n"
    "Group B ({group_b}) says:\n{claims_b}\n\n"
    "Write ONE sentence that captures the core point of disagreement between these groups. "
    "Be specific and controversial — this is the crux.\n\n"
    'Return ONLY valid JSON: {{"cruxClaim": "string", "explanation": "string"}}'
)


def detect_cruxes(session: AnalysisSession) -> list[dict]:
    """Detect crux claims using embedding-based divergence detection.

    Algorithm:
    1. Embed all claims with multilingual-e5-large.
    2. Per subtopic: compute centroid per territory group.
    3. If cosine distance between centroids > DIVERGENCE_THRESHOLD, flag as divergent.
    4. For divergent subtopics only, ask Ollama for a one-sentence crux label.

    Persists result via session.save_result and returns the list.
    Each crux dict: {topic, subtopic, cruxClaim, explanation, agree, disagree, cosine_distance}
    """
    if not session.claims_tree:
        raise ValueError("Extraia os claims primeiro ('Extrair claims').")

    cruxes: list[dict] = []

    for topic, subtopics in session.claims_tree.items():
        for subtopic, claims in subtopics.items():
            groups = _build_groups(claims)
            if len(groups) < 2:
                continue

            group_names = list(groups.keys())
            # Only handle binary divergence (two groups) for simplicity
            g_a, g_b = group_names[0], group_names[1]
            claims_a = [c["claim"] for c in groups[g_a]]
            claims_b = [c["claim"] for c in groups[g_b]]

            dist = _group_cosine_distance(claims_a, claims_b)
            if dist < DIVERGENCE_THRESHOLD:
                continue  # groups are semantically similar — no crux

            crux = _label_crux(topic, subtopic, g_a, claims_a, g_b, claims_b)
            if crux:
                crux.update({
                    "topic": topic,
                    "subtopic": subtopic,
                    "agree": [g_a],
                    "disagree": [g_b],
                    "cosine_distance": round(dist, 3),
                })
                cruxes.append(crux)

    session.save_result("cruxes", cruxes)
    return cruxes


def _build_groups(claims: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for c in claims:
        key = c.get("territory") or c.get("commentId", "?")
        groups.setdefault(key, []).append(c)
    return groups


def _group_cosine_distance(claims_a: list[str], claims_b: list[str]) -> float:
    """Cosine distance (1 - similarity) between the centroids of two claim sets."""
    emb_a = embed(claims_a).mean(axis=0)
    emb_b = embed(claims_b).mean(axis=0)
    # Embeddings are already L2-normalised; dot product == cosine similarity
    similarity = float(np.dot(emb_a, emb_b))
    return 1.0 - similarity


def _label_crux(
    topic: str, subtopic: str,
    g_a: str, claims_a: list[str],
    g_b: str, claims_b: list[str],
) -> dict | None:
    """Ask Ollama to produce a one-sentence crux label for the divergent pair."""
    prompt = LABEL_PROMPT_TMPL.format(
        topic=topic, subtopic=subtopic,
        group_a=g_a, claims_a="\n".join(f"- {c}" for c in claims_a),
        group_b=g_b, claims_b="\n".join(f"- {c}" for c in claims_b),
    )
    for _ in range(3):  # up to 3 retries for JSON parse failures
        raw = chat(messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ])
        try:
            obj = _extract_json(raw)
            if isinstance(obj, dict) and "cruxClaim" in obj:
                return obj
        except Exception:
            pass
    return None
```

### Step 4 — gavealab_poc/pages/cruxes.py

```python
from __future__ import annotations
import streamlit as st
from gavealab_poc.workspace import GaveaLabWorkspace


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("4. Opinioes divergentes")
    session = st.session_state.get("session")
    if session is None:
        st.warning("Crie ou carregue uma sessao na pagina 'Upload CSV'.")
        return
    if not session.claims_tree:
        st.warning("Extraia os claims primeiro (pagina 'Temas automaticos').")
        return

    st.caption(
        "Detecta subtopicos onde grupos divergem semanticamente (multilingual-e5-large + Ollama). "
        "O modelo de embedding (~560MB) e baixado na primeira execucao."
    )

    if st.button("Detectar divergencias"):
        with st.spinner("Calculando embeddings e identificando divergencias..."):
            try:
                from gavealab_poc.pipeline.cruxes import detect_cruxes
                detect_cruxes(session)
                st.session_state.session = session
            except Exception as exc:
                st.error(f"Erro: {exc}")
                return

    if not session.cruxes:
        st.info("Clique no botao para detectar opinioes divergentes.")
        return

    st.success(f"{len(session.cruxes)} pontos de divergencia encontrados.")
    for crux in session.cruxes:
        dist = crux.get("cosine_distance", 0)
        label = f"**{crux['topic']} / {crux['subtopic']}** — distancia coseno: {dist:.2f}"
        with st.expander(label):
            st.markdown(f"**Ponto de divergencia:** {crux.get('cruxClaim', '')}")
            st.markdown(f"*Explicacao:* {crux.get('explanation', '')}")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Concordam:**")
                for g in crux.get("agree", []):
                    st.markdown(f"- {g}")
            with col2:
                st.markdown("**Discordam:**")
                for g in crux.get("disagree", []):
                    st.markdown(f"- {g}")
```

### Step 5 — Verify

Using `tttc-poc/data/sample-gavealab.csv` (territory: asfalto/favela):
1. Upload CSV, gerar tópicos, extrair claims.
2. Clicar "Detectar divergencias".
3. Confirmar que o spinner mostra progresso e não trava.
4. Confirmar que subtópicos com territory asfalto/favela aparecem como cruxes (se cosine_distance > 0.25).
5. Confirmar que subtópicos com apenas um grupo **não** geram crux.
6. Confirmar que cada crux card exibe `cosine_distance`, `cruxClaim`, e colunas Concordam/Discordam.
7. Reload app — cruxes devem recarregar do SQLite sem re-executar.

## Commit
```
feat(gavealab-poc): embedding-based crux detection with multilingual-e5-large + Ollama labeling
```

## Review log
| Perspective | Status | Notes |
|-------------|--------|-------|
| DATA | Adopted | Embedding centroid per territory group; cosine distance gates LLM calls |
| ARCH | Adopted | embeddings.py singleton keeps model loaded once; pipeline/cruxes.py pure Python |
| PERF | Adopted | LLM called only for divergent subtopics (O(divergent) not O(all_subtopics)) |
| UX | Adopted | Two-column layout; cosine distance shown as confidence signal per crux |
| DX | Adopted | 3-attempt retry loop on JSON parse failures from Ollama |
