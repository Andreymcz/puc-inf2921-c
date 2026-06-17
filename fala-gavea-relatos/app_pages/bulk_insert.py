from __future__ import annotations

import pandas as pd
import streamlit as st

from .shared import api_post


def render() -> None:
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
