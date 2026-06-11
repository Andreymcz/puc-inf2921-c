from __future__ import annotations
import logging
import streamlit as st
from gavealab_poc.workspace import GaveaLabWorkspace

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

st.set_page_config(page_title="GaveaLab -- Analise de Relatos", layout="wide")


@st.cache_resource
def get_workspace() -> GaveaLabWorkspace:
    return GaveaLabWorkspace("gavealab.db")


if "session" not in st.session_state:
    st.session_state.session = None


def _page_all_sessions() -> None:
    from gavealab_poc.pages.all_sessions import render
    render(get_workspace())


def _page_upload() -> None:
    from gavealab_poc.pages.upload import render
    render(get_workspace())


def _page_auto_topics() -> None:
    from gavealab_poc.pages.auto_topics import render
    render(get_workspace())


def _page_manual_topics() -> None:
    from gavealab_poc.pages.manual_topics import render
    render(get_workspace())


def _page_cruxes() -> None:
    from gavealab_poc.pages.cruxes import render
    render(get_workspace())


def _page_umap_viz() -> None:
    from gavealab_poc.pages.umap_viz import render
    render(get_workspace())


pages = [
    st.Page(_page_all_sessions, title="Todos os Estudos", icon=":material/home:", default=True),
    st.Page(_page_upload, title="Upload CSV", icon=":material/upload_file:"),
    st.Page(_page_auto_topics, title="Temas automaticos", icon=":material/auto_awesome:"),
    st.Page(_page_manual_topics, title="Categorizar por temas", icon=":material/category:"),
    st.Page(_page_cruxes, title="Opinioes divergentes", icon=":material/compare_arrows:"),
    st.Page(_page_umap_viz, title="Visualizar clusters", icon=":material/scatter_plot:"),
]

pg = st.navigation(pages)

if st.session_state.get("session"):
    st.sidebar.success(f"Sessao ativa: **{st.session_state.session.name}**")
else:
    st.sidebar.info("Nenhuma sessao ativa.")

pg.run()
