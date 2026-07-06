# Research 000087 | DOCUMENT-O | 2026-07-06 18:26 | Perfis de uso do harness: exploratorio vs focado

tags: harness-usage, mining-de-artefatos, developer-profiles, seja, metodologia-pesquisa

## User brief

> Eu quero coletar toda informacao historica deste repositorio no que tange o perfil do desenvolvedor utilizando o harness seja. objetivo e mapear fluxos comuns que foram executados ao longo do projeto. research -> plan -> implement por exemplo e um fluxo natural, mas a pesquisa pergunta se outros fluxos emergem. podemos fazer 2 perfis: o perfil mais exploratorio que sao os artefatos deste projeto puc-inf2921-c, que visou gerar prototipos e acumular conhecimento sobre o dominio e o problema e o fala-gavea que foi focado em implementar uma solucao para um projeto bem definido. Qual o padrao dos 2 perfis e a diferenca / semelhanca entre eles?

## Agent interpretation

Minerar o historico completo de invocacoes de skills SEJA nos dois repositorios (puc-inf2921-c e submodule fala-gavea) a partir dos briefs, telemetria, cadeias `source:` nos planos, roadmaps, reflections e git log, para: (1) reconstruir os fluxos de skills efetivamente executados; (2) identificar fluxos recorrentes alem do canonico research -> plan -> implement; (3) caracterizar e comparar os perfis de uso "exploratorio" e "focado". Por decisao do usuario (Q&A abaixo), a analise adota narrativa em fases (exploracao -> transicao -> execucao focada, mais cauda de relato), enquadramento de pesquisa de doutorado (metodologia reproduzivel, implicacoes para design de harness) e mineracao completa (briefs + telemetria + qa-logs/reflections + git log).

## Files

- `_output/briefs-index.md` -- 96 invocacoes (2026-04-24 a 2026-06-30), log primario do perfil exploratorio
- `fala-gavea/_output/briefs-index.md` -- 120 invocacoes (2026-06-17 a 2026-07-01), log primario do perfil focado
- `_output/telemetry.jsonl` (62 eventos) e `fala-gavea/_output/telemetry.jsonl` (102 eventos) -- instrumento secundario
- `_output/plans/*.md` (63 planos) e `fala-gavea/_output/plans/*.md` (100 arquivos de plano) -- cadeias `source:`
- `_output/roadmaps/` (7) e `fala-gavea/_output/roadmaps/` (4)
- `_output/reflections/` (3) e `fala-gavea/_output/reflections/` (11)
- git log dos dois repos (260 commits / 68 dias; 396 commits / 14 dias)

---

## Q&A log

**Q1 (usuario):** Qual o padrao dos 2 perfis (exploratorio puc-inf2921-c vs focado fala-gavea) de uso do harness, e a diferenca / semelhanca entre eles? Que fluxos emergem alem de research -> plan -> implement?

**Q2 (agente, escopo):** Como classificar as ~40 entradas do puc-inf2921-c (10-17/jun) que sao prototipos do fala-gavea antes do repo dedicado existir?
**A2 (usuario):** Tratar como 3a fase: transicao (exploracao -> transicao -> execucao focada).

**Q3 (agente, escopo):** Qual o destino principal da analise?
**A3 (usuario):** Pesquisa de doutorado -- metodologia de mineracao, metricas reproduziveis, implicacoes para design de harness.

**Q4 (agente, escopo):** Profundidade da mineracao?
**A4 (usuario):** Mineracao completa -- briefs + telemetria + qa-logs + reflections + git log.

**A1 (agente):** ver secoes Resultados, Arquetipos de fluxo e Comparacao abaixo; sintese na Recommendations summary.

---

## Metodologia (reproduzivel)

