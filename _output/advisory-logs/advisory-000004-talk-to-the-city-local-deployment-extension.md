# Advisory 000004 | INF2921 Grupo C | 2026-05-23 23:52 UTC | Talk to the City — Local Deployment and Extension for GaveaLab

tags: local-deployment, civic-tech, llm-integration, architecture, vendor-lock-in

**User brief:** Abri o Talk to the City (https://talktothe.city/) e achei bem interessante. Quero extrair toda e qualquer informação necessária para rodar o software localmente, sem depender de serviços externos. Se for muito difícil, quero saber se existe a possibilidade de extender o software. Além da interface atual, podemos criar novas ferramentas para os stakeholders do GaveaLab. Repositório: https://github.com/aIObjectives/tttc-light-js

**Agent interpretation:** The team wants to (a) run tttc-light-js fully locally with no cloud dependencies, and (b) understand extension possibilities for creating new GaveaLab-specific tools on top of or alongside the platform. This advisory covers deployment feasibility, replacement strategy for each cloud dependency, and integration paths with the existing kb-qa RAG system.

**Files referenced:** GitHub repo (AIObjectives/tttc-light-js), community fork (Diegorb1329/tttc-light-js-ollama), public documentation.

---

## Q&A Log

### Q1 — Can Talk to the City be run fully locally, and can it be extended for GaveaLab stakeholders?

#### Platform Overview

Talk to the City (tttc-light-js) is a **pnpm monorepo** composed of three main applications:

| Package | Tech | Port | Purpose |
|---------|------|------|---------|
| `next-client` | Next.js | 3000 | Interactive visualization frontend |
| `express-server` | Express.js | 8080 | REST API, auth middleware, storage |
| `pipeline-worker` | Node.js | — | LLM-driven analysis pipeline |

Plus shared packages: `common` (types/schemas), `data-utils`, `utils`.

#### External Cloud Dependencies

| Service | Role | Replacement |
|---------|------|-------------|
| **Firebase** | Authentication | Keycloak, Authentik, or local JWT |
| **Google Cloud Storage (GCS)** | Report persistence | MinIO (S3-compatible) or local filesystem |
| **Google Pub/Sub** | Async job queue | BullMQ + local Redis |
| **Redis** | Caching/sessions | Self-hosted Redis (already in docker-compose, commented out) |
| **OpenAI API** | LLM inference | Ollama (community fork exists) |

#### Local Deployment Feasibility: **MEDIUM effort, fully achievable**

There is a community fork (`tttc-light-js-ollama` by Diegorb1329, Apache 2.0) that already replaces OpenAI with Ollama, proving the LLM substitution path. Taiwan's Ministry of Digital Affairs deployed a self-hosted production instance — real-world precedent that the architecture supports full self-hosting.

**Recommended replacement sequence (by risk/effort):**

1. **Start with Ollama fork** — validates the end-to-end pipeline without cloud LLM. Lowest risk.
2. **Replace GCS with MinIO** — S3-compatible, so only endpoint/credential env-vars change. The GCS SDK calls can typically be rewired with minimal code changes.
3. **Replace Pub/Sub with BullMQ** — Redis is already present in the docker-compose (commented out); BullMQ uses Redis as its backend.
4. **Replace Firebase Auth with Keycloak** — highest complexity. Requires JWKS endpoint wiring into the Express API, HTTPS termination, and secret rotation. Must be done before handling any real citizen data.

**Docker Compose strategy:** Create a `docker-compose.gavealab.yml` override file that layers GaveaLab-specific services (MinIO, Keycloak, Ollama) on top of the upstream compose, keeping the upstream diff minimal for easier rebasing.

#### Extension Possibilities for GaveaLab

The pipeline worker uses a **modular step-based architecture** — each analysis step is a composable function. This is the primary extension point:

- **`kb_qa_enrich` step** — Call `query_knowledge` (from the kb-qa MCP server) before or after LLM clustering to inject context from GaveaLab's document corpus (policy papers, prior research). Effort: Low–Medium.
- **Custom input adapters** — Feed data from GaveaLab's open datasets (IBGE, Rio Prefeitura APIs) directly into the pipeline instead of only manual uploads.
- **New visualization pages** — The Next.js frontend can host additional pages (e.g., geographic clustering maps relevant to GaveaLab's Amazônia and Gávea contexts).
- **REST API integration** — The Express server can expose new endpoints for external tools or dashboards.

#### Expert Perspective Summary

| Perspective | Finding |
|-------------|---------|
| **Architecture** | Modular design supports all planned substitutions; Ollama fork de-risks LLM swap |
| **Operations** | Docker Compose grows to ~6 services (MinIO, Keycloak, Ollama + originals); manageable |
| **Security** | Firebase Auth replacement is the highest-risk step; must use HTTPS + proper JWKS wiring before any real citizen data flows |
| **Data** | Local deployment improves data sovereignty for civic/participatory data — aligned with GaveaLab's mission |
| **Developer Experience** | Shared `common` package and existing Ollama fork make extension straightforward for the team |

#### Key Trade-offs

- **Security vs. Effort:** Keycloak setup is the most complex sub-task. Acceptable to skip auth only for a fully air-gapped demo with synthetic data — never with real GaveaLab participant data.
- **Fork maintenance vs. Vendor lock-in:** Prefer env-var and Docker Compose-level swaps over code patches to keep the upstream diff small and rebasing tractable.

---

## Recommendations Summary

| Priority | Recommendation |
|----------|---------------|
| HIGH | Start with the Ollama fork (`tttc-light-js-ollama`) and validate end-to-end pipeline locally before touching auth or storage |
| HIGH | Replace Firebase Auth with Keycloak behind HTTPS; wire JWKS validation into Express API before processing real citizen data |
| MEDIUM | Replace GCS with MinIO and Pub/Sub with BullMQ — add both to a `docker-compose.gavealab.yml` override file |
| MEDIUM | Add a `kb_qa_enrich` pipeline step that calls the kb-qa `query_knowledge` MCP tool to enrich LLM summarization with GaveaLab's document corpus |
| LOW | Document the compose override pattern and maintain a thin diff from upstream for easier future rebasing |
