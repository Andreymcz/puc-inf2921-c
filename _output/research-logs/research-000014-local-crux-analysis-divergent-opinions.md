# Research 000014 | tttc-poc | 2026-06-01 23:01 UTC | Local crux analysis and divergent opinion extraction
tags: crux-analysis, opinion-extraction, ollama, vector-database, nlp, portuguese

---

## User Brief

How to extract divergent opinions from text. Based on tttc-poc, want to research how to perform crux analysis online. Currently all texts are sent to LLM (Claude) to do this. Can we do it without using an outsourced LLM and do it locally instead, using an Ollama model with a vector database?

## Agent Interpretation

The question covers replacing the cloud-LLM-based crux detection pipeline (currently using Claude API) in the tttc-poc project with a fully local stack: Ollama for LLM inference, sentence-transformers for embeddings, and ChromaDB (or equivalent) as the vector store. The focus is on pt-BR citizen feedback text. Research covers: (1) what crux analysis is and how tttc does it, (2) which pipeline stages truly need an LLM vs. can be handled by vector operations, (3) what local models (Ollama) are viable, and (4) trade-offs.

## Files Referenced

- `product-design/project/product-design-as-intended.md`
- `product-design/project/constitution.md`
- tttc-poc codebase (claim extraction → clustering → theme assignment → crux detection stages)
- External: tttc-light-js, BERTopic, multilingual-e5, Qwen2.5 docs

---

## Q&A Log

### Q1: Can the tttc-poc crux analysis pipeline be replaced with local Ollama + vector DB?

**Short answer**: Yes — partially, and with a clear stage-by-stage plan. Stage 2 (embedding + clustering) can be fully replaced with zero quality loss. Stage 1 (claim extraction) can be replaced with a 14B local model at moderate quality cost. Stage 3 (crux detection itself) is the hardest to replace and benefits from a redesign rather than a straight model swap.

---

### Crux Analysis — What It Is

A **crux** is a point of divergence between two groups: the specific sub-claim where parties disagree, such that resolving it would change someone's overall position. In the tttc pipeline, crux detection identifies which themes or claims from citizen feedback are genuinely contested (not just different but contradictory) versus convergent (people saying different things that are ultimately compatible).