1. **Log de eventos**: cada linha das tabelas `briefs-index.md` e um evento `(timestamp, skill, brief, status)`. Os indices NAO sao confiavelmente ordenados (verificado: linhas de 25/jun acima de linhas de 28/jun) -- a analise re-ordena explicitamente por timestamp; empates de timestamp (invocacoes em lote, ex. 3 implements as 14:43 de 16/jun) preservam a ordem do arquivo como criterio de desempate.
2. **Segmentacao de sessoes**: eventos consecutivos separados por <= 3h pertencem a mesma sessao. Sensibilidade (fala-gavea): 35 sessoes a 1h, 26 a 2h, 18 a 3h, 17 a 6h -- os arquetipos de fluxo descritos abaixo sao estaveis nos 4 cortes; apenas a granularidade muda.
3. **Matriz de transicoes**: pares consecutivos dentro de sessao, reportados como contagem bruta E probabilidade condicional P(proxima|atual) normalizada por linha (correcao de comparabilidade entre corpora de tamanhos distintos).
4. **Assinaturas de sessao**: sequencia de skills da sessao com repeticoes consecutivas colapsadas.
5. **Disciplina de encadeamento**: fracao de briefs que referenciam explicitamente artefato anterior (`source:`, `research-NNN`, `plan-NNN`, `roadmap-NNN`); verificacao contra os headers `source:` dos arquivos de plano completos (o indice trunca briefs em 80 chars -- como `source:` e prefixo, a deteccao no indice e conservadora mas nao simetrica).
6. **Triangulacao de instrumentos**: telemetry.jsonl cobre 62/96 (65%) e 102/120 (85%) dos eventos dos briefs; briefs-index e a fonte de verdade para fluxos (cobre invocacoes que quebraram antes do flush de telemetria); telemetria e a fonte para duracao e decisoes estruturadas.
7. **Cortes de fase** (ancorados em eventos, escolhidos post hoc): F1 ate 10/jun 12:00 UTC (ultima entrada gavealab-poc pura); F2 de 10/jun a 17/jun (primeira invocacao /reflect em 11/jun; prototipos fala-gavea via roadmaps 026/028/054/056/070/071); F3 a partir do bootstrap do repo dedicado (plan-000072 "fala-gavea scaffold e seja-setup", 17/jun); F4 = cauda de relato no repo pai (>= 19/jun). **F3 e F4 sao concorrentes** (fluxos paralelos por repo, nao uma linha do tempo global) -- isso e usado como controle intra-sujeito, ver Achado central.

## Resultados por fase

| Metrica | F1 Exploracao | F2 Transicao | F3 Execucao focada | F4 Relato |
|---|---|---|---|---|
| Periodo | 24/abr - 10/jun | 10 - 17/jun | 17/jun - 1/jul | 19 - 30/jun |
| Repo | puc-inf2921-c | puc-inf2921-c | fala-gavea | puc-inf2921-c |
| Invocacoes | 25 | 55 | 120 | 16 |
| Dias ativos (inv/dia ativo) | 8 (3.1) | 6 (9.2) | 13 (9.2) | 7 (2.3) |
| Sessoes (inv/sessao) | 7 (3.6) | 10 (5.5) | 18 (6.7) | 7 (2.3) |
| Skills distintas | 5 | 4 | 10 | 6 |
| Top-3 skills | implement 48%, plan 28%, advise 12% | plan 44%, implement 35%, research 13% | plan 34%, implement 25%, research 22% | research 31%, communicate 25%, plan 19% |
| STARTED orfaos | 3 (12%) | 7 (13%) | 8 (7%) | 3 (19%) |
| Briefs encadeando artefato | 16% | 27% | 26% | 12% |
| Commits git no periodo | ~40 | ~134 | 396 | ~34 |

Transicoes-chave, P(proxima|atual) com n da linha:

| Transicao | F1 | F2 | F3 | Leitura |
|---|---|---|---|---|
| plan -> implement | 71% (n=7) | 55% (n=20) | 50% (n=36) | espinha dorsal universal |
| implement -> implement | 75% (n=8) | 29% (n=14) | 15% (n=27) | F1: execucao passo-a-passo de um plano longo |
| plan -> plan | 14% | 40% | 17% | F2: enfileiramento de planos (roadmap em lote) |
| research -> plan | 100% (n=2) | 33% (n=6) | **70% (n=23)** | F3: research just-in-time acoplada ao proximo plano |
| reflect -> plan/research | -- | 60%/40% (n=5) | 36%/36% (n=11) | reflect como bifurcacao de re-orientacao |

## Arquetipos de fluxo (alem de research -> plan -> implement)

Regra de identificacao: subsequencia (com repeticoes colapsadas) dentro de uma sessao; contagens de suporte indicadas.

