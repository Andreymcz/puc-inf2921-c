# Plan 000016 | FEATURE-X | 2026-06-02 02:19 | GaveaLab PoC -- UMAP cluster visualization | Review: light
# DONE | 2026-06-02 02:32 UTC |
plan_format_version: 1

## Brief (verbatim)
can we plan a visualization of the clusters using umap ?

## Context

The claim embeddings from `multilingual-e5-large` are 1024-dimensional vectors. UMAP reduces them
to 2D for scatter-plot visualization. Each point = one claim; colour = territory group (asfalto /
favela / other); hover = claim text + subtopic. This gives an immediate visual intuition of whether
territory groups actually cluster separately -- complementing the cosine-distance numbers in the
diagnostics table.

**Scope**: new sidebar page "Visualizar clusters" added after "Opinioes divergentes". Reads
`session.claims_tree` (already populated), re-embeds claims (model is cached via `lru_cache` so
no reload cost), runs UMAP, and renders a Plotly scatter chart. No new persistence needed.

**Dependencies to add**: `umap-learn>=0.5`, `plotly>=5.0` (Plotly renders natively in Streamlit).

**UMAP parameters**: `n_neighbors=15`, `min_dist=0.1`, `metric="cosine"`, `random_state=42`.
These are reasonable defaults for a small dataset (tens to low hundreds of points). Expose
`n_neighbors` and `min_dist` as sidebar sliders so the user can tune interactively.

## Files
- `gavealab-poc/pyproject.toml` (update — add umap-learn, plotly)
- `gavealab-poc/gavealab_poc/pipeline/umap_viz.py` (create — compute UMAP projection)
- `gavealab-poc/gavealab_poc/pages/umap_viz.py` (create — Streamlit page)
- `gavealab-poc/app.py` (update — add "Visualizar clusters" page to sidebar)

## Steps

### Step 1 — pyproject.toml: add umap-learn and plotly

- [x] Done

Add to `[project] dependencies`:
```
"umap-learn>=0.5",
"plotly>=5.0",
```

**Files**: `gavealab-poc/pyproject.toml`
**Tests**: N/A
**Verify**: `uv sync` completes without errors inside `gavealab-poc/`.

---

### Step 2 — gavealab_poc/pipeline/umap_viz.py

- [x] Done

Create the pipeline module that takes a `claims_tree` dict and returns a DataFrame ready for
Plotly, plus the UMAP reducer.

```python
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
```

**Files**: `gavealab-poc/gavealab_poc/pipeline/umap_viz.py`
**Tests**: N/A
**Verify**: module imports cleanly; `build_umap_df({})` returns an empty DataFrame.

---

### Step 3 — gavealab_poc/pages/umap_viz.py

- [x] Done

Create the Streamlit page. Key design choices:
- Sliders for `n_neighbors` (5–50, default 15) and `min_dist` (0.01–0.5, default 0.1) in a
  `st.form` so UMAP only reruns on explicit "Gerar visualizacao" click, not on every slider move.
- Plotly `scatter` with `color="territory"`, `hover_data=["claim", "subtopic"]`.
- Color scale uses Plotly's qualitative `Pastel` palette (readable, territory-neutral).

```python
from __future__ import annotations
import streamlit as st
from gavealab_poc.workspace import GaveaLabWorkspace


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("5. Visualizar clusters")
    session = st.session_state.get("session")
    if session is None:
        st.warning("Crie ou carregue uma sessao na pagina 'Upload CSV'.")
        return
    if not session.claims_tree:
        st.warning("Extraia os claims primeiro (pagina 'Temas automaticos').")
        return

    st.caption(
        "Projeta os embeddings dos claims em 2D via UMAP. "
        "Cada ponto e um claim; cor = grupo territorial."
    )

    with st.form("umap_params"):
        n_neighbors = st.slider("n_neighbors", 2, 50, 15,
                                help="Controla o balanco local/global da projecao.")
        min_dist = st.slider("min_dist", 0.01, 0.5, 0.1, step=0.01,
                             help="Distancia minima entre pontos na projecao.")
        submitted = st.form_submit_button("Gerar visualizacao")

    if not submitted:
        st.info("Ajuste os parametros e clique em 'Gerar visualizacao'.")
        return

    with st.spinner("Calculando embeddings e projecao UMAP..."):
        try:
            import plotly.express as px
            from gavealab_poc.pipeline.umap_viz import build_umap_df
            df = build_umap_df(
                session.claims_tree,
                n_neighbors=n_neighbors,
                min_dist=min_dist,
            )
        except Exception as exc:
            st.error(f"Erro: {exc}")
            return

    if df.empty:
        st.warning("Nenhum claim encontrado para visualizar.")
        return

    fig = px.scatter(
        df, x="x", y="y",
        color="territory",
        hover_data={"claim": True, "subtopic": True, "x": False, "y": False},
        title="Clusters de claims (UMAP 2D)",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(marker=dict(size=10, opacity=0.85))
    fig.update_layout(legend_title_text="Territorio", height=600)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Tabela de dados"):
        st.dataframe(df[["territory", "topic", "subtopic", "claim"]], use_container_width=True)
```

**Files**: `gavealab-poc/gavealab_poc/pages/umap_viz.py`
**Tests**: N/A
**Verify**: page renders without error; scatter chart appears with coloured points grouped by territory.

---

### Step 4 — app.py: add "Visualizar clusters" to sidebar

- [x] Done

```python
# Add to the radio options list:
page = st.sidebar.radio(
    "Navegacao",
    ["Upload CSV", "Temas automaticos", "Categorizar por temas",
     "Opinioes divergentes", "Visualizar clusters"],
)

# Add the new branch to the if/elif chain (before the final else):
elif page == "Visualizar clusters":
    from gavealab_poc.pages.umap_viz import render
```

**Files**: `gavealab-poc/app.py`
**Tests**: N/A
**Verify**: "Visualizar clusters" appears in the sidebar; navigating to it shows the UMAP page.

---

## Commit
```
feat(gavealab-poc): UMAP 2D cluster visualization of claim embeddings with Plotly
```

## Review log
| Perspective | Status | Notes |
|-------------|--------|-------|
| ARCH | Adopted | Pipeline module owns projection logic; page is thin adapter |
| PERF | Adopted | `lru_cache` on model means no re-download; form gate prevents re-run on slider drag |
| UX | Adopted | st.form decouples slider interaction from compute; hover shows claim + subtopic |
| DX | Adopted | n_neighbors clamped to min(value, N-1) to avoid UMAP crash on tiny datasets |
