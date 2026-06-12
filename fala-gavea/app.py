from __future__ import annotations

import hashlib
import os
import uuid
import pandas as pd
import httpx
import plotly.express as px
import streamlit as st
from fala_gavea.pipeline.cluster import build_cluster_df
from fala_gavea.pipeline.label_clusters import label_clusters

API_URL = os.environ.get("FALA_GAVEA_API_URL", "http://localhost:8000")
POSTS_PER_PAGE = 20

st.set_page_config(page_title="Fala Gavea", page_icon="🗣️", layout="wide")

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

USER_ID: str = st.session_state.user_id

_CITIZEN_NAMES: list[str] = [
    "Ana", "Carlos", "Fernanda", "João", "Mariana",
    "Pedro", "Luciana", "Rafael", "Beatriz", "Rodrigo",
    "Camila", "Diego", "Patricia", "André", "Juliana",
    "Marcos", "Vanessa", "Felipe", "Sandra", "Gustavo",
    "Renata", "Bruno", "Tatiana", "Eduardo", "Cristina",
    "Thiago", "Adriana", "Henrique", "Priscila", "Leonardo",
]


def citizen_name(user_id: str) -> str:
    """Deterministic human-readable name from a UUID."""
    idx = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % len(_CITIZEN_NAMES)
    return _CITIZEN_NAMES[idx]


# -- helpers ------------------------------------------------------------------


def api_get(path: str, **params: object) -> list | dict:
    r = httpx.get(f"{API_URL}{path}", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def api_post(path: str, body: dict) -> dict:
    r = httpx.post(f"{API_URL}{path}", json=body, timeout=10)
    r.raise_for_status()
    return r.json()


# -- pages --------------------------------------------------------------------


def page_posts() -> None:
    st.header("📋 Postagens")

    if "posts_page" not in st.session_state:
        st.session_state.posts_page = 0

    page: int = st.session_state.posts_page
    offset = page * POSTS_PER_PAGE

    try:
        posts = api_get("/citizen_posts/", limit=POSTS_PER_PAGE, offset=offset)
    except Exception as e:
        st.error(f"Erro ao carregar postagens: {e}")
        return

    if not posts and page == 0:
        st.info("Nenhuma postagem ainda. Crie a primeira!")
        return

    for post in posts:
        with st.container(border=True):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{post['territory_name']}** · _{post['territory_level']}_")
                st.write(post["text"])
                if post.get("ai_labels"):
                    st.caption("Labels: " + ", ".join(post["ai_labels"]))
                st.caption(f"👤 {citizen_name(post['author_id'])}  ·  {post['created_at'][:10]}")
            with col2:
                likes = post.get("likes_count", 0)
                if st.button(f"❤️ {likes}", key=f"like_{post['id']}"):
                    try:
                        api_post(f"/citizen_posts/{post['id']}/likes", {"user_id": USER_ID})
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                if likes > 0:
                    cache_key = f"likers_{post['id']}"
                    with st.expander("Ver quem curtiu"):
                        if cache_key not in st.session_state:
                            if st.button("Carregar curtidas", key=f"load_likes_{post['id']}"):
                                try:
                                    likes_data = api_get(f"/citizen_posts/{post['id']}/likes")
                                    st.session_state[cache_key] = likes_data.get("likers", [])
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao carregar likes: {e}")
                        else:
                            for liker in st.session_state[cache_key]:
                                st.caption(f"👤 {citizen_name(liker['user_id'])}")

    # pagination controls
    col_prev, col_info, col_next = st.columns([1, 2, 1])
    with col_prev:
        if page > 0:
            if st.button("← Anterior"):
                st.session_state.posts_page -= 1
                st.rerun()
    with col_info:
        start = offset + 1
        end = offset + len(posts)
        st.caption(f"Postagens {start}–{end} · página {page + 1}")
    with col_next:
        if len(posts) == POSTS_PER_PAGE:
            if st.button("Próxima →"):
                st.session_state.posts_page += 1
                st.rerun()


def page_new_post() -> None:
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
                    "author_id": USER_ID,
                })
                st.success("Postagem publicada!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao publicar: {e}")


