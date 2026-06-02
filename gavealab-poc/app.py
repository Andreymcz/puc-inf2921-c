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
st.title("GaveaLab -- Analise de Relatos de Cidadaos")


@st.cache_resource
def get_workspace() -> GaveaLabWorkspace:
    return GaveaLabWorkspace("gavealab.db")


workspace = get_workspace()

if "session" not in st.session_state:
    st.session_state.session = None

page = st.sidebar.radio(
    "Navegacao",
    ["Upload CSV", "Temas automaticos", "Categorizar por temas",
     "Opinioes divergentes", "Visualizar clusters"],
)

if page == "Upload CSV":
    from gavealab_poc.pages.upload import render
elif page == "Temas automaticos":
    from gavealab_poc.pages.auto_topics import render
elif page == "Categorizar por temas":
    from gavealab_poc.pages.manual_topics import render
elif page == "Visualizar clusters":
    from gavealab_poc.pages.umap_viz import render
else:
    from gavealab_poc.pages.cruxes import render

render(workspace)
