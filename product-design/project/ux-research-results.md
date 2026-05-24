# UX RESEARCH — INF2921-Grupo-C / kb-qa

<!-- maintained-by: human (designer/researcher); Human (markers) classification since SEJA 2.8.2 -->

> **Classification**: `Human (markers)` — prose content (personas, problem scenarios, journey observations) is human-authored only. Agents may write `<!-- INCORPORATED: plan-NNNNNN | YYYY-MM-DD -->` markers and append lines to the `## CHANGELOG` section, but only via `apply_marker.py` and only after AskUserQuestion confirmation.

---

## 1. Personas

### Persona Inventory

| ID | Name | Role / Archetype | Goals |
|----|------|-----------------|-------|
| R-P-001 | Course team member | Graduate student, AI researcher | Quickly retrieve relevant course content in AI sessions; avoid manual copy-paste |
| R-P-002 | Tool adopter | Developer evaluating the project for their own research | Adapt kb-qa to their own document corpus; extend the MCP tool |

### R-P-001: Course team member

> **Role / Archetype:** Graduate student in AI Systems Design (INF2921), PUC-Rio 2026.1
>
> **Bio:** Works daily with course materials (lecture PDFs, papers, research notes) and uses Claude Code as their primary AI assistant. Needs to ground AI answers in course-specific content that is not in Claude's training data.
>
> **Goals:**
> - G-001: Retrieve relevant chunks from lecture notes and papers during a Claude session without copy-pasting
> - G-002: Know the indexing state of the knowledge base at a glance
> - G-003: Ensure course documents stay on their machine (privacy)
>
> **Key Frustrations:**
> - Context window fills up when copy-pasting large PDFs into Claude
> - No easy way to search across multiple PDFs at once
>
> **Relevant Context:**
> - Technical proficiency: expert (Python, CLI tools, AI/ML)
> - Usage frequency: daily during active coursework periods
> - Domain knowledge: AI systems, NLP, RAG architectures

### R-P-002: Tool adopter

> **Role / Archetype:** Developer or researcher evaluating kb-qa for their own use
>
> **Bio:** Found kb-qa through the course repository or word-of-mouth. Wants to use it with their own document set (engineering specs, research papers, technical notes) and possibly extend the MCP tool or integrate it into their workflow.
>
> **Goals:**
> - G-001: Ingest their own documents with minimal configuration
> - G-002: Extend the MCP tool to support additional document types or metadata filters
>
> **Key Frustrations:**
> - Setup friction: embedding model download on first run (~274MB, no progress feedback)
> - Limited documentation on extending the loader for new file types
>
> **Relevant Context:**
> - Technical proficiency: intermediate to expert
> - Usage frequency: occasional (setup + periodic ingest)
> - Domain knowledge: varies

---

## 2. Problem Scenarios

### R-PS-001: AI session without course context

- **Persona:** R-P-001 (Course team member)
- **Goals:** G-001, G-003
- **Setting:** Evening study session, working on a course assignment with Claude Code open

The student is asking Claude about a specific algorithm discussed in a lecture PDF. Claude's training data does not include this course-specific material, so it gives a generic answer that misses the professor's specific formulation. The student has to find the PDF, locate the relevant section, and copy-paste it into the conversation — breaking their flow and consuming context window.

The problem recurs every time course-specific content is needed. For a course where lectures reference recent papers not in Claude's training data, this happens multiple times per session.

---

### R-PS-002: Stale knowledge base after adding new documents

- **Persona:** R-P-001 (Course team member)
- **Goals:** G-001, G-002
- **Setting:** After receiving new lecture materials mid-course

The student downloads new PDFs from the course site and places them in `knowledge/`. They forget to run `kb-qa ingest` and continue querying. The MCP tool returns results only from previously indexed documents, silently missing the new content. There is no warning that the index is out of date.

---

## 3. Cross-Reference Map

| Artifact ID | Artifact Title | Design Artifact | Relationship |
|-------------|---------------|----------------|-------------|
| R-P-001 | Course team member | product-design-as-intended §12 EMT 1.1 | Feeds |
| R-PS-001 | AI session without course context | product-design-as-intended §13 US-002, §14 MCP integration intent | Feeds |
| R-PS-002 | Stale knowledge base | product-design-as-intended §13 US-003, §8 UX patterns (status command) | Feeds |

---

## 4. Processing Status

| Artifact | Status | Incorporated in |
|----------|--------|----------------|
| R-P-001 | Incorporated in §12 EMT analysis | — |
| R-P-002 | Noted, not yet incorporated in design intent | — |
| R-PS-001 | Incorporated in §13 US-002 | — |
| R-PS-002 | Incorporated in §8 UX patterns and §0 planned changes | — |

---

## 5. Discovered User Journeys

> Journeys observed in real or simulated usage sessions. These inform `project/product-design-as-intended.md §15 Designed User Journeys`. Section is structurally append-only for prose.

### JM-E-001: First-time setup friction

Observed during the team's initial project setup. The first `kb-qa ingest` run triggered a silent 274MB model download with no visible progress indicator. Two team members believed the command had hung and killed it, requiring a full reingest.

**Opportunity**: Add an explicit "Downloading embedding model..." message before the first `SentenceTransformer()` call, or check if the model is cached and inform the user.

---

## CHANGELOG

<!-- Append-only. Format: YYYY-MM-DD | <id> | added|revised | plan-NNNNNN | <note> -->

2026-05-24 | R-P-001 | added | - | Initial persona from /design session
2026-05-24 | R-P-002 | added | - | Initial persona from /design session
2026-05-24 | R-PS-001 | added | - | Initial problem scenario from /design session
2026-05-24 | R-PS-002 | added | - | Initial problem scenario from /design session
2026-05-24 | JM-E-001 | added | - | First-time setup friction observed by team
