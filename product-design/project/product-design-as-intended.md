# DESIGN INTENT — INF2921-Grupo-C / GaveaLab

<!-- maintained-by: human (designer); Human (markers) classification since SEJA 2.8.3 -->

> **Classification**: `Human (markers)` — prose is human-authored only. Agents may write `STATUS` markers on §1-§17 sections, §15 JM-TB-NNN journey entries, and `### D-NNN:` Decision entries via `apply_marker.py` after AskUserQuestion confirmation. Agents may also append lines to the `## CHANGELOG` section.

---

## 0. Planned Changes

> **gavealab-poc** is the primary product. kb-qa remains in the repository as a supporting RAG tool for document retrieval during AI sessions, but new feature development is focused on gavealab-poc.

### gavealab-poc

| Target Version | Change Summary | Motivation / Rationale |
|---|---|---|
| current | UMAP 2D cluster visualization of claim embeddings (Plotly) | Help users see how opinions cluster spatially across topics |
| next | Export analysis results to CSV/JSON | Allow researchers to share or archive results outside the app |
| next | Filter clusters by topic or territory in UMAP view | Make cluster view actionable for geographic or thematic drill-down |
| future | Multi-session comparison view | Compare analysis across different datasets or time periods |

### kb-qa (supporting tool — maintenance only)

| Target Version | Change Summary | Motivation / Rationale |
|---|---|---|
| v0.2 | Expose similarity scores in `ask` command output | Give users confidence signals |
| v0.3 | LLM answer synthesis in CLI (`ask --synthesize`) | Provide direct answers via Claude, not just raw chunks |

---

## 1. Platform Purpose

GaveaLab is a local citizen feedback analysis tool designed as the capstone product for the INF2921/CIS2114 AI Systems Design course at PUC-Rio (2026.1). It enables researchers, civic organizations, and course teams to upload CSV datasets of citizen relatos (open-ended survey responses or public consultation comments) and analyze them through LLM-powered pipelines — without sending data to any cloud service.

The core problem it solves: when civic researchers or labs collect hundreds of qualitative comments from citizens, there is no lightweight tool that can automatically identify discussion topics, extract the key claims within each topic, surface points of genuine disagreement (cruxes), and visualize how opinions cluster spatially. Existing tools (Talk to the City, Polis) are complex to deploy or require cloud infrastructure. GaveaLab provides the same analytical power as a self-contained local Streamlit application.

