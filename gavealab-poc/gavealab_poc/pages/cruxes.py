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
                _, diagnostics = detect_cruxes(session)
                st.session_state.session = session
                st.session_state.crux_diagnostics = diagnostics
            except Exception as exc:
                st.error(f"Erro: {exc}")
                return

    diagnostics = st.session_state.get("crux_diagnostics", [])
    if diagnostics:
        with st.expander("🔍 Diagnóstico de distâncias (todos os subtópicos)", expanded=not session.cruxes):
            import pandas as pd
            df_diag = pd.DataFrame([
                {
                    "tópico": d["topic"],
                    "subtópico": d["subtopic"],
                    "grupos": ", ".join(d["groups"]),
                    "distância coseno": d["cosine_distance"],
                    "divergente": "✅" if d["divergent"] else "❌",
                }
                for d in diagnostics
            ])
            st.dataframe(df_diag, use_container_width=True)

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
