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

    st.divider()
    st.subheader("Claims por subtema")

    if st.button("Extrair claims (pode demorar)"):
        with st.spinner("Extraindo claims comentario por comentario..."):
            try:
                from gavealab_poc.pipeline.claims import extract_claims
                extract_claims(session)
                st.session_state.session = session
            except Exception as exc:
                st.error(f"Erro: {exc}")
                return

    if not session.claims_tree:
        st.info("Gere os temas e depois clique em 'Extrair claims'.")
        return

    import pandas as pd
    for topic, subtopics in session.claims_tree.items():
        st.markdown(f"### {topic}")
        for subtopic, claims in subtopics.items():
            with st.expander(f"{subtopic} ({len(claims)} claims)"):
                cols = ["claim", "quote", "territory"] if claims and "territory" in claims[0] else ["claim", "quote"]
                st.dataframe(pd.DataFrame(claims)[cols], use_container_width=True)
