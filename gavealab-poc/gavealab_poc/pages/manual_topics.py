from __future__ import annotations
import streamlit as st
import pandas as pd
from gavealab_poc.workspace import GaveaLabWorkspace


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("3. Categorizar por temas")
    session = st.session_state.get("session")
    if session is None:
        st.warning("Crie ou carregue uma sessao na pagina 'Upload CSV'.")
        return

    st.markdown(
        "Digite os temas que deseja usar para categorizar os relatos. "
        "O sistema classificara cada relato nos temas correspondentes."
    )

    themes_input = st.text_area(
        "Temas (um por linha)",
        placeholder="Mobilidade urbana\nSaude publica\nSeguranca\nEducacao",
        height=150,
    )
    themes = [t.strip() for t in themes_input.splitlines() if t.strip()]

    if not themes:
        st.info("Digite ao menos um tema acima.")
        return

    if st.button("Categorizar relatos"):
        with st.spinner("Categorizando com Ollama..."):
            try:
                from gavealab_poc.pipeline.manual_categories import categorize_by_themes
                categorize_by_themes(session, themes)
                st.session_state.session = session
            except Exception as exc:
                st.error(f"Erro: {exc}")
                return

    if not session.manual_categories:
        return

    st.success("Categorias salvas.")
    for theme, items in session.manual_categories.items():
        with st.expander(f"**{theme}** -- {len(items)} relatos"):
            if items:
                cols = ["territory", "text", "reason"] if items and "territory" in items[0] else ["text", "reason"]
                st.dataframe(pd.DataFrame(items)[cols], use_container_width=True)
            else:
                st.write("Nenhum relato classificado neste tema.")
