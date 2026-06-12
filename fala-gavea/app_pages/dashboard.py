from __future__ import annotations

import pandas as pd
import streamlit as st

from .shared import api_get, citizen_name


def render() -> None:
    st.header("📊 Dashboard")
    try:
        posts = api_get("/citizen_posts/", limit=1500)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return

    if not posts:
        st.info("Nenhuma postagem ainda.")
        return

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

    if "created_at" in df:
        st.subheader("Postagens por dia")
        df["date"] = pd.to_datetime(df["created_at"]).dt.date
        timeline = df.groupby("date").size().reset_index(name="posts")
        st.line_chart(timeline.set_index("date"))

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
