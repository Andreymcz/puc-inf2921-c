# Research 000086 | -X | 2026-06-30 21:54 UTC | GaveaLab PoC Fase 2 -- detalhamento tecnico para relatorio
tags: gavealab-poc, crux-detection, embeddings, umap, semantic-clustering, report-writing

---

## User Brief

communication artifacts para melhorar a escrita esta sessao. quero adicionar detalhes mais tecnicos das intencoes, planos researchers que foram executados e implementados durante esta fase

Fase 2 - GaveaLab PoC: analise semantica de conjuntos de relatos (jun/2026)
O GaveaLab Poc foi uma exploracao de ferramentas mais deterministicas para analise semantica
de textos, que nao dependessem tanto de LLMs. A ferramenta foi mais voltada para o caso de uso
de um pesquisador do GaveaLab que precisa analisar um estudo feito com relatos de cidadaos,
agrupar topicos em comum e detectar divergencias entre relatos do mesmo topico (mesma
solucao que o T3C, so que utilizando metodos de mapeamento semantico e clusterizacao).
O prototipo gerado substituiu a dependencia total de llms do T3C por tecnicas de mapeamento
semantico e clusterizacao de relatos, utilizando uma stack mais enxuta: Streamlit, SQLite,
SentenceTransformers, ChromaDB e Ollama. Foi implementando um fluxo de upload de
relatos e clusterizacao visual via UMAP (MCINNES; HEALY; MELVILLE, 2018).
(a) Temas automaticos (b) Visualizacao de divergencias (c) Clusterizacao semantica dos
relatos
Figura 3: Prototipo GaveaLab Prototipo de analise semantica de relatos enviados pelo pesqui-
sador Gavealab; (a) A pagina temas automaticos lista os temas inferidos, apontando os relatos
que fazem parte do tema, e as reivindicacoes para cada subtema tambem inferido.; (b) a pagina
de opinioes divergentes mostra a analise de divergencia nos subtopicos extraidos pelo sistema;
(c) a pagina visualizar clusters permite o pesquisador controlar os parametros da clusterizacao,
que e guiada pelo territorio do relato

## Agent Interpretation

The user wants a more technically precise rewrite of the "Fase 2 -- GaveaLab PoC" section of their
course report (PUC-Rio, INF2921), grounded in the actual research and plan artifacts executed
during that phase of the project, rather than the current high-level summary. The rewrite needs
to correctly attribute which pipeline stages were actually redesigned (vs. inherited unchanged
from tttc-poc), name the concrete models/parameters used, and reference the source artifacts
(research-000014, roadmap-000007, plan-000008/009/010/011/012/013/016) so the report is
auditable against the codebase's own history.

## Files Referenced

- `_output/research-logs/research-000014-local-crux-analysis-divergent-opinions.md`
- `_output/roadmaps/roadmap-000007-gavealab-claims-poc.md`
- `_output/plans/plan-000008-gavealab-poc-scaffold.md`
- `_output/plans/plan-000010-gavealab-poc-auto-topics.md`
- `_output/plans/plan-000011-gavealab-poc-claims.md`
- `_output/plans/plan-000013-gavealab-poc-cruxes.md`
- `_output/plans/plan-000016-gavealab-poc-umap-visualization.md`
- `product-design/project/product-design-as-coded.md` (section "0. GaveaLab PoC (sibling project)")
- `product-design/project/product-design-as-intended.md` (Decision D-005)

---

## Q&A Log

### Q1: How should the "Fase 2 -- GaveaLab PoC" report section be rewritten with accurate technical detail, citing the research and plans actually executed?

**Answer**: The rewrite below is grounded in the artifact chain research-000014 -> roadmap-000007 ->
plan-000008/009/010/011/012/013/016, verified against `product-design-as-coded.md`. The
research-reviewer agent flagged one critical scoping correction before this answer was finalized:
**only the divergence-detection (crux) stage was redesigned away from LLM dependency** -- topic
discovery and claims extraction kept the original LLM-gated design from roadmap-000007/D-005,
just running on local Ollama (`qwen3:8b`) instead of cloud Claude. The embedding-model swap
(`nomic-ai/nomic-embed-text-v1` -> `intfloat/multilingual-e5-large`) is also scoped to
gavealab-poc only; kb-qa kept nomic-embed unchanged (research-000014 R4). BERTopic/HDBSCAN
clustering (research-000014 R1/R6) was a recommendation, never implemented -- the as-coded
divergence detection groups claims by the `territory` column, not by an unsupervised clustering
algorithm.

Suggested rewrite (Portuguese, ASCII-safe, ready to paste into the report):

