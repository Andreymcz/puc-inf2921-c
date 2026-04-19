# UX RESEARCH — INF2921 Grupo C

<!-- maintained-by: human (designer/researcher); Human (markers) classification since SEJA 2.8.2 -->

---

## 1. Personas

### Persona Inventory

| ID | Name | Role / Archetype | Goals |
|----|------|-----------------|-------|
| R-P-001 | Andrey | IT Engineer | Build and evolve the RAG pipeline; retrieve technical references quickly |
| R-P-002 | Mauro | IT Engineer | Build and evolve the RAG pipeline; integrate with AI tools |
| R-P-003 | Julia | Production Engineer | Access course knowledge; apply systems thinking to AI project |
| R-P-004 | Herbert | Social Scientist | Access course knowledge in natural language without technical friction |
| R-P-005 | Natali | Designer | Access design references; contribute UX thinking to the project |

### R-P-001: Andrey

> **Role / Archetype:** IT Engineer — builder and maintainer
>
> **Goals:**
> - G-001: Build a reliable RAG ingest and query pipeline
> - G-002: Integrate the knowledge base with AI assistant tools via MCP
>
> **Technical proficiency:** Expert
> **Usage frequency:** Daily

### R-P-002: Mauro

> **Role / Archetype:** IT Engineer — builder
>
> **Goals:**
> - G-001: Develop and test the knowledge base components
> - G-002: Ensure MCP compatibility with Copilot and Claude
>
> **Technical proficiency:** Expert
> **Usage frequency:** Daily

### R-P-003: Julia

> **Role / Archetype:** Production Engineer — systems thinker
>
> **Goals:**
> - G-001: Apply engineering methods to the AI project
> - G-002: Access course knowledge efficiently during work sessions
>
> **Technical proficiency:** Intermediate
> **Usage frequency:** Weekly

### R-P-004: Herbert

> **Role / Archetype:** Social Scientist — domain expert and end user
>
> **Goals:**
> - G-001: Ask questions in natural language and get grounded answers
> - G-002: Contribute social science knowledge to the knowledge base
>
> **Technical proficiency:** Novice (CLI)
> **Usage frequency:** Weekly

### R-P-005: Natali

> **Role / Archetype:** Designer — UX contributor and end user
>
> **Goals:**
> - G-001: Access design and course references quickly
> - G-002: Contribute to the product's interaction design
>
> **Technical proficiency:** Intermediate
> **Usage frequency:** Weekly

---

## 2. Problem Scenarios

### R-PS-001: Scattered course knowledge

- **Persona:** R-P-004 (Herbert), R-P-005 (Natali)
- **Pain:** Course materials, meeting notes, and research references are spread across emails, shared folders, and individual notes. Finding a specific piece of information requires manual search across multiple places.
- **Current workaround:** Ask teammates directly or search manually.

### R-PS-002: Context lost during AI sessions

- **Persona:** R-P-001 (Andrey), R-P-002 (Mauro)
- **Pain:** When working with Claude or Copilot, the AI assistant lacks context about the team's specific project decisions, accumulated knowledge, and course material.
- **Current workaround:** Manually paste relevant context into each session.

---

## 3. Cross-Reference Map

| Persona | Problem Scenarios | Design Intent Sections |
|---------|-------------------|----------------------|
| R-P-001, R-P-002 | R-PS-002 | §1 Platform Purpose, §3 RAG Pipeline |
| R-P-004, R-P-005 | R-PS-001 | §1 Platform Purpose, §11 Global Vision |

---

## 4. Processing Status

| ID | Type | Status | Incorporated in |
|----|------|--------|----------------|
| R-P-001..005 | Persona | New | — |
| R-PS-001 | Problem Scenario | New | — |
| R-PS-002 | Problem Scenario | New | — |

---

## 5. Discovered User Journeys

> To be populated as the team uses the tool and observes actual usage patterns.

---

## CHANGELOG

### 2026-04-19
- Initial UX research file created via `/design`. Personas derived from team composition. Problem scenarios derived from project description.
