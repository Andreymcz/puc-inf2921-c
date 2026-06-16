# CONCEPTUAL DESIGN CHANGELOG — INF2921-Grupo-C / kb-qa

<!-- maintained-by: Agent (post-skill) -->

> Append-only log of changes to the as-coded conceptual design.
> Format: `YYYY-MM-DD | plan-NNNNNN | section | change summary`

2026-05-24 | - | all | Initial as-coded snapshot created from codebase scan during /design session
2026-06-01 | plan-000008 | §0 | Added GaveaLab PoC sibling project entry (gavealab-poc/ scaffold)
2026-06-02 | plan-000009 | §0 | Updated GaveaLab PoC entry: upload page implemented (CSV upload flow, session creation, previous sessions panel)
2026-06-02 | plan-000010 | §0 | Updated GaveaLab PoC entry: auto-topics page implemented (Ollama LLM pipeline, topic tree generation, SQLite persistence)
2026-06-02 | plan-000011 | §0 | Updated GaveaLab PoC entry: claims extraction pipeline and UI added (pipeline/claims.py, auto_topics.py claims section)
2026-06-02 | plan-000012 | §0 | Updated GaveaLab PoC entry: manual theme categorization tool added (pipeline/manual_categories.py, pages/manual_topics.py)
2026-06-02 | plan-000013 | §0 | Updated GaveaLab PoC entry: divergent opinion detection added (embeddings.py singleton, pipeline/cruxes.py embedding-based crux detection, pages/cruxes.py)
2026-06-02 | plan-000016 | §0 | Updated GaveaLab PoC entry: UMAP 2D cluster visualization added (pipeline/umap_viz.py, pages/umap_viz.py, sidebar page "Visualizar clusters")
2026-06-10 | plan-000021 | §0 | Added all-studies dashboard page (pages/all_sessions.py), modern st.navigation() multipage nav in app.py, GaveaLabWorkspace.get_sessions_summary(), upload page simplified (removed inline session list)
2026-06-11 | plan-000025 | harness | Added /python-scaffold SEJA skill: generates clean-arch Python REST API project (FastAPI + SQLAlchemy + SQLite + Pydantic v2 + pytest, 18 tests). No GaveaLab/kb-qa domain changes.
2026-06-11 | plan-000030 | §0b | Added Fala Gávea Streamlit frontend (fala-gavea/app.py): 4-page app consuming FastAPI backend — Postagens (likes), Nova Postagem, Validar Labels (AI label feedback), Dashboard (metrics + charts)
2026-06-11 | plan-000033 | §0b | Updated Fala Gávea: like traceability (GET /citizen_posts/{id}/likes, LikeRecord domain, GetPostLikes use case), label feedback user attribution (user_id stored in label_feedback JSON), Streamlit "Ver quem curtiu" expander and dashboard traceability tables
2026-06-11 | plan-000032 | §0b | Added fala-gavea/scripts/seed_db.py (1000 posts from sample CSV + ~50k likes), updated Dashboard: avg-likes metric, timeline chart, likes histogram (inf-bound bins)
2026-06-11 | plan-000036 | §0b | Fala Gávea: seed_db.py encoding fixed latin-1→utf-8; added citizen_name() hash-based name mapping; posts page paginated (20/page, prev/next); UUID display replaced with names in posts, likes expander, and dashboard traceability tables
2026-06-11 | plan-000039 | §0b | Fala Gávea: UMAP cluster pipeline added (pipeline/embeddings.py, pipeline/cluster.py, pipeline/label_clusters.py); set_ai_labels use case + POST /citizen_posts/{id}/ai_labels endpoint; "Explorar Clusters" Streamlit page with Plotly scatter + cluster summary table
2026-06-11 | plan-000040 | §0b | Fala Gávea: "Ver quem curtiu" expander now lazy-loads likers via session-state cache; eliminated N+1 API calls on page render (was: up to 20 calls/render; now: 0 calls until user clicks "Carregar curtidas")
2026-06-11 | plan-000041 | §0b | Fala Gávea: cluster view summary table replaced with "Posts por Cluster" expander list — each LLM label is an expander title with post count; lists all posts (Relato/Territorio columns) sorted by count desc, noise last
2026-06-12 | plan-000044 | §0b | Fala Gávea: embed on creation (POST /citizen_posts/ now calls embed_and_store); bulk insert route POST /citizen_posts/bulk (save_many, batched embedding); sentence_transformers import made lazy; test mock_embed autouse fixture
2026-06-12 | plan-000045 | §0b | Fala Gávea: added "Inserção em Massa" Streamlit page (page_bulk_insert) — CSV upload, column validation, territory_level filter, 20-row preview, calls POST /citizen_posts/bulk; page count updated from 5 to 6
2026-06-12 | plan-000043 | §0b | Fala Gávea: refactored app.py monolith into app_pages/ package — shared.py + 6 page modules (posts, new_post, label_feedback, dashboard, clusters, bulk_insert) each exporting render(); app.py now uses st.navigation() + st.Page(); USER_ID global replaced by st.session_state.user_id
2026-06-12 | plan-000047 | §0b | Fala Gávea: build_cluster_df no longer calls embed_and_store — embeddings are now fetched directly via get_embeddings (persisted at post-creation time); spinner text updated to reflect the change
2026-06-15 | plan-000049 | §0b | Fala Gávea: exposed n_neighbors, min_dist, min_cluster_size sliders in clusters page; noise-count hint added when posts land in cluster_id = -1
2026-06-15 | plan-000042 | §0b | Fala Gávea: debug logging added to label_clusters.py (FALA_GAVEA_DEBUG_LLM env var) and gavealab_poc/llm.py (GAVEALAB_DEBUG_LLM env var); silent except fixed to log cluster ID and error; clusters page: auto-label-generation removed from run_btn, per-cluster "🤖 Gerar label com IA" button added in expanders
2026-06-16 | plan-000055 | §0c | Fala Gávea Segurança: iluminação pública overlay added — infrastructure/iluminacao/loader.py (download + cache ArcGIS GeoJSON), GET /iluminacao/geojson + POST /iluminacao/refresh FastAPI endpoints, Leaflet "💡 Luminárias" layer toggle in app.js, refresh button panel in index.html sidebar
2026-06-16 | plan-000057 | §0d | Fala Gávea Segurança: ReportCategory expandido de 4 para 9 valores (furto_roubo, iluminacao, transito, espaco_publico_inseguro, vandalismo, moradores_situacao_rua, conflito_social, barulho_perturbacao, outro) derivados da análise do Fórum de Segurança da Gávea; seed script com 250 relatos pt-BR e distribuição realista; CATEGORIZE_PROMPT template em infrastructure/ai/prompts.py
