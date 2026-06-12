from __future__ import annotations

import streamlit as st

from .shared import api_get, api_post


def render() -> None:
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
                                {"label": label, "approved": True, "user_id": st.session_state.user_id},
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
                                {"label": label, "approved": False, "user_id": st.session_state.user_id},
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
