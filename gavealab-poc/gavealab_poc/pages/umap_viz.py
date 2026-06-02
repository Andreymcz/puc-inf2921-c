from __future__ import annotations
import streamlit as st
from gavealab_poc.workspace import GaveaLabWorkspace


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("5. Visualizar clusters")
    session = st.session_state.get("session")
    if session is None:
        st.warning("Crie ou carregue uma sessao na pagina 'Upload CSV'.")
        return
    if not session.claims_tree:
        st.warning("Extraia os claims primeiro (pagina 'Temas automaticos').")
        return

    st.caption(
        "Projeta os embeddings dos claims em 2D via UMAP. "
        "Cada ponto e um claim; cor = grupo territorial."
    )

    with st.form("umap_params"):
        n_neighbors = st.slider("n_neighbors", 2, 50, 15,
                                help="Controla o balanco local/global da projecao.")
        min_dist = st.slider("min_dist", 0.01, 0.5, 0.1, step=0.01,
                             help="Distancia minima entre pontos na projecao.")
        submitted = st.form_submit_button("Gerar visualizacao")

    if not submitted:
        st.info("Ajuste os parametros e clique em 'Gerar visualizacao'.")
        return

    with st.spinner("Calculando embeddings e projecao UMAP..."):
        try:
            import plotly.express as px
            from gavealab_poc.pipeline.umap_viz import build_umap_df
            df = build_umap_df(
                session.claims_tree,
                n_neighbors=n_neighbors,
                min_dist=min_dist,
            )
        except Exception as exc:
            st.error(f"Erro: {exc}")
            return

    if df.empty:
        st.warning("Nenhum claim encontrado para visualizar.")
        return

    fig = px.scatter(
        df, x="x", y="y",
        color="territory",
        hover_data={"claim": True, "subtopic": True, "x": False, "y": False},
        title="Clusters de claims (UMAP 2D)",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(marker=dict(size=10, opacity=0.85))
    fig.update_layout(legend_title_text="Territorio", height=600)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Tabela de dados"):
        st.dataframe(df[["territory", "topic", "subtopic", "claim"]], use_container_width=True)
