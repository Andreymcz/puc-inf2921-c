# QA Log | Plan 000016 | 2026-06-02 02:20 UTC | GaveaLab PoC -- UMAP cluster visualization

**Brief**: Plan a UMAP 2D cluster visualization of claim embeddings, coloured by territory group, rendered as a Plotly scatter chart in a new Streamlit page.

---

## Q1
User asked: "can we plan a visualization of the clusters using umap?"

## A1
Plan 000016 generated. Scope: new "Visualizar clusters" sidebar page using `umap-learn` + `plotly`. 4 steps: add dependencies to pyproject.toml, create `pipeline/umap_viz.py` (UMAP projection of claim embeddings), create `pages/umap_viz.py` (Streamlit page with `st.form` sliders for n_neighbors/min_dist and a Plotly scatter chart), update `app.py` sidebar. Model cached via existing `lru_cache` singleton — no re-download cost.
