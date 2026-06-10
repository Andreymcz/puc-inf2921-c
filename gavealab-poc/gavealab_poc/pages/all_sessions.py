from __future__ import annotations

import streamlit as st

from gavealab_poc.workspace import GaveaLabWorkspace

_RESULT_LABELS = {
    "topic_tree": "Temas",
    "claims_tree": "Claims",
    "cruxes": "Divergencias",
    "manual_categories": "Categorias",
}

_UMAP_BADGE = "UMAP"


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("Todos os Estudos")

    sessions = workspace.get_sessions_summary()
    if not sessions:
        st.info("Nenhuma sessao encontrada. Use a pagina 'Upload CSV' para criar sua primeira analise.")
        return

    for s in sessions:
        with st.container(border=True):
            col_info, col_badges = st.columns([3, 2])
            with col_info:
                st.markdown(f"**{s['name']}**")
                st.caption(s["created_at"][:10])
                st.caption(f"{s['comment_count']} relatos")
            with col_badges:
                available = set(s["available_results"])
                for result_type, label in _RESULT_LABELS.items():
                    color = "green" if result_type in available else "gray"
                    st.badge(label, color=color)
                umap_color = "green" if "claims_tree" in available else "gray"
                st.badge(_UMAP_BADGE, color=umap_color)

            if st.button("Abrir este estudo", key=f"open_{s['id']}"):
                st.session_state.session = workspace.load_session(s["id"])
                st.success(f"Sessao '{s['name']}' carregada. Use a navegacao para continuar a analise.")
                st.rerun()