1. **Fluxo de bootstrap** -- `advise/research -> plan -> implement^n`: abre espaco de problema e executa um plano longo em passos (F1; 3 sessoes iniciam com advise; implement -> implement 75%). Ex.: plano 000001 tttc-poc executado por steps em dias e maquinas diferentes.
2. **Execucao por ondas de roadmap** -- `plan --roadmap -> (plan[wave item] -> implement)^n`: roadmap decompoe, planos consomem itens por onda. Suporte: 12 planos do fala-gavea com `source: roadmap-NNN Wave N item M` + 4 planos no repo pai; explica plan -> plan 40% em F2.
3. **Loop de grooming** -- `reflect -> (research|plan) -> plan -> implement`: reflexao ancorada em artefatos inventaria lacunas e alimenta o proximo ciclo. Suporte: 11 reflections em F3, das quais 8 sao seguidas por research ou plan na mesma sessao; ex. reflection-000086 (tabela CRUD vs roadmap) e reflection-000163.
4. **Micro-loop de feature** -- `(research -> plan -> implement)^n` repetido dentro da mesma sessao: a unidade de trabalho do perfil focado. Suporte: P(plan|research)=70% em F3; assinaturas de sessao com 2-4 repeticoes do trio (ex. sessoes de 21/jun e 26/jun).
5. **Fluxo de relato** -- `research -> communicate` (e communicate -> research 100%, n=2, em F3): o harness usado como arquivo consultavel para escrever material externo (F4 e cauda de F3).

Papel duplo de /reflect (achado qualitativo): no repo pai, reflect e captura de decisao estrategica free-form (reflection-000052 registra a conversa de WhatsApp do pivo "atlas da Amazonia -> zoom in Gavea"); no fala-gavea, reflect e checkpoint periodico ancorado em artefatos (inventario de gaps contra roadmap). Mesma skill, funcao distinta por perfil.

## Comparacao dos perfis

**Semelhancas**
- plan -> implement e a transicao #1 em todos os cortes (50-71%); plan e ~34-44% das invocacoes em qualquer fase de construcao.
- Roadmaps sao o mecanismo de decomposicao nos dois perfis.
- Abandono (STARTED orfao) concentra-se em plan e reflect, nunca em implement.
- O trio research/plan/implement soma 76-92% das invocacoes em todas as fases de construcao.

**Diferencas**
- **Papel da research**: exploratorio usa advise/research para ABRIR o espaco de problema (montante, ampla, 1 research vira 1+ roadmaps); focado usa research just-in-time, acoplada ao plano seguinte (P(plan|research)=70%, cadeias `source: research-NNN` em 13+ planos).
- **Superficie de harness**: 5 skills em F1 -> 10 em F3; skills de governanca (check, document, design, pending, explain spec-drift) so aparecem no perfil focado.
- **Disciplina de encadeamento**: 16% -> 26-27% de briefs com referencia explicita a artefato anterior.
- **Cadencia e taxa de conclusao**: 3.1 -> 9.2 inv/dia ativo; orfaos 12-14% -> 7%; commits ~3.8/dia -> 28.3/dia (metrica de throughput mediado pelo harness -- /implement auto-commita; nao separa autoria humana/agente).
- **Funcao do reflect**: ideacao/pivo (exploratorio) vs checkpoint de progresso (focado).

**Achado central (controle intra-sujeito)**: F3 e F4 ocorrem nas MESMAS semanas, com o mesmo desenvolvedor e a mesma versao do harness, e exibem perfis opostos (6.7 vs 2.3 inv/sessao; micro-loop research->plan->implement vs research->communicate). Isso sustenta a afirmacao de que **o tipo de tarefa molda a forma do fluxo** -- mais defensavel que atribuir a diferenca a maturidade ou tempo de uso, que sao colineares com aprendizado do desenvolvedor, evolucao do harness e pressao de prazo entre F1 e F3.

## Expert analysis (research-reviewer, profundidade standard)

Perspectivas avaliadas: ARCH, DATA, TEST, UX, OPS, DX (SEC dobrada em DATA).

