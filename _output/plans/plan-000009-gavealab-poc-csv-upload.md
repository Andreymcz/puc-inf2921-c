# Plan 000009 | FEATURE-X | 2026-06-01 22:44 | GaveaLab PoC -- CSV upload page | Review: light
# DONE | 2026-06-02 00:05 UTC |
plan_format_version: 1

## Revision note
Revised 2026-06-01 23:10 UTC: render() now receives workspace; session created via
workspace.create_session(); sample CSV reference added for manual testing.

## Brief (verbatim)
Implement the CSV upload page: file picker, session name input, validation, preview,
and session creation via GaveaLabWorkspace.
(Wave 1, step 1 of roadmap-000007. Depends on plan-000008.)

## Files
- `gavealab-poc/gavealab_poc/pages/upload.py` (replace stub)

## Steps

### Step 1 -- Implement upload.py

```python
from __future__ import annotations
import streamlit as st
from gavealab_poc.workspace import GaveaLabWorkspace


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("1. Upload de Relatos")
    st.markdown(
        "Faca o upload de um arquivo CSV com os relatos dos cidadaos. "
        "Colunas esperadas: **comment** ou **text** (obrigatoria), "
        "**id** e **territory** (opcionais)."
    )

    session_name = st.text_input(
        "Nome da analise",
        placeholder="Ex.: Gavea 2026 -- rodada 1",
    )

    uploaded = st.file_uploader("Escolha um arquivo CSV", type=["csv"])
    if uploaded is None:
        st.info("Aguardando arquivo...")
        return

    # preview without committing
    import pandas as pd, io
    try:
        preview_df = pd.read_csv(io.BytesIO(uploaded.read()))
        uploaded.seek(0)
    except Exception as exc:
        st.error(f"Erro ao ler CSV: {exc}")
        return

    st.dataframe(preview_df.head(10), use_container_width=True)
    st.caption(f"{len(preview_df)} linhas detectadas.")

    if not session_name.strip():
        st.warning("Digite um nome para a analise antes de continuar.")
        return

    if st.button("Criar sessao de analise"):
        try:
            session = workspace.create_session(session_name.strip(), uploaded)
            st.session_state.session = session
            st.success(
                f"Sessao '{session_name}' criada com {len(session.df)} relatos. "
                "Use o menu lateral para escolher a ferramenta de analise."
            )
        except ValueError as exc:
            st.error(str(exc))

    # show existing sessions
    st.divider()
    st.subheader("Sessoes anteriores")
    sessions = workspace.list_sessions()
    if not sessions:
        st.caption("Nenhuma sessao encontrada.")
        return
    for s in sessions:
        col1, col2 = st.columns([4, 1])
        col1.markdown(f"**{s['name']}** -- {s['created_at'][:10]}")
        if col2.button("Carregar", key=f"load_{s['id']}"):
            st.session_state.session = workspace.load_session(s["id"])
            st.success(f"Sessao '{s['name']}' carregada.")
```

### Step 2 -- Manual verification
Reference CSV: `tttc-poc/data/sample-gavealab.csv`.
- Upload the sample CSV, enter a name, click "Criar sessao de analise".
- Confirm preview shows 30 rows, session is created, `gavealab.db` grows.
- Reload the page and confirm the session appears in "Sessoes anteriores" and can be reloaded.
- Upload a CSV missing both `text` and `comment` columns; confirm the error message appears.

## Commit
```
feat(gavealab-poc): CSV upload page with session creation and persistence
```

## Review log
| Perspective | Status | Notes |
|-------------|--------|-------|
| UX | Adopted | Name input required before commit; preview before commit |
| DATA | Adopted | _parse_csv in workspace normalizes comment->text and filters short rows |
