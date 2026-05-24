# DESIGN INTENT — INF2921-Grupo-C / kb-qa

<!-- maintained-by: human (designer); Human (markers) classification since SEJA 2.8.3 -->

> **Classification**: `Human (markers)` — prose is human-authored only. Agents may write `STATUS` markers on §1-§17 sections, §15 JM-TB-NNN journey entries, and `### D-NNN:` Decision entries via `apply_marker.py` after AskUserQuestion confirmation. Agents may also append lines to the `## CHANGELOG` section.

---

## 0. Planned Changes

| Target Version | Change Summary | Motivation / Rationale |
|---|---|---|
| v0.2 | Session-reuse CLI: avoid reloading SentenceTransformer on every call | Improve CLI startup time; the `KbQa` class already exists as a session-reuse wrapper |
| v0.2 | Expose similarity scores in `ask` command output | Give users confidence signals; currently raw chunks are returned with no relevance indication |
| v0.3 | LLM answer synthesis in CLI (`ask --synthesize`) | Provide direct answers via Claude, not just raw chunks |

---

## 1. Platform Purpose

kb-qa is a local RAG (Retrieval-Augmented Generation) knowledge base designed for the INF2921/CIS2114 AI Systems Design course at PUC-Rio (2026.1). It enables researchers, students, and AI developers to ingest their own `.md` and `.pdf` documents into a local ChromaDB vector store and query them semantically — without sending document content to any cloud service.

The core problem it solves: when working with Claude or other AI tools, researchers frequently lack a way to inject private or course-specific documents (lecture notes, papers, research notes) into the AI's context without copy-pasting. kb-qa bridges this gap by exposing a `query_knowledge` MCP tool that any MCP-enabled AI client can call to retrieve relevant chunks from the local knowledge base.

The project is designed to be a greenfield course demonstration while remaining general-purpose enough for adoption by other teams. Its defining principle is privacy-first: all embedding, storage, and retrieval runs locally.

### Design Philosophy

Privacy-first local RAG. Documents never leave the machine. The system does one thing well: accept a natural-language query and return the most semantically relevant chunks from the user's own documents. There is no user account, no cloud sync, no telemetry. The minimal API surface (one CLI group, one MCP tool) is intentional — simplicity enables trust.

---

## 2. Entity Hierarchy

<!-- REQ-ENT-001 -->

```
KnowledgeDocument  (.md or .pdf file in knowledge/)
└── Chunk          (text segment extracted during ingestion)
    └── Embedding  (vector stored in VectorStore collection)

VectorStore        (ChromaDB persistent collection — holds all Chunks)
```

### KnowledgeDocument

A source file (`.md` or `.pdf`) placed by the user in the `knowledge/` directory. Not stored directly in the system — only its derived Chunks are indexed. Visibility: local filesystem only. Ownership: whoever places the file. No soft-delete semantics (the file simply exists or does not). Identified by its filesystem path.

### Chunk

The atomic unit of content. A text segment extracted from a KnowledgeDocument during ingestion. Each Chunk carries metadata: `type` (md | pdf), `name` (filename without extension), `source` (absolute file path), and a content-addressable ID (MD5 hash of `source + first 200 chars of text`). Chunks are idempotent: re-ingesting the same document skips existing Chunk IDs unless `--force` is used.

### VectorStore

A ChromaDB `PersistentClient` collection named `kb-qa-docs`, stored at `knowledge/vectorstore/`. Holds all Chunks as cosine-similarity embeddings produced by the `nomic-ai/nomic-embed-text-v1` model. Not gitignored from the design perspective — it is the derived index that must exist before queries can be served.

---

## 3. Domain-Specific Concepts

**Content-addressable chunking**: Each Chunk is identified by an MD5 hash of its source path + first 200 characters of text. This enables incremental ingestion — only new or changed chunks are added on re-ingest, without requiring a full wipe and rebuild.

