from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from fala_gavea.pipeline.cluster import build_cluster_df
from fala_gavea.pipeline.label_clusters import label_clusters

from .shared import api_get, api_post


def render() -> None:
    st.header("🗺️ Explorar Clusters")
    st.caption("Clusterização semântica dos posts via UMAP + HDBSCAN. Labels gerados por IA.")

    if "cluster_df" not in st.session_state:
        st.session_state.cluster_df = None

    with st.expander("⚙️ Parâmetros de clusterização", expanded=False):
        n_neighbors = st.slider(
            "n_neighbors (UMAP)",
            min_value=2, max_value=50, value=15,
            help="Controla o balanço local/global da projeção. Reduza para datasets pequenos.",
        )
        min_dist = st.slider(
            "min_dist (UMAP)",
            min_value=0.01, max_value=0.5, value=0.1, step=0.01,
            help="Distância mínima entre pontos. Valores menores criam clusters mais compactos.",
        )
        min_cluster_size = st.slider(
            "min_cluster_size (HDBSCAN)",
            min_value=2, max_value=20, value=5,
            help="Tamanho mínimo de um cluster. Reduza se poucos posts formam grupos.",
        )

    col1, col2 = st.columns([1, 4])
    with col1:
        run_btn = st.button("🔄 Gerar Clusters", use_container_width=True)
        save_btn = st.button(
            "💾 Salvar Labels",
            disabled=st.session_state.cluster_df is None,
            use_container_width=True,
        )

    if run_btn:
        try:
            with st.spinner("Buscando posts..."):
                posts = api_get("/citizen_posts/", limit=500, offset=0)
        except Exception as e:
            st.error(f"Erro ao carregar posts: {e}")
            return

        if not posts:
            st.warning("Nenhum post encontrado.")
            return

        with st.spinner("Calculando clusters (embeddings já disponíveis)..."):
            df = build_cluster_df(
                posts,
                n_neighbors=n_neighbors,
                min_dist=min_dist,
                min_cluster_size=min_cluster_size,
            )

        df["cluster_label"] = df["cluster_id"].apply(
            lambda cid: "Não classificado" if cid == -1 else f"Cluster {cid}"
        )

        st.session_state.cluster_df = df
        n_clusters = df["cluster_id"].nunique() - (1 if -1 in df["cluster_id"].values else 0)
        st.success(f"{len(posts)} posts clusterizados em {n_clusters} clusters.")
        noise_count = int((df["cluster_id"] == -1).sum())
        if noise_count > 0:
            st.info(
                f"{noise_count} posts não foram atribuídos a nenhum cluster (ruído). "
                "Se esse número for alto, reduza `min_cluster_size` ou `n_neighbors`."
            )

    df = st.session_state.cluster_df
    if df is not None:
        fig = px.scatter(
            df,
            x="x",
            y="y",
            color="cluster_label",
            hover_data={"text": True, "territory_name": True, "x": False, "y": False},
            title="Clusters de Posts — Espaço Semântico (UMAP)",
            labels={"cluster_label": "Cluster", "x": "UMAP-1", "y": "UMAP-2"},
        )
        fig.update_traces(marker=dict(size=6, opacity=0.7))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Posts por Cluster")

        cluster_groups = df.groupby("cluster_label")
        counts = cluster_groups.size().reset_index(name="n")
        noise_label = "Nao classificado"
        main = counts[counts["cluster_label"] != noise_label].sort_values("n", ascending=False)
        noise = counts[counts["cluster_label"] == noise_label]
        ordered: pd.DataFrame = pd.concat([main, noise]).reset_index(drop=True)
        
        for _, row in ordered.iterrows():
            label = row["cluster_label"]
            n = row["n"]
            mask = df["cluster_label"] == label
            cluster_posts = df[mask][["text", "territory_name"]].copy()
            cluster_posts.columns = ["Relato", "Territorio"]
            with st.expander(f"{label}  ({n} posts)", expanded=False):
                st.dataframe(cluster_posts, use_container_width=True)
                cluster_ids_in_group = df[mask]["cluster_id"].unique()
                if not any(cid == -1 for cid in cluster_ids_in_group):
                    if st.button("🤖 Gerar label com IA", key=f"label_btn_{label}"):
                        cid = int(cluster_ids_in_group[0])
                        with st.spinner(f"Gerando label para Cluster {cid}..."):
                            new_labels = label_clusters(df[df["cluster_id"] == cid])
                        new_label = new_labels.get(cid, label)
                        df.loc[df["cluster_id"] == cid, "cluster_label"] = new_label
                        st.session_state.cluster_df = df
                        st.rerun()

        if save_btn:
            with st.spinner("Salvando labels nos posts..."):
                errors = 0
                for _, row in df.iterrows():
                    if row["cluster_id"] == -1:
                        continue
                    try:
                        api_post(
                            f"/citizen_posts/{row['post_id']}/ai_labels",
                            {"labels": [row["cluster_label"]]},
                        )
                    except Exception:
                        errors += 1
            if errors:
                st.warning(f"Labels salvos com {errors} erros.")
            else:
                st.success("Labels salvos com sucesso!")