The project is inspired by the [Talk to the City](https://github.com/AIObjectives/talk-to-the-city-reports) methodology and a local PoC (`tttc-poc/`) developed by the team. GaveaLab simplifies and extends that approach with a more accessible UI, persistent analysis sessions, and UMAP-based cluster visualization.

### Design Philosophy

Accessible local AI for civic research. Citizen data never leaves the analyst's machine. The system guides the user through a structured analysis pipeline — upload → topics → claims → divergence → visualization — but allows manual overrides at each step. Simplicity over configurability: sensible LLM defaults, single-click analysis steps, and immediate visual feedback enable researchers who are not engineers to use the tool effectively.

### Role of kb-qa

kb-qa (`src/kb_qa/`, `agents/`) continues to function as a supporting RAG tool. It is used by the team to query course documents (lecture notes, papers) via the MCP integration in Claude Code sessions. It is not the primary product of the course deliverable and receives maintenance-only updates.

---

## 2. Entity Hierarchy

### GaveaLab (primary product)

```
AnalysisSession        (one uploaded CSV dataset + all derived results)
├── Comment            (one row from the CSV — the atomic input unit)
├── TopicTree          (LLM-generated hierarchy of topics and subtopics)
│   └── Topic          (a discovered or user-defined discussion topic)
│       └── Claim      (a distilled statement extracted from Comments under a Topic)
│           └── Crux   (a pair or group of Claims that represent a point of divergence)
└── ClusterMap         (UMAP 2D projection of Claim embeddings for visualization)
```

### AnalysisSession

Created when the user uploads a CSV file. Persisted in SQLite (`gavealab.db`) via `GaveaLabWorkspace`. Holds the raw CSV and all derived results as JSON blobs (`topic_tree`, `claims_tree`, `cruxes`, `manual_categories`). Sessions are independent — re-uploading a file creates a new session; old sessions remain accessible. Identified by an auto-incremented integer ID.

### Comment

One row from the uploaded CSV. Required column: `text` (or `comment`, normalized on load). Optional columns: `id` (auto-generated if absent), `territory`, and any additional metadata columns kept as-is. Comments shorter than 10 characters are dropped at load time. Identified by the `id` string value.

### Topic

A discussion theme. Either LLM-generated (auto-topics pipeline) or user-defined (manual categorization). Each topic may have subtopics (nested structure from the LLM). Topics group Comments for downstream analysis.

### Claim

A distilled, third-person statement representing a point made by one or more Comments within a Topic. Extracted by the LLM claims pipeline. Each Claim has: `claim` (statement text), `quote` (supporting excerpt from the original comment), `comment_id`, `topic`, `subtopic`. Claims are the core unit of analysis.

### Crux

A point of genuine disagreement between Claims within the same Topic. Identified by the LLM cruxes pipeline. Each Crux describes the two opposing positions and cites the Claims supporting each side.

### ClusterMap

A 2D UMAP projection of Claim embeddings (computed via `nomic-ai/nomic-embed-text-v1`). Stored as coordinate arrays associated with the session. Used by the visualization page to render an interactive Plotly scatter plot where spatial proximity indicates semantic similarity.

---

### kb-qa (supporting tool)

```
KnowledgeDocument  (.md or .pdf file in knowledge/)
└── Chunk          (text segment extracted during ingestion)
    └── Embedding  (vector stored in VectorStore collection)

VectorStore        (ChromaDB persistent collection — holds all Chunks)
```

See historical design intent for entity details. kb-qa entity model is stable and not the focus of current development.

---

## 3. Domain-Specific Concepts

### GaveaLab

**Relato**: A citizen's open-ended response to a public consultation or survey question. The raw input material. Stored as a `Comment` in the system.

**LLM pipeline**: A sequential chain of stateless LLM calls that transforms Comments into increasingly structured insight: auto-topics (topic tree discovery) → claims extraction (distilled statements per topic) → cruxes detection (points of divergence). Each step is independently re-runnable.

**Topic tree**: A two-level hierarchy (topic → subtopic) generated by the LLM from the full comment corpus. Represents the major discussion themes found in the dataset. Can be replaced by a user-defined flat list of themes (manual categorization mode).

**Claim**: A compressed, third-person statement of a point made in one or more comments. Retains a supporting quote and link back to the original comment ID. Claims are the smallest unit that carries interpretive meaning.

**Crux**: A point of genuine disagreement between two or more Claims on the same topic. Not merely different opinions — a crux is a statement where understanding whether it is true would change people's minds. Concept borrowed from the rationalist tradition and the Talk to the City methodology.

**UMAP projection**: A 2D dimensionality reduction of Claim embeddings using UMAP (Uniform Manifold Approximation and Projection). Enables visual inspection of how opinion clusters relate spatially. Spatial proximity indicates semantic similarity; clusters that appear near each other are discussing related ideas.

**Ollama**: Local LLM inference server running at `http://localhost:11434`. Default model: `qwen3:8b` (configurable via `GAVEALAB_OLLAMA_MODEL`). All LLM calls use the OpenAI-compatible `/v1/chat/completions` endpoint.

### kb-qa (supporting tool)

**Content-addressable chunking**: Each Chunk is identified by an MD5 hash of its source path + first 200 characters of text. Enables incremental ingestion.

**MCP tool boundary**: `query_knowledge` (FastMCP) is the only external surface — accepts a question string, returns relevant chunks. Stateless per call.

---

## 4. Permission Model

<!-- REQ-PERM-001 -->

### System-Level Roles

| Role | Level | Capabilities |
|------|-------|-------------|
| Local user | — | Full access: ingest, status, ask, MCP query |

No authentication, no roles, no access control. The system is designed for single-user local deployment. Anyone with filesystem access to the repository can use all features.

### Resource-Level Access

Not applicable. There is one shared collection and no per-user or per-document scoping.

**Rationale**: The tool is a local research aid, not a multi-tenant service. Adding auth would add friction with no privacy benefit since the filesystem is already the access control layer.

---

## 5. Content Authoring & Attribution

Not applicable. kb-qa does not support user-generated content authoring. Documents are authored externally and placed in `knowledge/` by the user. Authorship is tracked by the filesystem (file owner, modification time). No mention/notification system.

---

## 6. Content Import & Export

### Import Formats

| Format | Source | Notes |
|--------|--------|-------|
| `.md` | Local filesystem | Full document; split into chunks by paragraph/section |
| `.pdf` | Local filesystem | Text extracted via pymupdf; images and tables are not currently indexed |

### Export Formats

Not supported. The vector store is a local derived index; no export functionality is designed.

---

## 7. User Community & Localization

### Target Community

Graduate students and researchers in the INF2921/CIS2114 AI Systems Design course (PUC-Rio, 2026.1). Team members: Andrey, Mauro, Julia, Herbert, Natali. Primary use case: analyzing pt-BR civic consultation datasets (relatos de cidadãos) from organizations such as GaveaLab. Domain expertise: AI/ML research and software engineering.

### Localization Design

| Aspect | Primary | Secondary |
|--------|---------|-----------|
<!-- REQ-I18N-001 -->
| UI language | pt-BR (Streamlit labels, sidebar navigation, page titles) | — |
| LLM prompt language | pt-BR (all system and user prompts in gavealab_poc/pipeline/) | en-US (fallback) |
| Code and comments | en-US | — |
| Backend error messages | en-US | — |

The Streamlit UI and all LLM prompts are in pt-BR to match the target dataset language and the user's native language. The embedding model (`nomic-ai/nomic-embed-text-v1`) handles multilingual content without additional configuration.

---

## 8. User Experience Patterns (Domain-Driven)

<!-- REQ-UX-001 -->

### GaveaLab

**Upload-then-analyze workflow**: The user uploads a CSV file on the "Upload CSV" page, naming the analysis session. The session is persisted immediately. All subsequent pages operate on the active session selected from the sidebar. The upload step is a one-time operation per dataset; analysis steps can be re-run independently.

**Sequential pipeline with manual override**: The natural flow is upload → auto-topics → claims → cruxes → visualization. However, the user may skip auto-topics and proceed directly to manual topic categorization if they already know the topic structure. Each pipeline step writes its results to the SQLite session and makes them available to downstream steps.

**Idempotent re-runs**: Each analysis page shows a "Re-run" button that discards and replaces the previous result for that step. Results are stored per session and per result type; re-running one step does not affect others.

**Session persistence across page navigations**: Streamlit's `st.session_state` holds the current `AnalysisSession` reference. The Streamlit app caches the `GaveaLabWorkspace` singleton. Navigating between pages does not lose analysis results — they are reloaded from SQLite on session resume.

**UMAP visualization as insight layer**: The cluster map page is not a pipeline step — it is a read-only visualization of Claims already computed. It provides spatial context: comments that generated semantically similar claims appear near each other, regardless of topic assignment.

**Progressive disclosure of complexity**: Simple actions (upload, run auto-topics) require one click. Advanced actions (manual category definition, crux inspection) are on dedicated pages. The sidebar navigation reflects the natural analysis flow.

### kb-qa (supporting tool)

**Ingest-then-query**: Documents placed in `knowledge/`, run `kb-qa ingest`, then query via CLI or MCP. Decoupled from the gavealab-poc analysis flow.

---

## 9. Administrative Domain

### Activity Logging

No structured activity logging. Standard Python `logging` module at INFO level is used during ingestion for progress reporting. No audit log required for a single-user local tool.

### Backup & Restore

The vector store at `knowledge/vectorstore/` can be deleted and rebuilt at any time by running `kb-qa ingest`. No backup process required — the source documents in `knowledge/` are the authoritative data.

### Terms & Conditions

Not applicable. Internal academic project.

---

## 10. Validation Constants (Domain)

<!-- REQ-VAL-001 -->

### GaveaLab

| Constant | Value | Domain Rationale |
|----------|-------|-----------------|
| Minimum comment length | 10 chars | Drops noise entries (single words, punctuation-only) |
| Default LLM model | `qwen3:8b` | Good quality/speed balance for local inference; configurable via `GAVEALAB_OLLAMA_MODEL` |
| Ollama base URL | `http://localhost:11434/v1` | Local inference; configurable via `GAVEALAB_OLLAMA_URL` |
| UMAP `n_components` | 2 | 2D projection for Plotly scatter visualization |
| UMAP `n_neighbors` | 15 | Default UMAP parameter; controls local vs. global structure balance |

### kb-qa (supporting tool)

| Constant | Value | Domain Rationale |
|----------|-------|-----------------|
| `n_results` max | 20 | Prevents excessive token usage in MCP consumers |
| `EMBED_BATCH_SIZE` | 256 | Balance between GPU/CPU memory and throughput |

Constants defined in `src/kb_qa/constants.py`.

---

# Part II — Metacommunication

## 11. Global Metacommunication Vision

<!-- REQ-MC-001 -->

I know you are a civic researcher or graduate student who collects qualitative feedback from citizens — open-ended survey responses, public consultation comments, neighborhood meeting notes — and struggles to make sense of hundreds of individual voices without losing the nuance in each one. Therefore, I have designed GaveaLab: a local tool that lets you upload your dataset, discover the discussion topics your citizens actually raised, extract the key claims within each topic, surface the points where citizens genuinely disagree, and see how opinions cluster visually — all running on your own machine, without sending citizen data to any cloud service.

*Updated by the design agent on 2026-06-02 to reflect the project's evolution from RAG tool (kb-qa) to GaveaLab citizen feedback analysis as the primary course deliverable.*

---

## 12. Extended Metacommunication Template Guiding Questions

1. Analysis (understanding needs and defining requirements)
   1.1. What do I know or don't know about (all of) you and how?
   I know you are a graduate student or researcher at PUC-Rio (INF2921/CIS2114 team), working on a capstone project for an AI Systems Design course. I know you want to demonstrate the application of LLM pipelines to a real civic problem — analyzing citizen relatos. I know your team has already built a tttc-poc (local Talk to the City adaptation) and iterated through several plan cycles toward a full Streamlit product. I do not know the exact size or sensitivity of the citizen datasets you plan to analyze in the course demonstration.
   > For detailed persona profiles and problem scenarios, see `project/ux-research-results.md §1-§4`.
   1.2. What do I know or don't know about affected others and how?
   The citizen data (relatos) represents real people's opinions and concerns. I know the team handles this data locally (no cloud upload). I do not know whether the datasets come from real public consultations or are synthetic for course purposes.
   1.3. What do I know or don't know about the intended (and other anticipated) contexts of use?
   Intended: course demonstration of an AI-powered civic tech tool; analysis of pt-BR citizen feedback datasets; GaveaLab organization use case. Anticipated extension: adapting the tool for other public consultation contexts beyond the course.
   1.4. *What ethical questions can be raised by what I have learned? Why?
   (1) Citizen relatos may contain personally identifiable information or sensitive opinions. Local-only processing mitigates external exposure, but the team should ensure datasets are anonymized or appropriately consented. (2) LLM-generated claims and cruxes may misrepresent or flatten nuanced opinions — the tool should always allow the analyst to inspect and override LLM outputs. (3) The clustering visualization may create an illusion of consensus or disagreement that is an artifact of the embedding model, not a reflection of reality.

2. Design
   2.1. What have I designed for you?
   A local Streamlit web application for structured analysis of citizen feedback datasets. Five analysis pages: CSV upload, auto topic discovery, manual topic categorization, divergence detection (cruxes), and UMAP cluster visualization. All LLM calls run through a local Ollama server.
   2.2. Which of your goals have I designed the system to support?
   (1) Transform a raw CSV of citizen comments into structured insight (topics → claims → cruxes) without manual coding. (2) Visualize semantic clustering of opinions to support qualitative analysis. (3) Keep citizen data local — no cloud upload. (4) Demonstrate LLM pipeline design as a course deliverable.
   2.3. In what situations/contexts do I intend/accept you will use the system to achieve each goal? Why?
   During course demonstrations and development iterations. For analyzing pt-BR civic consultation datasets (real or synthetic). As a local research tool for the GaveaLab organization use case.
   > For detailed solution representations, see Section 13 below.
   2.4. How should you use the system to achieve each goal, according to my design?
   Upload a CSV with a `text` (or `comment`) column. Run auto-topics to let the LLM discover discussion themes. Review and optionally override topics. Run claims to extract distilled statements per topic. Run cruxes to surface disagreements. Navigate to the cluster view to inspect spatial opinion patterns.
   2.5. For what purposes do I not want you to use the system?
   As a replacement for rigorous qualitative research methodology — LLM outputs are a starting point for analysis, not a final result. As a real-time or multi-user platform (the PoC is single-user local). As a tool for making policy decisions without human review of LLM-generated claims and cruxes.
   2.6. *What ethical principles influenced my design decisions?
   Data sovereignty: citizen data stays on the analyst's machine. Human oversight: every LLM output is displayed for review before being treated as a result. Transparency: the LLM model and prompts are configurable and inspectable.
   2.7. *How is the system I designed for you aligned with those ethical considerations?
   SQLite stores all data locally. The Streamlit UI shows all LLM outputs inline — no hidden processing. The Ollama model is configurable via env var so the analyst controls which model processes their data.

3. Prototyping, implementation, and formative evaluation
   3.1. How have I built the system to support my design vision?
   Python 3.13 + Streamlit + SQLite (GaveaLabWorkspace) + Ollama (OpenAI-compatible API, qwen3:8b) + sentence-transformers (nomic-embed-text-v1) + UMAP + Plotly. All compute runs locally.
   3.2. What have I built into the system to prevent undesirable uses and consequences?
   Minimum comment length filter (10 chars). No write endpoints exposed externally. LLM outputs stored per session and always reviewable. No auto-send to external services.
   3.3. What have I built into the system to help identify and remedy unanticipated negative effects?
   All pipeline results are displayed in the UI for human review. Sessions are persistent — the analyst can return to previous results. Re-run buttons allow regenerating any step if the output is unsatisfactory.
   3.4. *What ethical scenarios have I used to evaluate the system?
   (1) A dataset contains PII — mitigated by local-only storage; analyst is responsible for dataset anonymization. (2) LLM produces a biased or incorrect topic tree — mitigated by manual categorization mode as an alternative. (3) UMAP projection creates misleading clusters — the visualization includes claim text on hover so the analyst can verify cluster content directly.

4. Continuous, post-deployment evaluation and monitoring
   4.1. How much of my vision is reflected in the system's actual use?
   To be evaluated after the course demonstration with the GaveaLab dataset.
   4.2. What unanticipated uses have been made? By whom? Why?
   TBD — active development.
   4.3. What anticipated and unanticipated effects have resulted from its use? Whom do they affect? Why?
   TBD.
   4.4. *What ethical issues need to be handled through system redesign, redevelopment, policy, or even decommissioning?
   TBD.

---

## 13. Solution Representations

### GaveaLab User Stories

#### US-GL-001: Analisar relatos de cidadãos a partir de um CSV

- **Story:** Como pesquisadora do GaveaLab, quero fazer upload de um CSV com relatos de cidadãos e obter uma análise estruturada dos temas discutidos, para que eu possa entender rapidamente os principais pontos levantados sem ler cada comentário individualmente.
- **Acceptance Criteria:**
  - A página "Upload CSV" aceita arquivos com coluna `text` ou `comment`
  - A sessão é nomeada pelo usuário e persiste no banco SQLite
  - Após o upload, a página exibe quantos comentários foram carregados
  - Sessões anteriores são acessíveis via seletor na sidebar

#### US-GL-002: Descobrir temas automaticamente com LLM

- **Story:** Como pesquisador, quero que o sistema identifique automaticamente os temas discutidos nos relatos, para que eu não precise fazer codificação temática manual.
- **Acceptance Criteria:**
  - A página "Temas automáticos" gera uma árvore de tópicos/subtópicos via LLM
  - O resultado é exibido na UI para revisão antes de ser salvo
  - O botão "Re-run" permite regerar os temas se o resultado não for satisfatório
  - O resultado é salvo na sessão e fica disponível para os passos seguintes

#### US-GL-003: Categorizar comentários por temas manuais

- **Story:** Como pesquisadora, quero definir meus próprios temas e pedir ao sistema que categorize cada comentário, para que eu possa aplicar uma taxonomia de análise existente.
- **Acceptance Criteria:**
  - A página "Categorizar por temas" aceita uma lista de temas digitados pelo usuário
  - O LLM atribui cada comentário ao tema mais relevante
  - O resultado mostra a distribuição de comentários por tema

#### US-GL-004: Identificar pontos de divergência (cruxes)

- **Story:** Como pesquisador, quero ver onde os cidadãos genuinamente discordam, para que eu possa identificar as questões mais controversas da consulta.
- **Acceptance Criteria:**
  - A página "Opiniões divergentes" exibe cruxes identificados pelo LLM
  - Cada crux apresenta as duas posições opostas e cita os claims que as sustentam
  - O resultado é vinculado às claims já extraídas na sessão

#### US-GL-005: Visualizar clusters de opiniões

- **Story:** Como pesquisadora, quero ver um mapa visual de como as opiniões se agrupam semanticamente, para que eu possa identificar padrões que não aparecem na análise textual.
- **Acceptance Criteria:**
  - A página "Visualizar clusters" exibe um scatter plot 2D (Plotly) das claims embedadas via UMAP
  - Cada ponto mostra o texto da claim e o tópico ao passar o mouse
  - Pontos são coloridos por tópico para facilitar a leitura

### kb-qa User Stories (supporting tool — stable)

#### US-KQ-001: Ingerir materiais de curso

- **Story:** As a course team member, I want to ingest my lecture PDFs and notes so that I can query them through Claude without copy-pasting.
- **Acceptance Criteria:**
  - `kb-qa ingest` processes all `.md` and `.pdf` files in `knowledge/`
  - Re-running on unchanged files does not duplicate chunks
  - Progress is visible via a progress bar

#### US-KQ-002: Consultar base de conhecimento via MCP

- **Story:** As a researcher, I want Claude to automatically retrieve relevant chunks from my knowledge base so that its answers are grounded in my own documents.
- **Acceptance Criteria:**
  - MCP server configured in `.claude/settings.json`; Claude calls `query_knowledge` and receives relevant chunks with `text`, `type`, `name`, `source`

---

## 14. Per-Feature Metacommunication Intentions

| Feature / Flow | Designer Intent | Priority | Source | Last Synced |
|---|---|---|---|---|
<!-- REQ-MC-002 -->
| CSV upload + session persistence | I have designed upload to create a persistent session immediately so that you can always return to a previous analysis without re-uploading your data | P0 | human | 2026-06-02 00:00 UTC |
| Auto topic discovery | I have designed auto-topics as a starting point, not a final answer — you can re-run, override, or replace it with manual categorization so that the LLM's topic structure never locks you in | P0 | human | 2026-06-02 00:00 UTC |
| Claims extraction | I have designed claims as the core analysis unit so that you are reasoning about distilled statements, not raw noisy text — but every claim retains a quote link back to the original comment | P0 | human | 2026-06-02 00:00 UTC |
| Cruxes detection | I have designed cruxes detection to identify genuine disagreement, not just different opinions, so that you can focus facilitation or policy attention on the points that actually divide people | P1 | human | 2026-06-02 00:00 UTC |
| UMAP cluster visualization | I have designed the cluster view as an exploratory layer — it shows you spatial patterns across all claims, not a conclusion — so that you can discover themes that cut across the LLM's topic assignments | P1 | human | 2026-06-02 00:00 UTC |
| Manual topic categorization | I have designed manual categorization as a parallel path to auto-topics so that analysts who already have a coding framework can apply it without being overridden by the LLM | P1 | human | 2026-06-02 00:00 UTC |
| Document ingestion (kb-qa ingest) | I have designed ingestion to be incremental and idempotent so that you can add documents at any time without disrupting the existing index | P2 (maintenance) | human | 2026-05-24 00:00 UTC |
| MCP integration (kb-qa) | I have designed the MCP server as a passthrough so that any AI tool can call query_knowledge and receive grounded context from your documents without any modification to your workflow | P2 (maintenance) | human | 2026-05-24 00:00 UTC |

---

## 15. Designed User Journeys

<!-- REQ-JM-001 -->
### JM-TB-001: First-time document ingestion and MCP query

- **Persona:** R-P-001 (Course team member)
- **Goal:** Index course materials and use them in a Claude session
- **Pre-conditions:** Repository cloned; `uv sync` run; documents placed in `knowledge/`

#### Steps

| # | Action | Touchpoint | User Emotion | Pain Point | Opportunity |
| - | ------ | ---------- | ------------ | ---------- | ----------- |
| 1 | Run `kb-qa ingest` | CLI | Curious | First run downloads the embedding model (~274MB) — takes a few minutes with no explicit progress feedback | Show model download progress |
| 2 | Watch progress bar as chunks are embedded | CLI | Satisfied | None | — |
| 3 | Run `kb-qa status` to confirm chunks indexed | CLI | Confident | — | — |
| 4 | Open Claude Code; ask a question about a document topic | Claude Code (MCP) | Satisfied | Must have run MCP server separately; no auto-start | Auto-start MCP server from Claude Code settings |
| 5 | Claude calls `query_knowledge` and receives relevant chunks | MCP tool result | Delighted | Response is raw chunks — Claude must synthesize | Add synthesize option to reduce raw chunk noise |

#### Post-conditions / Outcomes

User has a working local knowledge base integrated with Claude. Future ingestions are fast (incremental). MCP tool is available in all Claude sessions where the server is configured.

---

### JM-TB-002: Análise completa de relatos de cidadãos com GaveaLab

- **Persona:** R-P-GL-001 (Pesquisadora civic tech / GaveaLab)
- **Goal:** Transformar um CSV bruto de relatos em insight estruturado: temas → claims → cruxes → visualização
- **Pre-conditions:** `streamlit run gavealab-poc/app.py` rodando; Ollama com `qwen3:8b` disponível em `localhost:11434`

#### Steps

| # | Action | Touchpoint | User Emotion | Pain Point | Opportunity |
| - | ------ | ---------- | ------------ | ---------- | ----------- |
| 1 | Abre o app no browser; vê sidebar com as 5 páginas | Streamlit UI | Orientada | Nenhuma — navegação clara | — |
| 2 | Vai para "Upload CSV"; nomeia a sessão e faz upload do arquivo | Página Upload | Confiante | Nenhuma — feedback imediato de quantos comentários foram carregados | Mostrar prévia das primeiras linhas |
| 3 | Vai para "Temas automáticos"; clica em "Gerar temas" | Página Auto-topics | Curiosa | LLM demora ~30s para datasets grandes; sem barra de progresso | Mostrar spinner com mensagem de progresso |
| 4 | Revisa a árvore de tópicos gerada; decide aceitar | Página Auto-topics | Satisfeita | Tópicos ocasionalmente muito genéricos | Botão "Re-run" com prompt personalizado |
| 5 | Vai para "Visualizar clusters"; explora o scatter plot 2D | Página UMAP | Deleitada | Primeiro run calcula embeddings — pode ser lento | Cache de embeddings por sessão |
| 6 | Hover sobre pontos no mapa; identifica um cluster de reclamações sobre transporte | Plotly scatter | Insightful | — | Filtro por tópico diretamente no gráfico |
| 7 | Vai para "Opiniões divergentes"; lê os cruxes identificados | Página Cruxes | Reflexiva | Cruxes às vezes repetem o que foi dito, não o ponto de conflito real | Melhorar prompt de cruxes com exemplos few-shot |

#### Post-conditions / Outcomes

Pesquisadora tem uma análise completa da consulta: temas identificados, claims organizados por tema, pontos de divergência explicitados, e mapa visual de clusters. Pode voltar à sessão a qualquer momento sem re-processar.

---

# Part III — Delta from As-Coded

## 16. Conceptual Design Delta

### New (in as-intended but not in as-coded)

| Section | Element | Description |
|---|---|---|
<!-- REQ-DELTA-001 -->
| §0 | Export analysis results | CSV/JSON export not yet implemented |
| §0 | Filter by topic/territory in UMAP | Cluster view filter not yet implemented |
| §13 | US-GL-004 | Cruxes page implemented but full divergence quality needs improvement (see JM-TB-002 step 7) |

### Changed (differs between as-coded and as-intended)

| Section | Element | As-Coded | As-Intended |
|---|---|---|---|
| §1 | Primary product | kb-qa (RAG tool) was original product | GaveaLab is the primary course deliverable |

### Removed (in as-coded but not in as-intended)

| Section | Element | Reason for Removal |
|---|---|---|
| — | — | — |

---

## 17. Metacommunication Delta

### New Intentions (not yet implemented)

| Feature / Flow | Designer Intent | Priority |
|---|---|---|
| Export results (CSV/JSON) | Allow researchers to share or archive session results outside the app | P1 |
| UMAP topic filter | Filter cluster view by topic to focus spatial analysis | P1 |
| Progress indicators for LLM steps | Show spinner + estimated time for auto-topics and claims steps | P1 |
| Score visibility in kb-qa ask output | Show cosine distance alongside each result chunk | P2 |
| LLM synthesis in kb-qa ask command | Offer `--synthesize` flag to call Claude and return a direct answer | P3 |

### Changed Intentions (implementation differs from intent)

| Feature / Flow | As-Coded | As-Intended | Priority |
|---|---|---|---|
| — | — | — | — |

### Deprecated Intentions (implemented but no longer desired)

| Feature / Flow | Current Implementation | Reason for Deprecation |
|---|---|---|
| — | — | — |

---

## Decisions

> Validated decisions with preserved rationale.

<!-- STATUS: proposed -->
### D-001: Use ChromaDB as the vector store

**Context**: For a local RAG tool with a small-to-medium knowledge base (hundreds to low thousands of documents), several vector stores are viable: ChromaDB (local, embedded), Qdrant (local or remote), FAISS (library only), pgvector (PostgreSQL extension). The course project needs something that runs entirely locally with minimal setup.

**Decision**: We use ChromaDB with `PersistentClient` as the vector store. It runs embedded (no server process), persists to a local directory, and requires no additional infrastructure.

**Consequences**: Fast setup and zero ops overhead. Not suitable for multi-host or high-concurrency scenarios. ChromaDB's API is stable for our use case (cosine similarity over a single collection).

---

<!-- STATUS: proposed -->
### D-002: Expose retrieval via MCP (FastMCP)

**Context**: The primary use case is injecting knowledge base results into AI sessions (Claude Code, Copilot). Two integration options: MCP tool (model-controlled, composable) or a REST API (user-controlled, more flexible). MCP is the emerging standard for tool integration with Claude.

**Decision**: Expose `query_knowledge` as an MCP tool via FastMCP. The CLI (`kb-qa ask`) remains available for direct use.

**Consequences**: Works out-of-the-box with Claude Code via settings.json configuration. Requires the MCP server to be running. Composable with future MCP consumers.

---

<!-- STATUS: proposed -->
### D-003: Use nomic-ai/nomic-embed-text-v1 as the embedding model

**Context**: Several open embedding models are available via sentence-transformers. Key criteria: multilingual support (pt-BR + en-US documents), strong semantic quality, permissive license, reasonable model size.

**Decision**: Use `nomic-ai/nomic-embed-text-v1`. Produces high-quality multilingual embeddings, is MIT-licensed, and runs locally via sentence-transformers.

**Consequences**: First run requires downloading ~274MB. Inference runs on CPU (or GPU if available). Model upgrades require reingesting all documents (new embeddings are not backward-compatible with old ones).

---

### D-004: Use Streamlit + SQLite for the GaveaLab frontend and persistence layer

**Context**: The primary product (gavealab-poc) needs a lightweight web UI for a local, single-user analysis tool. Options considered: FastAPI + React (too much overhead for a course PoC), Gradio (limited multi-page support), Streamlit (native Python, multi-page, easy session state, fast to iterate).

**Decision**: Use Streamlit for the UI and SQLite (via Python's built-in `sqlite3`) for session persistence. No ORM — direct SQL via `GaveaLabWorkspace` which owns all DB access.

**Consequences**: Zero infrastructure overhead. Streamlit's session state model requires care around `@st.cache_resource` for the workspace singleton. SQLite limits concurrent write access, acceptable for single-user local deployment. Streamlit's rerun-on-interaction model makes progress feedback for long LLM calls require explicit spinners.

---

### D-005: Use Ollama as the LLM backend for GaveaLab

**Context**: The LLM pipeline (topics, claims, cruxes) needs a local inference server. Options: Ollama (simple API, many models, OpenAI-compatible), llama.cpp (lower-level), cloud API (violates privacy principle). The tttc-poc already used Ollama successfully.

**Decision**: Use Ollama at `http://localhost:11434/v1` with the OpenAI-compatible endpoint. Default model: `qwen3:8b`. Model is configurable via `GAVEALAB_OLLAMA_MODEL` env var.

**Consequences**: Requires Ollama to be running as a separate process. Model download is a one-time operation. `qwen3:8b` provides good quality/speed balance on CPU; teams with GPU can swap to a larger model via env var. All LLM calls go through `gavealab_poc/llm.py` to centralize model configuration.

---

## CHANGELOG

<!-- Append-only. Format: YYYY-MM-DD | <id> | added|revised|revoked|superseded | plan-NNNNNN | <note> -->

2026-05-24 | D-001 | added | - | ChromaDB vector store decision
2026-05-24 | D-002 | added | - | MCP tool exposure decision
2026-05-24 | D-003 | added | - | nomic-embed-text-v1 embedding model decision
2026-06-02 | D-004 | added | - | Streamlit + SQLite for GaveaLab UI and persistence
2026-06-02 | D-005 | added | - | Ollama as LLM backend for GaveaLab pipeline
2026-06-02 | design-update | revised | - | §1 §2 §3 §7 §8 §10 §11 §12 §13 §14 §15 §16 §17 updated to reflect GaveaLab as primary product; kb-qa repositioned as supporting tool
