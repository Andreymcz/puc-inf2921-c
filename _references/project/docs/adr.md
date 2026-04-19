---
recommended: true
freshness: immutable-once-accepted
diataxis: explanation
---

# Architecture Decision Records — INF2921 Grupo C

ADRs capture the *why* behind significant decisions so future team members don't undo them without understanding the trade-offs.

## File Organization

| Path | Purpose |
|------|---------|
| `docs/adr/` | All ADR files |
| `docs/adr/INDEX.md` | ADR index |
| `docs/adr/adr-NNNN-<slug>.md` | Individual ADR files |

## ADR Format

```markdown
# ADR-NNNN: {{Decision Title}}

- **Status**: {{Proposed | Accepted | Deprecated | Superseded by ADR-MMMM}}
- **Date**: {{YYYY-MM-DD HH:MM UTC}}
- **Deciders**: {{who was involved}}

## Context

{{What is the issue? What forces are at play?}}

## Decision

{{What are we deciding? State as imperative: "We will use X for Y."}}

## Consequences

{{What becomes easier or harder? What are the trade-offs?}}
```

## Existing Decisions

See `_references/project/product-design-as-intended.md § Decisions` for decisions recorded during design sessions.

| ID | Title | Status |
|----|-------|--------|
| D-001 | Use ChromaDB as the vector store | proposed |
