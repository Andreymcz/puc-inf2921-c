from __future__ import annotations

import streamlit as st

from .shared import api_post


def render() -> None:
    st.header("✍️ Nova Postagem")
    with st.form("new_post_form"):
        text = st.text_area("Relato *", placeholder="Descreva sua sugestão ou reclamação...")
        col1, col2 = st.columns(2)
        with col1:
            territory_level = st.selectbox("Nível territorial", ["neighborhood", "district", "city"])
        with col2:
            territory_name = st.text_input("Nome do território *", placeholder="Ex: Gávea")
        submitted = st.form_submit_button("Publicar", type="primary")

    if submitted:
        if not text.strip() or not territory_name.strip():
            st.error("Preencha o relato e o nome do território.")
        else:
            try:
                api_post("/citizen_posts/", {
                    "text": text.strip(),
                    "territory_level": territory_level,
                    "territory_name": territory_name.strip(),
                    "author_id": st.session_state.user_id,
                })
                st.success("Postagem publicada!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao publicar: {e}")