**Embedding model**: `nomic-ai/nomic-embed-text-v1` via `sentence-transformers`. Chosen for strong multilingual performance and permissive licensing. The model name is centralized in `constants.py` to enable future upgrades without scattered changes.

**Cosine similarity search**: Queries are embedded using the same model and compared against all Chunk embeddings using cosine distance (`hnsw:space: cosine`). The `n_results` parameter controls how many top chunks are returned.

**MCP tool boundary**: The system exposes retrieval via the `query_knowledge` MCP tool (FastMCP). The tool is stateless with respect to conversation — each call is an independent retrieval, not a session. The MCP boundary is the only external surface: it accepts a question string and returns a list of chunk dicts.

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

Graduate students and researchers in the INF2921/CIS2114 AI Systems Design course (PUC-Rio, 2026.1). Team members: Andrey, Mauro, Julia, Herbert, Natali. Domain expertise: AI/ML research and software engineering. Language mix: Portuguese (pt-BR) native, English (en-US) technical.

### Localization Design

| Aspect | Primary | Secondary |
|--------|---------|-----------|
<!-- REQ-I18N-001 -->
| UI default language | pt-BR (knowledge documents) | en-US (CLI interface, code, MCP tool) |
| Backend error default | en-US | — |

The CLI interface and MCP tool responses are English-only. Knowledge documents can be in any language — the embedding model handles multilingual content. No frontend localization applies.

---

## 8. User Experience Patterns (Domain-Driven)

<!-- REQ-UX-001 -->

**Ingest-then-query workflow**: The user places documents in `knowledge/`, runs `kb-qa ingest`, then queries via `kb-qa ask` or through the MCP tool in their AI session. The two phases (ingestion and retrieval) are intentionally decoupled — ingestion is a one-time or periodic operation, querying is interactive.

**Incremental ingestion**: Repeated `kb-qa ingest` runs are fast and idempotent — only new chunks are added. Users can add documents to `knowledge/` and re-run ingest without losing existing indexed content. The `--force` flag bypasses this for full reingest.

**CLI status visibility**: The `kb-qa status` command shows chunk counts by document type and a delta between the knowledge directory and the vector store, so users can see at a glance whether re-ingestion is needed.

**MCP passthrough design**: The `query_knowledge` tool returns raw chunks with `text`, `type`, `name`, and `source` metadata. The AI client (Claude, Copilot) is responsible for synthesizing the answer — kb-qa's job is retrieval only. This keeps the tool composable with any MCP consumer.

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

| Constant | Value | Domain Rationale |
|----------|-------|-----------------|
| `n_results` max | 20 | Prevents excessive token usage in downstream LLM consumers; ChromaDB performance degrades past this for typical knowledge bases |
| `EMBED_BATCH_SIZE` | 256 | Balance between GPU/CPU memory and throughput during model.encode() |

These constants are defined in `src/kb_qa/constants.py`. No frontend counterpart — this is a CLI/MCP-only tool.

---

# Part II — Metacommunication

## 11. Global Metacommunication Vision

<!-- REQ-MC-001 -->

I know you are a researcher or AI developer who needs instant, semantic access to your own documents during work or study sessions. Therefore, I have designed a local knowledge base that lets you ingest your own `.md` and `.pdf` files and query them through Claude and other AI tools — without sending your documents to any cloud service.

*Generated by the design agent based on specifications defined in the design session on 2026-05-24.*

---

## 12. Extended Metacommunication Template Guiding Questions

