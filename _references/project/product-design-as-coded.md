# AS-CODED — INF2921 Grupo C

<!-- maintained-by: Agent (post-skill); Agent classification since SEJA 2.8.4 -->

---

## Conceptual Design

### 1. Platform Purpose

Python CLI + MCP server for RAG-based knowledge retrieval. Ingests `.md` and `.pdf` files into ChromaDB and exposes `query_knowledge` via MCP for AI assistants.

#### Design Philosophy

Knowledge accessible in context — inside the AI assistant session, not in a separate tool.

### 2. Entity Hierarchy

```
KnowledgeBase (ChromaDB collection)
└── Document (source file: .md or .pdf)
    └── Chunk (embedded text segment)
```

#### KnowledgeBase

- ChromaDB collection (`kb_qa` default collection name from `constants.py`)
- Single instance per local deployment

#### Document

- Source file loaded by `src/kb_qa/loader.py` (Markdown) or PyMuPDF (PDF)
- Identified by file path

#### Chunk

- Text segment produced by `src/kb_qa/ingest.py`
- Embedded by `sentence-transformers`
- Stored with metadata in ChromaDB

### 3. Domain-Specific Concepts

**RAG Pipeline**: Ingest (loader.py → ingest.py) → Embed (sentence-transformers) → Store (ChromaDB) → Query (query.py) → MCP (agents/mcp_server.py)

### 4. Permission Model

#### System-Level Roles

| Role | Level | Capabilities |
|------|-------|-------------|
| User | Full access | CLI ingest, CLI query, MCP query_knowledge tool |

### 5. Authorship

N/A

### 6. Import / Export

Documents ingested from local filesystem via `kb-qa ingest <path>`.

### 7. i18n

No runtime i18n. Documents in pt-BR or en-US.

### 8. UX Patterns

CLI only. Commands: `kb-qa ingest`, `kb-qa query`, `kb-qa list`.

### 9. Visual Design

N/A

### 10. Validation Constants

| Field | Value | Source |
|-------|-------|--------|
| Chunk size | defined in `src/kb_qa/constants.py` | constants.py |

---

## Metacommunication

> Post-skill will populate this section after the first plan execution.

---

## Journey Maps

> Post-skill will populate this section after the first plan execution.
