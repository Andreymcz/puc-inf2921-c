# Roadmap 000007 | 2026-06-01 22:44 | GaveaLab Claims Analysis PoC -- Streamlit

## Source
- tttc-poc/tttc-light-js-ollama/pyserver/main.py (read -- pipeline reference)
- tttc-poc/tttc-light-js-ollama/pyserver/config.py (read -- prompts and Ollama config)
- product-design/conventions.md (read)
- product-design/project/product-design-as-intended.md (read)

## Brief (verbatim)
baseado no tttc-poc, quero re-implementar um fluxo de tratamento de relatos / claims de cidadaos em uma stack mais simples. quero implementar em python usando streamlit.
O caso de uso basico e o seguinte: # Como GaveaLab quero uma ferramenta que ajude a coletar e sintetizar pesquisas com cidadaos democratizar acesso a info e consolidar perfis e necessidades

Estou pensando em um fluxo onde o usuario cria uma analise, fazendo o upload de um arquivo csv, contendo varias entradas.
Sao disponiblizadas varias ferramentas de analise: separacao de temas automatico, usuario digita temas e o software categoriza automaticamente, dentro de um tema o software identifica opinioes divergentes.

Quero implementar uma prova de conceito usando python e streamlit de forma monolitica. se possivel usando uma llm local do mesmo nodo que o tttc-poc

## Agent Interpretation

Re-implement the tttc-poc LLM pipeline (topic tree -> claims -> cruxes) as a self-contained
Streamlit application. The app lets a user upload a CSV of citizen relatos, then offers three
analysis tools:

1. **Auto topics**: LLM automatically discovers topics/subtopics from the comments.
2. **Manual categorization**: User types topic names; LLM categorizes each comment against them.
3. **Divergence detection**: LLM identifies "crux" claims -- statements where opinions split.

LLM backend: Ollama at localhost:11434 (same stack as tttc-poc, default model qwen3:8b).
Architecture: single Python package `gavealab_poc/` under `gavealab-poc/`, launched with
`streamlit run gavealab-poc/app.py`.

---

## Wave Summary

### Wave 0 -- Foundation (sequential)
| # | ID | Title | Scope | Type | Plan | Status |
|---|-----|-------|-------|------|------|--------|
| 1 | scaffold | Project scaffold, Streamlit skeleton, Ollama client | cross-cutting | technical | plan-000008 | pending |

### Wave 1 -- Core Pipeline (sequential)
All depend on Wave 0.

| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|-----|-------|-------|------|------|-----------|--------|
| 2 | csv-upload | CSV upload page + data model | backend | technical | plan-000009 | scaffold | pending |
| 3 | auto-topics | Auto topic tree generation (LLM step 1) | backend | technical | plan-000010 | csv-upload | pending |
| 4 | claims | Claims extraction per comment (LLM step 2) | backend | technical | plan-000011 | auto-topics | pending |

### Wave 2 -- Analysis Tools (parallel)
Both depend on Wave 1 (claims).

| # | ID | Title | Scope | Type | Plan | Depends on | Status |
|---|-----|-------|-------|------|------|-----------|--------|
| 5 | manual-themes | Manual theme input + categorization tool | backend | technical | plan-000012 | claims | pending |
| 6 | cruxes | Divergent opinion (cruxes) detection tool | backend | technical | plan-000013 | claims | pending |

> Wave 2 items can be executed in parallel once Wave 1 is complete.

---

## Execution Instructions

### Wave 0 (sequential)
1. /implement plan-000008 (scaffold)

### Wave 1 (sequential)
Execute in order after Wave 0:
1. /implement plan-000009 (csv-upload)
2. /implement plan-000010 (auto-topics)
3. /implement plan-000011 (claims)

### Wave 2 (parallel -- 2 plans)
Both depend on Wave 1 completion.
Execute in parallel via multiple Claude Code sessions or worktree-isolated agents:
- /implement plan-000012 (manual-themes)
- /implement plan-000013 (cruxes)

---

## Design Notes

### Directory layout (new)
```
gavealab-poc/
  app.py                  # Streamlit entry point
  gavealab_poc/
    __init__.py
    llm.py                # Ollama client wrapper (re-uses ollama_openai_adapter pattern)
    data.py               # CSV parsing, AnalysisSession dataclass
    pipeline/
      topics.py           # Step 1: comments -> topic tree
      claims.py           # Step 2: comments + tree -> claims
      cruxes.py           # Step 3: claims -> crux/divergence analysis
    pages/
      upload.py           # Page: CSV upload
      auto_topics.py      # Page: auto topic analysis
      manual_topics.py    # Page: manual theme categorization
      cruxes.py           # Page: divergence view
  requirements.txt        # streamlit, ollama (httpx-based), pandas
```

### CSV format expected
```
id,text,speaker
c1,"O transporte publico precisa melhorar",Alice
c2,"As ruas estao em pessimo estado",Bob
```
Minimum required columns: `text`. `id` and `speaker` are optional (auto-generated if absent).

### LLM integration
Reuse `ollama_openai_adapter` approach from tttc-poc: OpenAI-compatible client pointed at
`http://localhost:11434/v1`. Default model: `qwen3:8b` (configurable via env var
`GAVEALAB_OLLAMA_MODEL`). All prompts sourced from tttc-poc `config.py` and adapted.
Thinking mode disabled (`think=False`) for speed, matching tttc-poc behavior.

### State management
Streamlit `st.session_state` holds the `AnalysisSession` (uploaded CSV + derived results).
No database or file persistence in PoC scope.

### No authentication, no persistence
PoC is single-user, local. No login, no saved sessions.
