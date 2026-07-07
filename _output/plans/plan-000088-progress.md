# Progress -- Plan 000088

Append-only cross-iteration learnings. Each subagent reads this file at the start and appends findings at the end.

## Codebase Patterns
<!-- Subagents consolidate reusable patterns here -->
- Bare `python` is NOT on PATH in Git Bash on this machine; always run analytics scripts with `uv run python <script>` from the repo root.
- The parent `_output/briefs-index.md` is a LIVE index: it gained the research-000087 entry (2026-07-06) after the research window closed. To reproduce research-000087's published numbers, filter out `^| 2026-07` lines (corpus congelado, 96 entradas) before running `mine_harness_flows.py`; the live index (97) shifts F4 from 16 to 17 invocations.
- `mine_harness_flows.py` takes two positional args: parent briefs-index path, fala-gavea briefs-index path. Python's stable `list.sort` already implements the research's tie-break rule (re-sort by timestamp, file order on ties).

## Iteration Log

### 2026-07-06 -- Step 1: verificar e congelar numeros de suporte da taxonomia (SUCCESS)

- Ran `uv run python _output/generated-scripts/mine_harness_flows.py _output/briefs-index.md fala-gavea/_output/briefs-index.md` -- script ran as-is, no parsing/tie-break fixes needed.
- ONE minimal additive script change: new block printing row-normalized P(next|current) with row n (the raw top-14 count list hid the row totals n=36/23/27/11 cited in research-000087). No parsing or ordering logic touched.
- Also ran the script against a filtered copy of the parent index (excluding 2026-07 lines) to reproduce the research's frozen corpus (96 entries).
- Created `_output/tmp/taxonomia-support-counts.md` with verified numbers; committed both files (`9d56f0f`).
- Key verified numbers (frozen corpus): archetype supports -- (1) bootstrap: 3 F1 sessions start with advise, implement->implement 75% (6/8); (2) roadmap waves: 4 parent plans OK, fala-gavea 15 plans with `source: roadmap` (8 with explicit Wave) vs 12 claimed -- DIVERGENCE; (3) grooming: 11 reflections in F3, 8 followed by research/plan (4+4 of n=11) OK; (4) micro-loop: P(plan|research)=70% (16/23) in F3 OK; (5) relato: communicate->research 100% (2/2) in F3 OK. Transitions: plan->implement 71/55/50% (F1/F2/F3), implement->implement 75/29/15%, research->plan 100/33/70%, reflect->plan/research 60/40 (F2) and 36/36 (F3), plan->plan 14/40/17% -- all match. Phase metrics F1-F4 all match on frozen corpus (25/55/120/16 invocations; 3.6/5.5/6.7/2.3 inv/session; orphans 12/13/7/19%; chaining 16/27/26/12%).
- Divergences vs research-000087: (a) "12 planos fala-gavea com source: roadmap Wave" not reproducible -- actual 15 total / 8 with explicit Wave text; support file recommends citing 15 (8 explicit) or flagging 12 as unreproduced; (b) live parent index has 97 entries (F4=17) vs published 96 (F4=16) -- explained by the research-000087 self-entry, not an error; use cutoff <= 30/jun. Commits-per-phase row NOT verified (git-log-based, out of scope for this script) -- marked as taken from research-000087.

### 2026-07-06 -- Step 2: secao de taxonomia (SUCCESS, subagent paralelo)

Criada `_output/communication/2026-07-06/taxonomia-arquetipos-fluxo.md` -- secao autossuficiente pt-BR com regra de identificacao operacional, 5 arquetipos (assinatura + descricao + suporte verificado + ancora por ID) e fechamento com o papel duplo de /reflect. Divergencia do arquetipo 2 tratada: texto usa 15+4 verificados e marca o 12 da pesquisa como nao reproduzido. Ancoras: plano 000001 (bootstrap), roadmap-000151 + roadmap-000071 Wave 0 (ondas), reflection-000086/000163 (grooming), sessoes F3 21/26-jun (micro-loop), cadeia research-000087 -> plan-000088 (relato). Verificado: UTF-8 sem BOM, sem em/en-dashes ou curly quotes, setas ASCII '->'. Commit e log feitos pelo orquestrador (subagentes paralelos nao commitam).

### 2026-07-06 -- Step 3: figura de timeline (SUCCESS, subagent paralelo)

Criada `_output/communication/2026-07-06/timeline-faixas-paralelas.md`. Mermaid gantt com 2 sections (puc-inf2921-c: F1 24/abr-10/jun, F2 10-17/jun, F4 19-30/jun; fala-gavea: F3 17/jun-1/jul, ano 2026), datas conferidas contra research-000087 e taxonomia-support-counts.md (corpus congelado, F4=16 inv); sobreposicao F3||F4 destacada via tasks `active`; legenda + tabela textual-fallback acessivel + frase de leitura do argumento causal incluidas. mermaid-cli nao instalado -- validacao por inspecao de sintaxe. Sem divergencias. UTF-8 sem BOM, sem caracteres tipograficos.

### 2026-07-06 -- Step 4: passe de privacidade/LGPD nos dois entregaveis (SUCCESS -- aprovado, 0 correcoes)

Revisados `taxonomia-arquetipos-fluxo.md` e `timeline-faixas-paralelas.md` contra Rec 3 da research-000087 e Checklist D (security-checklists.md). Verificado: (a) nomes de colegas (Andrey, Mauro, Julia, Herbert, Natali, Sheila, Fabiene) + @-handles, e-mails, telefones -- grep sem matches; (b) nenhuma citacao verbatim de brief/reflection/WhatsApp -- ancoras usam apenas ID + parafrase neutra (notavel: reflection-000052 aparece como "pivo de escopo do produto", sem o conteudo de WhatsApp que o proprio research log menciona); (c) nenhum conteudo de relato de seguranca cidada. Resultado: APROVADO sem correcoes. Nota de passe registrada no rodape de cada arquivo; encoding verificado (UTF-8 sem BOM). Commit `f8728aa` com apenas os dois entregaveis.
