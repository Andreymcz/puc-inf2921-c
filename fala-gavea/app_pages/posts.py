from __future__ import annotations

import streamlit as st

from .shared import POSTS_PER_PAGE, api_get, api_post, citizen_name


def render() -> None:
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
                        api_post(f"/citizen_posts/{post['id']}/likes", {"user_id": st.session_state.user_id})
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