1. Analysis (understanding needs and defining requirements)
   1.1. What do I know or don't know about (all of) you and how?
   I know you are a graduate student or researcher at PUC-Rio enrolled in INF2921/CIS2114, working with AI systems and natural language processing tools. I know you work with course materials, papers, and research notes that you cannot easily inject into AI sessions. I do not know the specific document types or languages you work with most, or whether you use the MCP interface through Claude Code or another client.
   > For detailed persona profiles and problem scenarios, see `project/ux-research-results.md §1-§4`.
   1.2. What do I know or don't know about affected others and how?
   The primary affected party is the document owner (you). No other users are affected since this is a single-user local tool. I do not know whether course documents are shared among team members or whether each person maintains an independent knowledge base.
   1.3. What do I know or don't know about the intended (and other anticipated) contexts of use?
   Intended: AI-assisted study sessions, research note retrieval during writing, course material lookup during Claude conversations. Anticipated but not primary: batch document processing, integration with note-taking tools. I do not know the typical session length or document volume.
   1.4. *What ethical questions can be raised by what I have learned? Why?
   The tool processes documents that may contain sensitive research data, personal notes, or proprietary information. The privacy-first design (local-only storage) mitigates this, but users should be aware that MCP client queries — including the retrieved text — pass through the AI provider's inference infrastructure.

2. Design
   2.1. What have I designed for you?
   A CLI tool and MCP server for local semantic search over your own documents. The CLI provides `ingest`, `status`, and `ask` commands. The MCP server exposes `query_knowledge` to any MCP-compatible AI client.
   2.2. Which of your goals have I designed the system to support?
   (1) Quick retrieval of relevant content from a personal document corpus without manual search. (2) Integration with AI tools (Claude, Copilot) via MCP without copy-pasting document content. (3) Privacy: no documents uploaded to third-party services.
   2.3. In what situations/contexts do I intend/accept you will use the system to achieve each goal? Why?
   During AI-assisted writing or research sessions when you need to ground the AI's responses in your own documents. During course study when you want to quickly find relevant lecture notes or papers.
   > For detailed solution representations, see Section 13 below.
   2.4. How should you use the system to achieve each goal, according to my design?
   Place documents in `knowledge/`, run `kb-qa ingest`, then either use `kb-qa ask "your question"` directly or configure the MCP server in your Claude Code settings and let Claude call `query_knowledge` automatically.
   2.5. For what purposes do I not want you to use the system?
   As a replacement for a proper full-text search engine on large corpora (ChromaDB at this scale is not optimized for millions of documents). As a multi-user service. As a system that makes write decisions — it is read-only at the MCP boundary.
   2.6. *What ethical principles influenced my design decisions?
   Data sovereignty: your documents stay on your machine. Minimal surface: the tool does one thing. Transparency: open source, no telemetry.
   2.7. *How is the system I designed for you aligned with those ethical considerations?
   The vector store is local and gitignored. The MCP tool is read-only. There are no analytics calls or external API dependencies beyond the embedding model (which runs locally).

3. Prototyping, implementation, and formative evaluation
   3.1. How have I built the system to support my design vision?
   Python 3.13 + ChromaDB (local PersistentClient) + sentence-transformers (nomic-embed-text-v1, local inference) + FastMCP + click CLI. All compute runs locally.
   3.2. What have I built into the system to prevent undesirable uses and consequences?
   `n_results` cap at 20. Read-only MCP tool. No write endpoints exposed.
   3.3. What have I built into the system to help identify and remedy unanticipated negative effects?
   `kb-qa status` reports chunk counts and delta; logging at INFO level during ingestion; error messages surfaced to the CLI user.
   3.4. *What ethical scenarios have I used to evaluate the system?
   (1) A user inadvertently exposes sensitive documents via git — mitigated by gitignoring `knowledge/vectorstore/`. (2) An MCP client uses `query_knowledge` to exfiltrate document content — mitigated by the local-only deployment model (content only leaves via the MCP query response, which the user explicitly configured).

4. Continuous, post-deployment evaluation and monitoring
   4.1. How much of my vision is reflected in the system's actual use?
   To be evaluated after the course team adopts the MCP integration in their Claude Code sessions.
   4.2. What unanticipated uses have been made? By whom? Why?
   TBD — early-stage project.
   4.3. What anticipated and unanticipated effects have resulted from its use? Whom do they affect? Why?
   TBD.
   4.4. *What ethical issues need to be handled through system redesign, redevelopment, policy, or even decommissioning?
   TBD.

