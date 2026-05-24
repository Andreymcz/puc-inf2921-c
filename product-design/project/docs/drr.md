---
recommended: true
depends_on: [all]
freshness: immutable-once-accepted
diataxis: explanation
---

# DESIGN RATIONALE RECORDS — INF2921-Grupo-C / kb-qa

> Design Rationale Records capture the *why* behind significant design decisions. See `product-design/project/product-design-as-intended.md ## Decisions` for the authoritative D-NNN decision list. DRR files in this directory provide the extended context and rejected alternatives.

## File Organization

| Path | Purpose |
|------|---------|
| `product-design/project/docs/drr/` | Extended DRR files (optional; for decisions needing more space than the D-NNN entry allows) |
| `product-design/project/product-design-as-intended.md ## Decisions` | Canonical D-NNN decision index |

## DRR Format

```markdown
# DRR-NNNNNN: {{Decision Title}}

- **Status**: {{Proposed | Accepted | Deprecated | Superseded by DRR-MMMM}}
- **Date**: {{YYYY-MM-DD HH:MM UTC}}
- **Deciders**: {{who was involved in the decision}}

## Context

{{What is the issue? What forces are at play? What problem needs solving?}}

## Decision

{{We will use X for Y.}}

## Consequences

- `+` {{Benefit}}
- `-` {{Trade-off}}

## Rejected Alternatives

### Alternative 01

{{ Proposal }}

- `+` {{ Pro }}
- `-` **{{ Main con — reason for rejection }}**
```

## Key Decisions

See `product-design/project/product-design-as-intended.md ## Decisions` for:

- D-001: Use ChromaDB as the vector store
- D-002: Expose retrieval via MCP (FastMCP)
- D-003: Use nomic-ai/nomic-embed-text-v1 as the embedding model