> **Fase 2 -- GaveaLab PoC: analise semantica de conjuntos de relatos (jun/2026)**
>
> O GaveaLab PoC partiu de uma investigacao preparatoria (research-000014) sobre como reduzir
> a dependencia do pipeline do T3C (Talk to the City) em relacao a LLMs de nuvem (Claude). Essa
> investigacao decompos o pipeline do T3C em tres estagios -- (1) extracao de claims a partir do
> relato bruto, (2) agrupamento semantico das claims em temas/subtemas, e (3) deteccao de pontos
> de divergencia (cruxes) entre claims do mesmo subtema -- e mostrou que apenas os estagios 1 e 3
> dependem estritamente de raciocinio por LLM; o estagio 2 e uma operacao puramente vetorial.
>
> A partir dessa analise, o prototipo (roadmap-000007, plan-000008 a plan-000016) reimplementou
> o fluxo do T3C como uma aplicacao Streamlit monolitica, mantendo a extracao de topicos e claims
> via LLM local (Ollama, `qwen3:8b`, endpoint compativel com a API OpenAI, thinking mode
> desabilitado para reduzir latencia -- plan-000008, plan-000010, plan-000011), porem substituindo
> a etapa de deteccao de divergencias -- antes inteiramente delegada ao LLM no T3C -- por uma
> abordagem de mapeamento semantico (plan-000013): calculo de distancia de cosseno entre os
> centroides de embedding de grupos territoriais, acionando o LLM local apenas para rotular, em
> uma frase, os pares de grupos ja identificados como divergentes (limiar `DIVERGENCE_THRESHOLD
> = 0.25`). Essa redesenho transforma uma tarefa aberta e cara ("encontrar todos os cruxes") em
> uma tarefa estreita e barata, aplicada apenas aos subtemas efetivamente divergentes.
>
> Para essa etapa, o pipeline GaveaLab passou a usar `intfloat/multilingual-e5-large` em vez de
> `nomic-ai/nomic-embed-text-v1` (mantido na ferramenta kb-qa), por apresentar desempenho
> superior em clusterizacao de opinioes em portugues. A stack do prototipo combina Streamlit
> (interface), SQLite via `GaveaLabWorkspace` (persistencia de sessoes e resultados),
> SentenceTransformers (embeddings) e Ollama (inferencia local), mantendo o mesmo backend de
> LLM ja usado no tttc-poc.
>
> A pagina "Visualizar clusters" (plan-000016) projeta os embeddings de 1024 dimensoes
> (multilingual-e5-large) das claims extraidas em duas dimensoes via UMAP (MCINNES; HEALY;
> MELVILLE, 2018), com parametros `n_neighbors=15`, `min_dist=0.1` e metrica de cosseno,
> ajustaveis interativamente por sliders na barra lateral. Cada ponto representa uma claim,
> colorida pelo territorio de origem; ao passar o mouse sao exibidos o texto da claim e o subtema
> associado -- permitindo ao pesquisador inspecionar visualmente se os territorios formam
> agrupamentos semanticos distintos, de forma complementar ao sinal numerico de distancia de
> cosseno usado na deteccao de cruxes.
>
> (a) Temas automaticos (b) Visualizacao de divergencias (c) Clusterizacao semantica dos relatos
>
> Figura 3: Prototipo GaveaLab -- prototipo de analise semantica de relatos enviados pelo
> pesquisador GaveaLab. (a) A pagina "Temas automaticos" lista os temas inferidos pela LLM
> (plan-000010), aponta os relatos associados a cada tema e as claims extraidas para cada
> subtema (plan-000011). (b) A pagina "Opinioes divergentes" mostra, para cada subtema, a
> distancia de cosseno entre os centroides de embedding dos grupos por territorio e o rotulo de
> divergencia gerado pela LLM apenas quando esse limiar e ultrapassado (plan-000013). (c) A
> pagina "Visualizar clusters" permite ao pesquisador controlar interativamente os parametros de
> clusterizacao UMAP (n_neighbors, min_dist), com pontos coloridos pelo territorio do relato
> (plan-000016).

**Key corrections applied relative to the original draft** (per research-reviewer findings):
1. "Substituiu a dependencia total de LLMs" was overclaimed -- only crux detection (estagio 3) was
   redesigned; topic/claims extraction (estagio 1) is still LLM-driven, just local instead of cloud.
2. The embedding-model swap is scoped to gavealab-poc, not the whole repository (kb-qa kept
   nomic-embed-text-v1).
3. BERTopic/HDBSCAN is not mentioned as implemented -- it was a research-000014 recommendation
   (R1, R6) never adopted; the as-coded grouping is by `territory` column, not algorithmic
   clustering.
4. plan-000010/000011/000012 are cited briefly to explain why the "Temas automaticos" page still
   shows LLM-generated content, disambiguating point 1.
5. UMAP citation and concrete parameters (`n_neighbors=15`, `min_dist=0.1`, cosine metric) are
   sourced from plan-000016 and kept close to the original caption phrasing, which the review
   found already accurate.

---

## Recommendations Summary

| # | Priority | Recommendation |
|---|----------|----------------|
| R1 | HIGH | Scope the "reduced LLM dependency" claim explicitly to the divergence-detection (crux) stage; topic/claims extraction remained LLM-gated via local Ollama (`qwen3:8b`), per D-005 and plan-000010/011. |
| R2 | HIGH | Scope the embedding-model swap (`nomic-embed-text-v1` -> `multilingual-e5-large`) to gavealab-poc only; kb-qa retained nomic-embed unchanged (research-000014 R4). |
| R3 | MEDIUM | Do not present BERTopic/HDBSCAN as implemented; it is a research-000014 recommendation (R1, R6) that was not adopted. The as-coded divergence grouping is by the `territory` column. |
| R4 | MEDIUM | Cite plan-000010/000011/000012 briefly to acknowledge the unchanged, LLM-gated topic/claims/manual-categorization stages, supporting and disambiguating R1. |
| R5 | LOW | Keep the MCINNES; HEALY; MELVILLE (2018) UMAP citation and add the concrete parameters (`n_neighbors=15`, `min_dist=0.1`, cosine metric) from plan-000016, since they support the existing caption claim that the researcher controls clustering parameters. |