def page_label_feedback() -> None:
    st.header("🏷️ Validar Labels da IA")
    st.caption("Aprove ou rejeite os labels atribuídos automaticamente pela IA.")
    try:
        posts = api_get("/citizen_posts/", limit=100)
    except Exception as e:
        st.error(f"Erro ao carregar postagens: {e}")
        return

    posts_with_labels = [p for p in posts if p.get("ai_labels")]
    if not posts_with_labels:
        st.info("Nenhuma postagem com labels de IA ainda.")
        return

    for post in posts_with_labels:
        with st.expander(f"{post['text'][:80]}..."):
            st.caption(f"Território: {post['territory_name']} · {post['created_at'][:10]}")
            for label in post["ai_labels"]:
                existing = post.get("label_feedback", {}).get(label)
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"`{label}`")
                with col2:
                    approved = isinstance(existing, dict) and existing.get("approved") is True
                    if st.button("👍", key=f"up_{post['id']}_{label}", type="primary" if approved else "secondary"):
                        try:
                            api_post(
                                f"/citizen_posts/{post['id']}/label_feedback",
                                {"label": label, "approved": True, "user_id": USER_ID},
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                with col3:
                    rejected = isinstance(existing, dict) and existing.get("approved") is False
                    if st.button("👎", key=f"down_{post['id']}_{label}", type="primary" if rejected else "secondary"):
                        try:
                            api_post(
                                f"/citizen_posts/{post['id']}/label_feedback",
                                {"label": label, "approved": False, "user_id": USER_ID},
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))


def page_dashboard() -> None:
    st.header("📊 Dashboard")
    try:
        posts = api_get("/citizen_posts/", limit=1500)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return

    if not posts:
        st.info("Nenhuma postagem ainda.")
        return

    import pandas as pd

    df = pd.DataFrame(posts)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de postagens", len(df))
    total_likes = int(df["likes_count"].sum()) if "likes_count" in df else 0
    col2.metric("Total de likes", total_likes)
    avg_likes = round(total_likes / len(df), 1) if len(df) else 0
    col3.metric("Média de likes por post", avg_likes)
    posts_with_labels = df[df["ai_labels"].apply(lambda x: len(x) > 0)] if "ai_labels" in df else pd.DataFrame()

    st.subheader("Top posts por likes")
    top = df.nlargest(10, "likes_count")[["text", "territory_name", "territory_level", "likes_count"]]
    top = top.copy()
    top["text"] = top["text"].str[:60] + "..."
    st.dataframe(top, use_container_width=True)

    st.subheader("Distribuição por território")
    by_territory = df.groupby("territory_name").size().reset_index(name="posts")
    st.bar_chart(by_territory.set_index("territory_name"))

    # ── Timeline de postagens ─────────────────────────────────────────────────
    if "created_at" in df:
        st.subheader("Postagens por dia")
        df["date"] = pd.to_datetime(df["created_at"]).dt.date
        timeline = df.groupby("date").size().reset_index(name="posts")
        st.line_chart(timeline.set_index("date"))

    # ── Histograma de likes ───────────────────────────────────────────────────
    if total_likes > 0:
        st.subheader("Distribuição de likes por post")
        bins = [0, 1, 2, 4, 7, 11, 20, 50, float("inf")]
        labels_hist = ["0", "1", "2-3", "4-6", "7-10", "11-19", "20-49", "50+"]
        df["likes_bucket"] = pd.cut(
            df["likes_count"], bins=bins, right=False, labels=labels_hist
        )
        hist = df["likes_bucket"].value_counts().sort_index()
        st.bar_chart(hist)

    if not posts_with_labels.empty:
        st.subheader("Feedback de labels")
        feedback_rows = []
        for _, row in posts_with_labels.iterrows():
            for label, fb in (row.get("label_feedback") or {}).items():
                if isinstance(fb, dict):
                    approved_val = fb.get("approved")
                    usuario = fb.get("user_id", "")
                else:
                    approved_val = fb
                    usuario = ""
                feedback_rows.append({"label": label, "aprovado": approved_val, "usuario": usuario})
        if feedback_rows:
            fdf = pd.DataFrame(feedback_rows)
            summary = fdf.groupby(["label", "aprovado"]).size().reset_index(name="count")
            st.dataframe(summary, use_container_width=True)

    st.subheader("Rastreabilidade de likes")
    if st.button("Carregar rastreabilidade"):
        likes_rows = []
        posts_with_likes = [p for p in posts if p.get("likes_count", 0) > 0]
        with st.spinner(f"Buscando likes de {len(posts_with_likes)} postagens..."):
            for post in posts_with_likes:
                try:
                    likes_data = api_get(f"/citizen_posts/{post['id']}/likes")
                    likers = [lr["user_id"] for lr in likes_data.get("likers", [])]
                    likes_rows.append({
                        "post_id": post["id"][:8],
                        "texto": post["text"][:40],
                        "curtidores": ", ".join(citizen_name(u) for u in likers),
                    })
                except Exception:
                    pass
        if likes_rows:
            st.dataframe(pd.DataFrame(likes_rows), use_container_width=True)
        else:
            st.info("Nenhum like registrado.")

    st.subheader("Rastreabilidade de labels")
    label_trace_rows = []
    for post in posts:
        feedback = post.get("label_feedback") or {}
        for label, info in feedback.items():
            if isinstance(info, dict):
                label_trace_rows.append({
                    "label": label,
                    "aprovado": info.get("approved"),
                    "usuario": citizen_name(str(info.get("user_id", "") or "")),
                })
    if label_trace_rows:
        st.dataframe(pd.DataFrame(label_trace_rows), use_container_width=True)
    else:
        st.info("Nenhum feedback de label registrado.")


