# Taxonomia de arquetipos -- numeros de suporte verificados

- **Data:** 2026-07-06
- **Plano:** plan-000088, Step 1
- **Fonte primaria:** `_output/research-logs/research-000087-perfis-de-uso-do-harness-exploratorio-vs-focado.md` (secoes "Resultados por fase" e "Arquetipos de fluxo")
- **Instrumento:** `_output/generated-scripts/mine_harness_flows.py` rodado contra `_output/briefs-index.md` (repo pai) e `fala-gavea/_output/briefs-index.md` (submodule)

## Como reproduzir

```
uv run python _output/generated-scripts/mine_harness_flows.py _output/briefs-index.md fala-gavea/_output/briefs-index.md
```

Notas de reproducao:

1. O script rodou sem falhas como preservado. Foi feita UMA modificacao minima e aditiva (plan-000088 step 1): um bloco que imprime as probabilidades condicionais P(proxima|atual) normalizadas por linha, com o n da linha. Sem ele, a lista "top transitions" trunca em 14 contagens brutas e nao permite verificar os n citados na pesquisa (n=36, n=23, n=27, n=11). Nenhuma logica de parsing ou desempate foi alterada (re-sort por timestamp + desempate por ordem do arquivo, ja conformes a Metodologia itens 1-2 da pesquisa 000087, pois `list.sort` do Python e estavel).
2. **Corpus congelado vs corpus atual:** o indice do repo pai ganhou 1 entrada APOS a janela da pesquisa -- a propria invocacao de research-000087 (2026-07-06 18:26). O corpus atual tem 97 entradas no repo pai; a pesquisa reporta 96 (24/abr a 30/jun). Para reconferir os numeros publicados, o script foi rodado tambem contra uma copia filtrada do indice sem as linhas de 2026-07 (corpus congelado). Todos os numeros abaixo referem-se ao **corpus congelado**, que reproduz a pesquisa; a unica fase afetada pela entrada extra e F4 (16 -> 17 invocacoes no corpus atual).

## Tamanho dos corpora

| Corpus | Pesquisa 000087 | Verificado | Status |
|---|---|---|---|
| Repo pai (briefs-index) | 96 invocacoes (24/abr - 30/jun) | 96 (congelado); 97 no indice atual, +1 = a propria research-000087 em 06/jul | OK (congelado) |
| fala-gavea (briefs-index) | 120 invocacoes (17/jun - 1/jul) | 120 | OK |

## Suporte dos 5 arquetipos

| # | Arquetipo | Suporte citado na pesquisa | Verificado pelo script / grep | Status |
|---|---|---|---|---|
| 1 | Fluxo de bootstrap (`advise/research -> plan -> implement^n`) | F1; 3 sessoes iniciam com advise; implement->implement 75% | Entry-point de sessao em F1: advise 3x; implement->implement 75% (6/8, n=8) | OK |
| 2 | Execucao por ondas de roadmap (`plan --roadmap -> (plan[wave item] -> implement)^n`) | 12 planos fala-gavea com `source: roadmap-NNN Wave N item M` + 4 planos no repo pai; plan->plan 40% em F2 | fala-gavea: 15 planos com header `source: roadmap-NNN` (8 com "Wave N" explicito na linha + 7 com `source: roadmap-000151`, roadmap organizado em 3 waves mas sem o texto "Wave" na linha source). Repo pai: 4 planos (roadmap-000026 W0-1, roadmap-000028 W0-1 e W1-1, roadmap-000071 Wave 0). plan->plan em F2: 40% (8/20, n=20) | DIVERGE no numero fala-gavea (ver Divergencias); repo pai OK; plan->plan OK |
| 3 | Loop de grooming (`reflect -> (research|plan) -> plan -> implement`) | 11 reflections em F3, 8 seguidas de research ou plan na mesma sessao | 11 arquivos em `fala-gavea/_output/reflections/`; linha reflect em F3: n=11 transicoes de saida, das quais plan 4 + research 4 = 8 | OK |
| 4 | Micro-loop de feature (`(research -> plan -> implement)^n` na mesma sessao) | P(plan|research)=70% em F3; assinaturas de sessao com 2-4 repeticoes do trio | research em F3: n=23, plan 70% (16/23); assinaturas de sessao com o trio repetido presentes na saida (ex. `implement > research > plan > implement > research > plan > implement > ...`) | OK |
| 5 | Fluxo de relato (`research -> communicate`; communicate -> research 100%, n=2, em F3) | communicate->research 100%, n=2 (F3); cauda F4 dominada por research/communicate | communicate em F3: n=2, research 100% (2/2); F4: research 31%, communicate 25%, plan 19% | OK |

