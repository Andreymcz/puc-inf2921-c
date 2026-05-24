# QA Log — Advisory 000004 | Talk to the City — Local Deployment and Extension for GaveaLab
# 2026-05-23 23:56 UTC

## Brief

Folowing advisory3: Abri o talk to the city (https://talktothe.city/) e achei bem interessante. Quero extrair toda e qualquer informação necessária para rodar o software localmente, sem depender de serviços externos. Se for muito difícil, quero saber se existe a possibilidade de extender o software. Além da interface atual, podemos criar novas ferramentas para os stakeholders do GaveaLab. Repositório: https://github.com/aIObjectives/tttc-light-js

## Q&A Log

### Q1 — Can Talk to the City be run fully locally, and can it be extended for GaveaLab stakeholders?

**Answer:** Yes — feasible at medium effort. The platform is a pnpm monorepo (Next.js + Express.js + pipeline-worker). All five cloud dependencies (Firebase, GCS, Pub/Sub, Redis, OpenAI) have viable local replacements. A community fork (`tttc-light-js-ollama`) already replaces OpenAI with Ollama. Taiwan's Ministry of Digital Affairs runs a self-hosted production instance. The modular pipeline-step architecture supports new tools such as a `kb_qa_enrich` step that calls the kb-qa RAG server.

**Recommended replacement sequence:**
1. Start with Ollama fork (lowest risk)
2. Replace GCS with MinIO (env-var level change)
3. Replace Pub/Sub with BullMQ + local Redis
4. Replace Firebase Auth with Keycloak behind HTTPS (highest complexity, must be done before real citizen data)

**Extension for GaveaLab:** Add a `kb_qa_enrich` pipeline step calling `query_knowledge` MCP tool; custom input adapters for open datasets; new Next.js visualization pages.
