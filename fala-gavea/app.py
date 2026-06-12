from __future__ import annotations

import uuid

import streamlit as st

from app_pages import bulk_insert, clusters, dashboard, label_feedback, new_post, posts

st.set_page_config(page_title="Fala Gavea", page_icon="🗣️", layout="wide")

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

pg = st.navigation(
    [
        st.Page(posts.render, title="Postagens", icon="📋", default=True),
        st.Page(new_post.render, title="Nova Postagem", icon="✍️"),
        st.Page(label_feedback.render, title="Validar Labels", icon="🏷️"),
        st.Page(dashboard.render, title="Dashboard", icon="📊"),
        st.Page(clusters.render, title="Explorar Clusters", icon="🗺️"),
        st.Page(bulk_insert.render, title="Inserção em Massa", icon="📥"),
    ]
)

with st.sidebar:
    st.title("🗣️ Fala Gávea")
    st.caption(f"Sessão: `{st.session_state.user_id[:8]}...`")
    st.divider()

pg.run()
