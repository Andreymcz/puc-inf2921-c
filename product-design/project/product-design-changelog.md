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