def page_clusters() -> None:
    st.header("🗺️ Explorar Clusters")
    st.caption("Clusterização semântica dos posts via UMAP + HDBSCAN. Labels gerados por IA.")

    if "cluster_df" not in st.session_state:
        st.session_state.cluster_df = None

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

        with st.spinner("Calculando embeddings e clusters (pode levar alguns minutos na primeira vez)..."):
            df = build_cluster_df(posts)

        with st.spinner("Gerando labels com IA..."):
            cluster_label_map = label_clusters(df)
            df["cluster_label"] = df["cluster_id"].map(cluster_label_map)

        st.session_state.cluster_df = df
        n_clusters = df["cluster_id"].nunique() - (1 if -1 in df["cluster_id"].values else 0)
        st.success(f"{len(posts)} posts clusterizados em {n_clusters} clusters.")

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
        ordered = pd.concat([main, noise]).reset_index(drop=True)

        for _, row in ordered.iterrows():
            label = row["cluster_label"]
            n = row["n"]
            cluster_posts = df[df["cluster_label"] == label][["text", "territory_name"]].copy()
            cluster_posts.columns = ["Relato", "Territorio"]
            with st.expander(f"{label}  ({n} posts)", expanded=False):
                st.dataframe(cluster_posts, use_container_width=True)

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


def page_bulk_insert() -> None:
    st.header("📥 Inserção em Massa")
    st.caption(
        "Faça upload de um CSV com as colunas `text`, `territory_level`, "
        "`territory_name` e `author_id` para criar múltiplas postagens de uma vez."
    )

    uploaded = st.file_uploader("Arquivo CSV", type=["csv"])
    if uploaded is None:
        st.info("Selecione um arquivo CSV para continuar.")
        return

    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Erro ao ler o CSV: {e}")
        return

    required = {"text", "territory_level", "territory_name", "author_id"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"Colunas obrigatórias ausentes: {', '.join(sorted(missing))}")
        return

    valid_levels = {"neighborhood", "district", "city"}
    invalid_mask = ~df["territory_level"].isin(valid_levels)
    if invalid_mask.any():
        st.warning(
            f"{int(invalid_mask.sum())} linha(s) com `territory_level` inválido "
            "(valores aceitos: neighborhood, district, city). Essas linhas serão ignoradas."
        )
        df = df[~invalid_mask]

    df = df.dropna(subset=["text", "territory_level", "territory_name", "author_id"])
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"].str.len() > 0].reset_index(drop=True)

    if df.empty:
        st.error("Nenhuma linha válida encontrada no CSV após a validação.")
        return

    st.subheader(f"Prévia — {len(df)} postagem(ns) a criar")
    st.dataframe(
        df[["text", "territory_level", "territory_name", "author_id"]].head(20),
        use_container_width=True,
    )
    if len(df) > 20:
        st.caption(f"... e mais {len(df) - 20} linha(s) não exibidas.")

    if st.button("📤 Criar Postagens", type="primary"):
        items = df[["text", "territory_level", "territory_name", "author_id"]].to_dict(orient="records")
        with st.spinner(f"Criando {len(items)} postagem(ns)..."):
            try:
                result = api_post("/citizen_posts/bulk", {"items": items})
                created = len(result.get("items", []))
                st.success(f"{created} postagem(ns) criada(s) com sucesso!")
            except Exception as e:
                st.error(f"Erro ao criar postagens: {e}")


# -- navigation ---------------------------------------------------------------

PAGES = {
    "📋 Postagens": page_posts,
    "✍️ Nova Postagem": page_new_post,
    "🏷️ Validar Labels": page_label_feedback,
    "📊 Dashboard": page_dashboard,
    "🗺️ Explorar Clusters": page_clusters,
    "📥 Inserção em Massa": page_bulk_insert,
}

with st.sidebar:
    st.title("🗣️ Fala Gávea")
    st.caption(f"Sessão: `{USER_ID[:8]}...`")
    st.divider()
    selection = st.radio("Navegação", list(PAGES.keys()), label_visibility="collapsed")

PAGES[selection]()
