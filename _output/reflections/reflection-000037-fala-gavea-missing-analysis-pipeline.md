# Reflection 000037 | 2026-06-11 17:42 UTC | fala-gavea: motor de análise ausente

## Artifacts reflected on

- [research-000023](_output/research-logs/research-000023-plataforma-fala-gavea-roadmap.md) — Plataforma Fala Gávea: visão, casos de uso e roadmap
- [roadmap-000026](_output/roadmaps/roadmap-000026-fala-gavea-streamlit-app.md) — Fala Gávea: Streamlit App de Participação Cidadã
- [roadmap-000028](_output/roadmaps/roadmap-000028-fala-gavea-streamlit-frontend.md) — Fala Gávea: Streamlit frontend + backend likes/label_feedback
- [plan-000029](_output/plans/plan-000029-fala-gavea-backend-likes-label-feedback.md) — Backend: likes e label_feedback endpoints
- [plan-000030](_output/plans/plan-000030-fala-gavea-app-streamlit.md) — App Streamlit consumindo API REST
- [plan-000027](_output/plans/plan-000027-fala-gavea-setup-streamlit.md) — Fala Gávea: Project setup — Streamlit + estrutura de pacote
- [plan-000032](_output/plans/plan-000032-fala-gavea-seed-dataset-dashboard-viz.md) — Seed dataset (posts + likes) + dashboard visualizations
- [plan-000033](_output/plans/plan-000033-fala-gavea-like-label-traceability.md) — Like and label traceability
- [plan-000036](_output/plans/plan-000036-fala-gavea-pagination-names-encoding.md) — Posts pagination, citizen names, encoding fix
- [plan-000021](_output/plans/plan-000021-gavealab-poc-all-studies-page-multipage-nav.md) — gavealab-poc: all studies page and modern multipage navigation
- [plan-000020](_output/plans/plan-000020-generate-sample-gavealab-csv.md) — Generate sample-gavealab.csv with 500 and 1000 entries
- [plan-000025](_output/plans/plan-000025.md) — SEJA skill: clean Python project template generator
- [check-000034](_output/check-logs/check-000034-plan-000033-validation.md) — Validation: plan-000033
- [check-000035](_output/check-logs/check-000035-plan-000033-code-review.md) — Code review: plan-000033

## Summary

A semana construiu dois produtos em paralelo:

**gavealab-poc** recebeu uma página de listagem de todas as sessões de análise e navegação multipage modernizada (plan-000021). O motor de análise (tópicos → claims → cruxes → UMAP) está implementado e funcional nesse PoC.

**fala-gavea** saiu do zero e ganhou toda a camada de participação cidadã: backend FastAPI com entidade `CitizenPost`, modelo `LikeModel`, use cases `ToggleLike`/`AddLabelFeedback`, endpoints REST, app Streamlit com 4 páginas (Postagens, Nova Postagem, Validar Labels, Dashboard), seed de 1000 relatos reais com likes simulados, rastreabilidade de quem curtiu cada post, paginação de posts e nomes de cidadãos legíveis. A decisão explícita em plan-000032 foi: "Labelização automática fica para depois."

O research-000023 identificou dois subsistemas: B (Motor de Análise — PoC) e A (Camada de Input — Fala Gávea). A semana implementou A. B existe no PoC mas ainda não foi conectado ao Fala Gávea.

## Reflection

> "no app fala-gavea nao temos: Tópicos, reinvindicações (claims), discordâncias (cruxes) e UMAP para visualização iterativa dos clusters"

O Fala Gávea construiu a camada de coleta e engajamento cidadão (posts, likes, label feedback) mas ainda não tem o motor de análise do gavealab-poc. Há uma assimetria: o gavealab-poc analisa CSVs externos mas não tem plataforma de input; o Fala Gávea tem input cidadão real mas não analisa o que coleta. O próximo passo natural é conectar os dois — trazer tópicos, claims, cruxes e UMAP para dentro do Fala Gávea, operando sobre os posts já coletados em vez de CSVs carregados manualmente.

O fluxo desejado que emergiu da reflexão:
1. Clusterização dos posts via UMAP (visualização interativa das distâncias semânticas)
2. Labels geradas por IA a partir dos clusters (auto-labeling com LLM)
3. Cruxes e claims extraídos dos posts agrupados por tópico

Isso fecha o loop entre a camada de input cidadão e o motor de análise, realizando a arquitetura de dois subsistemas descrita no research-000023.

## Follow-ups

- Como adaptar o pipeline `gavealab_poc/pipeline/` para operar sobre `CitizenPost` em vez de linhas de CSV? Os embeddings precisariam ser computados e armazenados por post.
- O UMAP no gavealab-poc opera sobre claims (pós-extração). No Fala Gávea, faz sentido rodar UMAP diretamente sobre os posts brutos primeiro, e depois refinar com claims?
- A auto-labelização via LLM deve usar os clusters UMAP como entrada (bottom-up) ou a árvore de tópicos do pipeline existente (top-down)?
- Onde armazenar os embeddings dos posts? Uma nova coluna no `CitizenPostModel` (JSON) ou uma tabela separada `PostEmbedding`?