| Perspectiva | Status | Sintese |
|---|---|---|
| ARCH (estrutura da analise) | Adotada c/ revisoes | Taxonomia de 4-5 arquetipos e modelo de fases sao solidos SE as fases forem ancoradas em eventos e a concorrencia F3/F4 for explicita (fluxos paralelos por repo, nao timeline global). Incorporado na Metodologia item 7. |
| DATA (integridade + privacidade) | Deferida -> tratada | Indice nao ordenado e empates de timestamp ameacavam as matrizes -- corrigido com re-sort + regra de desempate (Metodologia 1). Privacidade: briefs citam nomes de colegas e decisao vinda de WhatsApp; passe de redacao/consentimento OBRIGATORIO antes de citar verbatim em publicacao (LGPD). |
| TEST (validade metodologica) | Deferida -> tratada | Contagens brutas nao comparaveis entre corpora -- adicionadas probabilidades normalizadas; sensibilidade do corte de sessao (1h/2h/3h/6h) reportada; metricas de n pequeno (orfaos: 8 vs 12 eventos) mantidas descritivas, sem linguagem de significancia. |
| UX (comunicabilidade do resultado) | Adotada | Narrativa 3-fases+cauda legivel; recomendada figura de timeline com os dois repos como faixas paralelas, transformando a concorrencia F3/F4 no argumento mais forte. |
| OPS (observabilidade) | Adotada | O proprio gap de cobertura telemetria/briefs (65-85%) motiva a proposta de telemetria de assinatura de fluxo (session_id + arestas source_artifact + status terminal). |
| DX (reproducibilidade) | Adotada c/ revisoes | "Mineracao reproduzivel" exige pacote de replicacao: script de mineracao, regras de desempate, codebook dos arquetipos, log de eventos anonimizado. Script preservado (ver Follow-ups). |

## Ameacas a validade (formato padrao MSR)

- **Construto**: briefs registram os ARGUMENTOS da invocacao, nao o que a sessao realmente fez; commits/dia conflaciona atividade humana e do agente; STARTED orfao conflaciona crash e abandono.
- **Interna (confundidores)**: maturidade do projeto, aprendizado do desenvolvedor, evolucao da versao do harness e pressao de prazo sao colineares entre F1 e F3 -- parte da alta de encadeamento 16%->26% pode ser induzida por tooling (o harness passou a propagar `source:` automaticamente em algum ponto da janela; verificar changelog do harness antes de afirmar disciplina). A mecanica do `--roadmap` pode inflar a fatia de plan em F2 programaticamente. Mitigacao: controle intra-sujeito F3||F4.
- **Externa**: um unico desenvolvedor, um unico harness, um unico dominio (civic tech academico); generalizacao requer replicacao.
- **Conclusao**: n pequeno em varias celulas (F1 research n=2; F4 todas as linhas n<=2); indices truncam briefs em 80 chars.

---

## Recommendations summary

1. **[HIGH] Reportar a taxonomia de 5 arquetipos de fluxo** (bootstrap, ondas de roadmap, loop de grooming, micro-loop de feature, fluxo de relato) com contagens de suporte e regra de identificacao operacional -- e a resposta direta a pergunta "que outros fluxos emergem".
2. **[HIGH] Ancorar a claim causal no controle intra-sujeito F3||F4**: afirmar "tipo de tarefa molda a forma do fluxo" (sustentado) em vez de "maturidade, nao tempo" (confundido); enumerar explicitamente os confundidores nao removiveis, incluindo evolucao do harness na janela.
3. **[HIGH] Passe de privacidade/consentimento antes de qualquer citacao verbatim** de briefs, reflections ou decisoes vindas de WhatsApp no texto de doutorado (nomes de colegas; dominio de relatos de seguranca cidada; LGPD).
4. **[MEDIUM] Empacotar a metodologia como artefato de replicacao**: script de mineracao + regras de re-sort/desempate/lote + codebook dos arquetipos + log de eventos anonimizado + tabela de sensibilidade do corte de sessao.
5. **[MEDIUM] Estruturar limitacoes como threats-to-validity** (construto/interna/externa/conclusao) no texto final -- formato esperado por comites e revisores MSR.
6. **[LOW] Propor telemetria de assinatura de fluxo no harness** (session_id, arestas source_artifact, status terminal por invocacao), citando o gap de cobertura 65-85% medido aqui como evidencia-requisito.

## Follow-ups

- Script de mineracao preservado no scratchpad da sessao; copiar para `_output/generated-scripts/` se a Rec 4 for executada.
- Verificar no changelog do harness SEJA quando as skills de governanca e a propagacao automatica de `source:` foram introduzidas (Rec 2).
- Figura de timeline com faixas paralelas (repo pai x fala-gavea) para o texto do doutorado (sugestao UX do reviewer).