## Probabilidades de transicao P(proxima|atual)

Todas verificadas pela saida do bloco row-normalized do script (corpus congelado).

| Transicao | F1 | F2 | F3 | Status vs pesquisa |
|---|---|---|---|---|
| plan -> implement | 71% (5/7, n=7) | 55% (11/20, n=20) | 50% (18/36, n=36) | OK |
| implement -> implement | 75% (6/8, n=8) | 29% (4/14, n=14) | 15% (4/27, n=27) | OK |
| plan -> plan | 14% (1/7) | 40% (8/20) | 17% (6/36) | OK |
| research -> plan | 100% (2/2, n=2) | 33% (2/6, n=6) | 70% (16/23, n=23) | OK |
| reflect -> plan / reflect -> research | -- | 60% / 40% (3/5 e 2/5, n=5) | 36% / 36% (4/11 e 4/11, n=11) | OK |
| communicate -> research | -- | -- | 100% (2/2, n=2) | OK |

## Metricas por fase (corpus congelado)

| Metrica | F1 Exploracao | F2 Transicao | F3 Execucao focada | F4 Relato | Status |
|---|---|---|---|---|---|
| Periodo | 24/abr - 10/jun | 10 - 17/jun | 17/jun - 1/jul | 19 - 30/jun | OK |
| Invocacoes | 25 | 55 | 120 | 16 | OK |
| Dias ativos (inv/dia ativo) | 8 (3.1) | 6 (9.2) | 13 (9.2) | 7 (2.3) | OK |
| Sessoes (inv/sessao) | 7 (3.6) | 10 (5.5) | 18 (6.7) | 7 (2.3) | OK |
| Skills distintas | 5 | 4 | 10 | 6 | OK |
| Top-3 skills | implement 48%, plan 28%, advise 12% | plan 44%, implement 35%, research 13% | plan 34%, implement 25%, research 22% | research 31%, communicate 25%, plan 19% | OK |
| STARTED orfaos | 3 (12%) | 7 (13%) | 8 (7%) | 3 (19%) | OK |
| Briefs encadeando artefato | 16% | 27% | 26% | 12% | OK |
| Commits git no periodo | ~40 | ~134 | 396 | ~34 | NAO verificado neste passo (fonte: git log, tomado de research-000087) |

Contraste de perfis usado no texto: 6.7 inv/sessao (F3) vs 2.3 inv/sessao (F4) -- ambos verificados.

## Divergencias

1. **Suporte do arquetipo 2 (ondas de roadmap) no fala-gavea: pesquisa diz 12, verificado 15 (ou 8, dependendo do criterio).** Contagem por grep em `fala-gavea/_output/plans/*.md`: 15 arquivos de plano tem header `source:` referenciando um roadmap; destes, 8 trazem "Wave N" explicito na linha (roadmaps 000071, 00001, 000088) e 7 trazem apenas `source: roadmap-000151` (roadmap que e organizado em 3 waves, mas cuja linha source nos planos 000152-000158 nao repete o texto "Wave"). Nao ha criterio que reproduza exatamente 12; o numero da pesquisa provavelmente foi contado com um padrao intermediario nao registrado. **Recomendacao para o texto:** citar "15 planos do fala-gavea com `source:` apontando para um roadmap (8 deles com item de wave explicito na linha) + 4 planos no repo pai", ou manter 12 apenas se marcado como numero da pesquisa original nao reproduzido. A direcao do achado (suporte de dois digitos ao encadeamento roadmap->plano no perfil focado) permanece valida.
2. **Corpus do repo pai cresceu de 96 para 97 apos a pesquisa** (entrada da propria research-000087, 06/jul, cai em F4: 16 -> 17 invocacoes no indice atual). Nao e erro da pesquisa: os numeros publicados referem-se a janela 24/abr - 30/jun e reproduzem exatamente no corpus congelado (indice filtrado sem linhas de 2026-07). Qualquer re-execucao futura do script contra o indice vivo vai divergir em F4; usar o corte <= 30/jun para citar os numeros publicados.
3. Nenhuma outra divergencia: todos os demais numeros (5 arquetipos exceto o item 1 acima, 6 linhas de transicao, metricas F1-F4) reproduzem exatamente.
