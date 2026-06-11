from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from gavealab_poc.workspace import GaveaLabWorkspace


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("1. Upload de Relatos")
    st.info("Para ver e carregar sessoes anteriores, va para **Todos os Estudos** no menu.")

    # --- New session upload ---
    st.subheader("Nova sessao")
    st.markdown(
        "Faca o upload de um arquivo CSV com os relatos dos cidadaos. "
        "Colunas esperadas: **comment** ou **text** (obrigatoria), "
        "**id** e **territory** (opcionais)."
    )

    session_name = st.text_input(
        "Nome da analise",
        placeholder="Ex.: Gavea 2026 -- rodada 1",
    )

    uploaded = st.file_uploader("Escolha um arquivo CSV", type=["csv"])
    if uploaded is None:
        return

    try:
        preview_df = pd.read_csv(io.BytesIO(uploaded.read()))
        uploaded.seek(0)
    except Exception as exc:
        st.error(f"Erro ao ler CSV: {exc}")
        return

    st.dataframe(preview_df.head(10), use_container_width=True)
    st.caption(f"{len(preview_df)} linhas detectadas.")

    if not session_name.strip():
        st.warning("Digite um nome para a analise antes de continuar.")
        return

    if st.button("Criar sessao de analise"):
        try:
            session = workspace.create_session(session_name.strip(), uploaded)
            st.session_state.session = session
            st.success(
                f"Sessao '{session_name}' criada com {len(session.df)} relatos. "
                "Use o menu lateral para escolher a ferramenta de analise."
            )
        except ValueError as exc:
            st.error(str(exc))
