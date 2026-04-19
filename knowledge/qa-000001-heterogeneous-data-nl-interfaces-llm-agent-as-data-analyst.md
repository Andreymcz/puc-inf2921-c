# QA 000001 | 2026-04-19 14:00 UTC | Heterogeneous Data — NL Interfaces in the Survey LLM-Agent-as-Data-Analyst

**Brief**: Summary of what is stored in the knowledge base and a deep-dive into heterogeneous data NL interface systems (LOTUS, XMODE, BasicQA-Agent, Data Interpreter, AgenticData) from the LLM/Agent-as-Data-Analyst survey.

---

## Q1
What is stored in the knowledge base?

## A1
The knowledge base contains 1,218 indexed chunks from the following sources:

**PDFs:**
- Huyen (2025) — *AI Engineering: Building Applications with Foundation Models*
- Bommasani et al. (2022) — *On the Opportunities and Risks of Foundation Models* (Stanford)
- Weisz et al. (2024) — *Design Principles for Generative AI Applications* (CHI '24)
- de Souza et al. (2016) — *Software Developers as Users*
- EARTO (2014) — *The TRL Scale as a Research & Innovation Policy Tool*
- Tang et al. (2025) — *LLM/Agent-as-Data-Analyst Survey*

**Markdown:**
- `datasets.md`
- Two plan/QA files for the kb-qa project itself

**Thematic coverage:** foundation model theory, AI engineering practice, UX/HCI principles for GenAI, research methodology (TRL), and emerging agentic data analysis systems.

---

## Q2
Can you sample some contents from the vector store and make a summary?

## A2
Summary of each document in the knowledge base:

- **Huyen (2025)**: Practical book covering AI application architecture — model evolution (GPT-2 → multimodal), production patterns (RAG, guardrails, caching, routing), user feedback design.
- **Bommasani et al. (2022)**: Stanford survey on foundation model opportunities and risks — NLP adaptability, multilingual challenges, societal implications, homogenization risks.
- **Weisz et al. (2024)**: Six HCI/UX design principles for generative AI — validated via heuristic evaluation of ChatGPT, DALL-E, Copilot, and others by 18 design practitioners.
- **de Souza et al. (2016)**: Semiotic engineering applied to software development — how meaning inscribed in code propagates to end users; Human-Centered Computing (HCC) framework.
- **EARTO (2014)**: TRL scale origins (NASA/space), adoption across EU R&D funding, critique of its linear innovation assumptions, recommendations for adaptation.
- **Tang et al. (2025)**: Comprehensive survey on LLM/Agent-as-Data-Analyst — covers structured, semi-structured, unstructured, and heterogeneous data modalities; NL2SQL, autonomous pipeline orchestration, and future directions.

---

## Q3
In LLM/Agent-as-Data-Analyst Survey, tell me more about heterogeneous data with natural language interfaces — specifically: AgenticData, Data Interpreter - Analysis Agent; LOTUS, XMODE, BasicQA-Agent.

## A3
The survey organizes these systems into three sub-problems for heterogeneous data: **modality alignment**, **heterogeneous retrieval**, and **analysis agents**.

### Retrieval Layer

**LOTUS** *(arxiv '25)*
- Declarative programming interface for text-based heterogeneous data retrieval.
- Supports top-k search over data columns and similarity index construction.
- SQL-like abstraction (select, project, join, aggregation) expressed in natural language.
- Limitation: text-only; does not cross into image/video modalities.

**XMODE** *(arxiv '24)*
- Assumes heterogeneous metadata is organized in a database (structured side).
- Uses LLMs to decompose a NL query into multi-step subtasks: text-to-SQL, VLM-based image classification, visualization code generation.
- Example: *"Plot the number of paintings that depict war in each century"* → (1) SQL retrieves painting metadata, (2) VLM classifies images for war depiction, (3) LLM generates visualization code.
- Key strength: cross-modal operation chaining under a single NL query.

**BasicQA-Agent** *(alongside LOTUS/XMODE in Figure 1)*
- Positioned in the VectorDB / Doc Search column — targets heterogeneous retrieval via vector similarity.
- Functions as a simpler baseline for QA over indexed heterogeneous data, without full agentic orchestration.
- Represents the closed-world/literal end of the evolution axis toward open-world/semantic systems.

### Analysis Agent Layer

**Data Interpreter — Analysis Agent** *(ACL '25)*
- Placed at the top of the autonomy axis — most autonomous pipeline design in the survey.
- Can independently orchestrate analytical workflows: selecting data sources, operations, and tools from a NL user intent.
- Corresponds to O4 design goal: *Automatic Workflow Orchestration & Evolution* — self-designing prompts, selecting tools, generating new agentic modules.

**AgenticData** *(arxiv '25)*
- Multi-agent framework for cross-domain data analysis via natural language.
- Generates a logical plan in a single step, then runs it through:
  - **Plan Validator** — checks correctness
  - **Plan Optimizer** — refines the plan
  - **Plan Executor** — carries it out
- Supports both relational operators (filter, project) and semantic operators (scan, extract).
- Designed specifically for disorganized heterogeneous data (unlike XMODE which assumes organized metadata).

### Evolution Summary

| System | Interface | Autonomy |
|---|---|---|
| BasicQA-Agent | Natural Language | Static / low |
| LOTUS | DSL / SQL-like NL | Static |
| XMODE | Natural Language | Semi-autonomous (multi-step decomposition) |
| Data Interpreter | Natural Language | Fully autonomous |
| AgenticData | Natural Language | Autonomous + adaptive |

**Survey takeaway:** True cross-modal reasoning (SQL retrieval + VLM image analysis + NL generation in one pipeline) is still in its infancy in production — these systems are frontier research, not yet industrial standard.