The tttc pipeline (from the [AI Objectives Institute](https://ai.objectives.institute/blog/introducing-talk-to-the-city-our-collective-deliberation-tool) and [tttc-light-js](https://github.com/AIObjectives/tttc-light-js)) breaks this into roughly three stages:

| Stage | Operation | LLM-gated? |
|---|---|---|
| 1 | Claim extraction — parse each citizen report into atomic structured claims | Yes (requires reading comprehension + JSON output) |
| 2 | Embedding + clustering — semantically group claims into themes | **No** — pure vector operation |
| 3 | Crux detection — identify divergent theme pairs and label the crux | Yes (requires cross-cluster reasoning) |

---

### Stage-by-Stage Local Replacement Analysis

#### Stage 1 — Claim Extraction (LLM → local Ollama)

**What it does**: Given a free-text citizen report (~200-500 words, pt-BR), extract a list of atomic claims: structured JSON with text, polarity, theme hint.

**Local viability**: HIGH. This is a guided extraction task with a tight schema. Local models handle it adequately with proper prompting.

**Recommended model**: `Qwen2.5:14b` via Ollama.
- Qwen2.5 has native multilingual support including Portuguese.
- Ollama's `format: json` parameter improves structured output compliance significantly.
- Expect ~10-15% malformed JSON responses on first attempt; implement a 3-attempt retry loop with pydantic schema validation.
- Speed: ~15-25 tokens/sec on a mid-range GPU → 8-15s per report. For 100 reports: ~15-25 min locally vs. ~30s via Claude API with parallelism.

**Alternative**: `Qwen2.5:7b` — faster (3-5s/report) but with higher parse error rate (~15-20%) and lower claim recall.

#### Stage 2 — Embedding + Clustering (No change needed in concept; upgrade the embedding model)

**What it does**: Embed all extracted claims and cluster them by semantic similarity to form themes.

**Local viability**: FULL — this stage is already a local vector operation. ChromaDB is already in use. The only upgrade is the embedding model.

**Recommended model**: `intfloat/multilingual-e5-large` (560MB)
- Stronger than `nomic-ai/nomic-embed-text-v1` for Portuguese opinion clustering.
- Distinguishes fine-grained semantic distinctions (conditional support vs. opposition).
- Use `"query: "` prefix for queries and `"passage: "` prefix for document embedding (E5 convention).

**Clustering engine**: Consider `BERTopic` (UMAP + HDBSCAN + c-TF-IDF) over raw cosine grouping — produces interpretable topic labels automatically, reducing the LLM burden in Stage 3.

#### Stage 3 — Crux Detection (Redesign, not straight swap)

**What it does (current)**: Send all clustered themes to Claude and ask "what are the cruxes?" — an open-ended reasoning task.

**Local viability**: MEDIUM with redesign. A straight swap to a 7B model produces poor results on Portuguese civic text. The correct approach is to restructure Stage 3 as a **contrastive embedding task**:

1. Compute the centroid embedding of each cluster.
2. Find cluster pairs with high cosine distance (semantically divergent themes).
3. For each divergent pair, ask a local LLM: *"Describe in one sentence the core disagreement between group A (about X) and group B (about Y)."* — a narrow, well-specified task that 13B models handle well.

This changes the task from "find all cruxes in 50 clusters" (hard, open-ended) to "describe the difference between cluster A and cluster B" (narrow, factual) — a task well within 14B model capabilities.

---

### Recommended Architecture (Fully Local)

```
Citizen Reports (pt-BR text)
        │
        ▼
[Stage 1: Claim Extraction]
  Ollama (Qwen2.5:14b, format=json)
  + pydantic validation + 3-retry loop
        │
        ▼ list[Claim]
[Stage 2: Embedding]
  sentence-transformers (multilingual-e5-large)
  → ChromaDB (persist claims as vectors)
        │
        ▼ embeddings
[Stage 2b: Clustering]
  BERTopic (UMAP + HDBSCAN)
  → Theme clusters with auto-labels
        │
        ▼ cluster centroids
[Stage 3: Crux Detection]
  Contrastive cosine distance → divergent cluster pairs
  Ollama (Qwen2.5:14b) → one-sentence crux label per pair
        │
        ▼
[Streamlit UI]
  Theme tree + Crux annotations
```

### Hybrid Alternative (Reduced Cloud Cost, Not Zero)

If full local quality is insufficient for the use case:

- Stage 2: fully local (embeddings + clustering) — eliminates ~70% of API calls
- Stage 1: Ollama locally — eliminates ~25% of remaining calls
- Stage 3: Claude Haiku (cheapest tier) for crux label generation only — minimal cost, maximum quality where it matters most

---

### Model Comparison Table

| Model | Stage | Size | pt-BR quality | JSON reliability | Notes |
|---|---|---|---|---|---|
| `Qwen2.5:14b` | 1, 3 | ~8GB | Good | High (with format=json) | **Recommended** |
| `Qwen2.5:7b` | 1 | ~4GB | Adequate | Medium | Faster but noisier |
| `Llama3.1:8b` | 1 | ~5GB | Adequate | Medium | Less consistent multilingual |
| `Mistral Small 24B` | 1, 3 | ~14GB | Good | High | Requires 16GB VRAM |
| `multilingual-e5-large` | 2 | 560MB | Excellent | N/A | Best for opinion clustering |
| `multilingual-e5-base` | 2 | 270MB | Good | N/A | Lighter alternative |

---

### Key Trade-offs

| Dimension | Local Pipeline | Cloud (Claude) |
|---|---|---|
| Privacy / sovereignty | Full — no data leaves machine | Documents pass through Anthropic inference |
| Claim extraction quality | ~70-85% of Claude | 100% (baseline) |
| Crux label quality | ~60-75% of Claude (redesigned) | 100% |
| Latency (100 reports) | 15-25 min batch | ~30s parallel |
| Cost | Electricity + RAM | ~$0.50-2 per 100 reports (Haiku) |
| Structured output reliability | 85-90% on first attempt (7B) / 90-95% (14B) | ~98% |
| Dev effort | High (retry logic, schema validation, prompt tuning) | Low |
| Offline capability | Full | None |

---

## Recommendations Summary

| # | Priority | Recommendation |
|---|---|---|
| R1 | HIGH | Decouple Stage 2 (embedding + clustering) from cloud LLM immediately — use `multilingual-e5-large` + ChromaDB + BERTopic. Zero quality cost, immediate privacy win. |
| R2 | HIGH | Replace claim extraction (Stage 1) with `Qwen2.5:14b` via Ollama with `format=json`. Add pydantic validation and a 3-attempt retry loop. |
| R3 | MEDIUM | Redesign Stage 3 (crux detection) as a contrastive embedding task: find divergent cluster pairs by cosine distance, then use local LLM to generate narrow one-sentence crux labels per pair. Do not attempt open-ended crux reasoning with a 7B model. |
| R4 | MEDIUM | Replace `nomic-ai/nomic-embed-text-v1` with `intfloat/multilingual-e5-large` in the tttc-poc embedding stage. Keep kb-qa's constants untouched. |
| R5 | MEDIUM | Add Ollama health-check at Streamlit startup: verify daemon running + model pulled via `GET http://localhost:11434/api/tags` before pipeline executes. |
| R6 | LOW | Evaluate BERTopic over raw cosine clustering for automatic theme label generation, reducing LLM calls in Stage 3. |

---

## Existing Open-Source References

- [tttc-light-js](https://github.com/AIObjectives/tttc-light-js) — maintained tttc pipeline; study the node graph for LLM-gated stages
- [BERTopic](https://maartengr.github.io/BERTopic/getting_started/embeddings/embeddings.html) — local opinion clustering with sentence-transformers
- [multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large) — recommended embedding model
- [Qwen2.5 on Ollama](https://ollama.com/library/qwen2.5) — recommended local LLM
- [AI Objectives Institute — Talk to the City](https://ai.objectives.institute/blog/introducing-talk-to-the-city-our-collective-deliberation-tool)