---

## 13. Solution Representations

### Option B: User Stories

#### US-001: Ingest course materials

- **Story:** As a course team member, I want to ingest my lecture PDFs and notes so that I can query them through Claude without copy-pasting.
- **Goals:** G-001 (quick retrieval), G-003 (privacy)
- **Acceptance Criteria:**
  - Running `kb-qa ingest` processes all `.md` and `.pdf` files in `knowledge/`
  - Running it again on unchanged files does not duplicate chunks
  - Progress is visible via a progress bar

#### US-002: Query knowledge base via MCP

- **Story:** As a researcher, I want Claude to automatically retrieve relevant chunks from my knowledge base so that its answers are grounded in my own documents.
- **Goals:** G-001 (quick retrieval), G-002 (AI integration)
- **Acceptance Criteria:**
  - The MCP server is running and configured in `.claude/settings.json`
  - Claude calls `query_knowledge` with my question and receives relevant chunks
  - The result includes `text`, `type`, `name`, and `source` for each chunk

#### US-003: Check indexing status

- **Story:** As a team member, I want to know whether my documents are up to date in the vector store without re-ingesting everything.
- **Goals:** G-001 (quick retrieval)
- **Acceptance Criteria:**
  - `kb-qa status` shows chunk counts by type (md, pdf)
  - It shows a delta between knowledge directory and vector store

---

## 14. Per-Feature Metacommunication Intentions

| Feature / Flow | Designer Intent | Priority | Source | Last Synced |
|---|---|---|---|---|
<!-- REQ-MC-002 -->
| Document ingestion (kb-qa ingest) | I have designed ingestion to be incremental and idempotent so that you can add documents at any time without disrupting the existing index | P0 | human | 2026-05-24 00:00 UTC |
| Semantic query (kb-qa ask / query_knowledge) | I have designed retrieval to return the most relevant chunks with source metadata so that you can trace every result back to its original document | P0 | human | 2026-05-24 00:00 UTC |
| Status check (kb-qa status) | I have designed the status command to show you exactly how many chunks are indexed and whether re-ingestion is needed, so you always know the state of your knowledge base | P1 | human | 2026-05-24 00:00 UTC |
| MCP integration | I have designed the MCP server as a passthrough so that any AI tool can call query_knowledge and receive grounded context from your documents without any modification to your workflow | P0 | human | 2026-05-24 00:00 UTC |

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

# Part III — Delta from As-Coded

## 16. Conceptual Design Delta

### New (in as-intended but not in as-coded)

| Section | Element | Description |
|---|---|---|
<!-- REQ-DELTA-001 -->
| §0 | Planned v0.2 improvements | Session-reuse CLI + score visibility not yet implemented |
| §14 | Synthesize intent | `ask --synthesize` not yet implemented |

### Changed (differs between as-coded and as-intended)

| Section | Element | As-Coded | As-Intended |
|---|---|---|---|
| — | — | — | — |

### Removed (in as-coded but not in as-intended)

| Section | Element | Reason for Removal |
|---|---|---|
| — | — | — |

---

## 17. Metacommunication Delta

### New Intentions (not yet implemented)

| Feature / Flow | Designer Intent | Priority |
|---|---|---|
| Score visibility in ask output | Show cosine distance alongside each result chunk | P1 |
| LLM synthesis in ask command | Offer `--synthesize` flag to call Claude and return a direct answer | P2 |

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

## CHANGELOG

<!-- Append-only. Format: YYYY-MM-DD | <id> | added|revised|revoked|superseded | plan-NNNNNN | <note> -->

2026-05-24 | D-001 | added | - | ChromaDB vector store decision
2026-05-24 | D-002 | added | - | MCP tool exposure decision
2026-05-24 | D-003 | added | - | nomic-embed-text-v1 embedding model decision
