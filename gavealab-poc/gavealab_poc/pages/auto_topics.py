from __future__ import annotations
import streamlit as st
from gavealab_poc.workspace import GaveaLabWorkspace


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("2. Temas automaticos")
    session = st.session_state.get("session")
    if session is None:
        st.warning("Crie ou carregue uma sessao na pagina 'Upload CSV'.")
        return

    if st.button("Gerar temas com IA"):
        with st.spinner("Analisando relatos com Ollama..."):
            try:
                from gavealab_poc.pipeline.topics import generate_topic_tree
                generate_topic_tree(session)
                st.session_state.session = session
            except Exception as exc:
                st.error(f"Erro ao chamar Ollama: {exc}")
                return

    if not session.topic_tree:
        st.info("Clique em 'Gerar temas' para iniciar a analise.")
        return

    st.success(f"{len(session.topic_tree)} temas identificados. Resultado salvo.")
    for topic in session.topic_tree:
        with st.expander(
            f"**{topic['topicName']}** -- {topic.get('topicShortDescription', '')}"
        ):
            for sub in topic.get("subtopics", []):
                st.markdown(
                    f"- **{sub['subtopicName']}**: {sub.get('subtopicShortDescription', '')}"
                )
