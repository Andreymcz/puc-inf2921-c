# DONE | 2026-07-07 12:08 UTC | Plan 000088 | INF2921-Grupo-C | 2026-07-06 19:53 UTC | Follow-ups research-000087: taxonomia de arquétipos + figura de timeline | Review: light
plan_format_version: 1

source: research-000087
spawned: communication-000093

## Brief

Executar os dois follow-ups de alta/média prioridade da pesquisa 000087 ("Perfis de uso do harness: exploratório vs focado"), ambos entregáveis de escrita para o texto de doutorado:

1. **[HIGH — Rec 1]** Reportar a taxonomia de 5 arquétipos de fluxo (bootstrap, ondas de roadmap, loop de grooming, micro-loop de feature, fluxo de relato) como uma seção autossuficiente de texto, com contagens de suporte e a regra de identificação operacional. É a resposta direta à pergunta de pesquisa "que outros fluxos emergem além de research → plan → implement".
2. **[Follow-up UX do reviewer]** Produzir a figura de timeline com faixas paralelas (repo pai `puc-inf2921-c` × submodule `fala-gavea`) que transforma a concorrência intra-sujeito F3‖F4 no argumento visual mais forte do texto.

> **Escopo:** entregáveis de redação para o texto de doutorado, não features de software. Todos os passos são doc-only (`Tests: N/A`). A fonte primária de conteúdo é `research-000087` — o plano **cita e reestrutura** o que já foi minerado, não re-minera do zero (o script de mineração já está preservado em `_output/generated-scripts/mine_harness_flows.py`).

---

## Context

### Fontes disponíveis

| Fonte | Conteúdo relevante |
|-------|-------------------|
| `_output/research-logs/research-000087-perfis-de-uso-do-harness-exploratorio-vs-focado.md` | Fonte primária: taxonomia dos 5 arquétipos (§"Arquétipos de fluxo"), contagens de suporte, regra de identificação, tabela de resultados por fase (F1–F4), matriz de transições, achado central intra-sujeito, ameaças à validade |
| `_output/generated-scripts/mine_harness_flows.py` | Script de mineração preservado (Rec 4) — produz contagens de skills, sessões, transições por perfil. Fonte reproduzível dos números de suporte |
| `_output/briefs-index.md` (96 inv.) + `fala-gavea/_output/briefs-index.md` (120 inv.) | Logs primários dos dois perfis — input do script de mineração |
| `relatorio/relatorio-inf2921-grupo-c.tex` + `.md` | Texto colaborativo da disciplina/doutorado onde a seção e a figura podem ser integradas (destino de publicação candidato) |

### Decisões de escopo herdadas da pesquisa (não re-litigar)

- Narrativa em 4 fases ancoradas em eventos: F1 exploração → F2 transição → F3 execução focada → F4 cauda de relato. **F3 e F4 são concorrentes** (fluxos paralelos por repo, não timeline global) — este é o eixo do argumento causal.
- Enquadramento de pesquisa de doutorado: metodologia reproduzível + ameaças à validade em formato MSR.
- **Passe de privacidade/LGPD obrigatório (Rec 3)** antes de qualquer citação verbatim de briefs, reflections ou decisões vindas de WhatsApp — nomes de colegas e domínio de relatos de segurança cidadã. Ver Step 4.

### Alvo de saída

- Seção de taxonomia: arquivo Markdown standalone em `_output/communication/` (reutilizável), com opção de integração no `relatorio/` (Step 5).
- Figura de timeline: diagrama Mermaid `gantt` (renderizável em Markdown/PDF sem dependências externas), acompanhado de uma versão textual-fallback acessível.

---

## Steps

### Step 1: Verificar e congelar os números de suporte da taxonomia

Rodar o script de mineração preservado contra os dois `briefs-index.md` para reconfirmar as contagens de suporte que aparecerão na seção de texto (evitar copiar números do relatório de pesquisa sem verificação — a Rec 4 exige reprodutibilidade). Registrar num arquivo de apoio os números exatos por arquétipo: suporte de cada um dos 5 arquétipos, as probabilidades condicionais de transição citadas (plan→implement, implement→implement, research→plan, reflect→plan/research), e as métricas por fase.

Se o script não rodar como está (parsing de índice, empates de timestamp), corrigir minimamente e anotar a correção — a regra de re-sort + desempate por ordem de arquivo já está documentada na §Metodologia da pesquisa 000087 (itens 1–2).

- **Files**: `_output/generated-scripts/mine_harness_flows.py` (modify, apenas se necessário), `_output/tmp/taxonomia-support-counts.md` (create — tabela de números verificados)
- **References**: `_output/research-logs/research-000087-perfis-de-uso-do-harness-exploratorio-vs-focado.md`
- **Verify**: script roda com `uv run python _output/generated-scripts/mine_harness_flows.py <path-repo-pai> <path-fala-gavea>` e produz contagens; `taxonomia-support-counts.md` lista o suporte dos 5 arquétipos e ≥4 probabilidades de transição, conferidos contra a §"Arquétipos de fluxo" da pesquisa
- **Tests**: N/A (script analítico de uso único; sem código de produção)
- [x] Done

---

### Step 2: Escrever a seção de texto "Taxonomia de arquétipos de fluxo"

Criar a seção autossuficiente de texto (Rec 1) em Markdown, estruturada para publicação acadêmica. Deve conter, para cada um dos 5 arquétipos:

1. **Nome + assinatura de sequência** (ex.: `advise/research → plan → implement^n`).
2. **Descrição** do que o fluxo representa no comportamento do desenvolvedor.
3. **Contagem de suporte** (dos números verificados no Step 1, não copiados às cegas).
4. **Exemplo âncora** (artefato concreto: ex. plano 000001 tttc-poc para bootstrap; reflection-000086 para grooming).

Ordem e conteúdo dos 5 arquétipos (da pesquisa 000087):
- **Bootstrap** — `advise/research → plan → implement^n` (F1; 3 sessões iniciam com advise; implement→implement 75%).
- **Ondas de roadmap** — `plan --roadmap → (plan[wave item] → implement)^n` (12 planos fala-gavea + 4 repo pai com `source: roadmap-NNN Wave N`; explica plan→plan 40% em F2).
- **Loop de grooming** — `reflect → (research|plan) → plan → implement` (11 reflections em F3, 8 seguidas de research/plan na mesma sessão).
- **Micro-loop de feature** — `(research → plan → implement)^n` (P(plan|research)=70% em F3; a unidade de trabalho do perfil focado).
- **Fluxo de relato** — `research → communicate` (communicate→research 100%, n=2; harness como arquivo consultável).

Abrir a seção declarando a **regra de identificação operacional**: subsequência (com repetições consecutivas colapsadas) dentro de uma sessão, sessão = eventos separados por ≤3h, contagens de suporte indicadas. Fechar com o achado qualitativo do **papel duplo de /reflect** (ideação/pivô no perfil exploratório vs checkpoint ancorado em artefatos no focado) — este é o insight que diferencia os perfis e conecta a taxonomia à pergunta comparativa.

Enquadrar como resposta explícita à pergunta de pesquisa: "além do canônico research → plan → implement, emergem 5 arquétipos recorrentes."

- **Files**: `_output/communication/2026-07-06/taxonomia-arquetipos-fluxo.md` (create)
- **References**: `_output/research-logs/research-000087-perfis-de-uso-do-harness-exploratorio-vs-focado.md`, `.claude/references/general/report-conventions.md`
- **Depends on**: Step 1
- **Verify**: os 5 arquétipos presentes, cada um com assinatura + descrição + suporte + exemplo âncora; regra de identificação declarada no topo; parágrafo do papel duplo de /reflect no fechamento; números batem com `taxonomia-support-counts.md`
- **Tests**: N/A (entregável de redação)
- **Docs**: o próprio arquivo é o artefato final
- [x] Done

---

### Step 3: Produzir a figura de timeline com faixas paralelas

Criar a figura que representa as 4 fases como faixas temporais, com os dois repositórios (`puc-inf2921-c` e `fala-gavea`) como **trilhas paralelas**, tornando visível que **F3 e F4 ocorrem nas mesmas semanas** (o controle intra-sujeito — argumento causal central). Usar um diagrama Mermaid `gantt` (renderiza em Markdown/PDF via mermaid-cli ou VS Code sem assets externos), com:

- Section "puc-inf2921-c (perfil exploratório)": F1 Exploração (24/abr–10/jun), F2 Transição (10–17/jun), F4 Cauda de relato (19–30/jun).
- Section "fala-gavea (perfil focado)": F3 Execução focada (17/jun–1/jul).
- Alinhamento visual que evidencie a sobreposição temporal F3‖F4 (mesmas semanas, mesmo desenvolvedor, mesma versão do harness, perfis opostos: 6.7 vs 2.3 inv/sessão).

Incluir imediatamente abaixo do diagrama uma **legenda + versão textual-fallback acessível** (tabela período→fase→perfil→métrica-chave) para o caso de o renderizador não suportar Mermaid e para acessibilidade — a §Ameaças-à-validade da pesquisa e a boa prática MSR pedem que a figura não seja o único portador da informação.

Anotar sob a figura a leitura de uma frase: a sobreposição temporal é o que sustenta "o tipo de tarefa molda a forma do fluxo" em vez de "maturidade/tempo" (confundidos).

- **Files**: `_output/communication/2026-07-06/timeline-faixas-paralelas.md` (create — diagrama Mermaid + fallback textual)
- **References**: `_output/research-logs/research-000087-perfis-de-uso-do-harness-exploratorio-vs-focado.md` (§Resultados por fase, §"Achado central")
- **Depends on**: Step 1
- **Verify**: diagrama Mermaid `gantt` válido com 2 sections (uma por repo) e 4 tarefas de fase datadas; sobreposição F3/F4 visível; legenda + tabela textual-fallback presentes; frase de leitura do argumento causal presente
- **Tests**: N/A (entregável de figura)
- **Docs**: o próprio arquivo é o artefato final
- [x] Done

---

### Step 4: Passe de privacidade/LGPD sobre os dois entregáveis

Antes de qualquer integração no texto de publicação, revisar a seção de taxonomia (Step 2) e a figura (Step 3) contra a Rec 3 da pesquisa: **nenhuma citação verbatim** de briefs, reflections ou decisões vindas de WhatsApp que exponha nomes de colegas ou conteúdo de relatos de segurança cidadã (LGPD). Os exemplos âncora devem referenciar artefatos por **ID** (plano 000001, reflection-000086), não por conteúdo textual sensível. Se algum exemplo citar nome próprio ou trecho de mensagem privada, substituir por referência de ID ou paráfrase anonimizada.

Registrar o resultado do passe (aprovado / itens corrigidos) em uma nota curta no rodapé de cada arquivo ou num log de apoio.

- **Files**: `_output/communication/2026-07-06/taxonomia-arquetipos-fluxo.md` (modify, se necessário), `_output/communication/2026-07-06/timeline-faixas-paralelas.md` (modify, se necessário)
- **References**: `_output/research-logs/research-000087-perfis-de-uso-do-harness-exploratorio-vs-focado.md` (§Recommendations Rec 3, §Ameaças-à-validade DATA), `product-design/project/security-checklists.md § Checklist D — Document Privacy`
- **Depends on**: Step 2, Step 3
- **Verify**: nenhum nome próprio de colega nem trecho de WhatsApp verbatim nos dois arquivos; exemplos referenciam artefatos por ID; nota de passe de privacidade registrada
- **Tests**: N/A
- [x] Done

---

### Step 5: (Opcional) Integrar seção e figura no relatório de doutorado/disciplina

Se o usuário confirmar que os entregáveis vão para o texto colaborativo, inserir a seção de taxonomia e a figura de timeline como uma nova subseção do `relatorio/relatorio-inf2921-grupo-c.md` (e espelhar no `.tex` se o LaTeX for o formato de entrega). Localização sugerida: uma subseção metodológica sobre "perfis de uso do harness" no processo de elaboração (seção 2 do relatório) ou um apêndice de pesquisa. Converter o Mermaid para uma figura estática (PNG/SVG via mermaid-cli) se o pipeline LaTeX não renderizar Mermaid nativamente.

Este step é **condicional** — só executar após confirmação do usuário sobre o destino, já que a decisão inicial foi manter os entregáveis como artefatos standalone primeiro.

- **Files**: `relatorio/relatorio-inf2921-grupo-c.md` (modify), `relatorio/relatorio-inf2921-grupo-c.tex` (modify, se LaTeX), `relatorio/figuras/timeline-faixas-paralelas.png` (create, se conversão necessária)
- **References**: `relatorio/relatorio-inf2921-grupo-c.tex`
- **Depends on**: Step 4
- **Verify**: subseção presente no relatório com a seção de taxonomia e a figura (ou referência à figura estática); renderiza em PDF sem erros
- **Tests**: N/A
- **Docs**: integração no artefato de relatório final
- [ ] Done (condicional — aguarda confirmação do usuário)

---

## Artifact Index

| Artifact | Path | Status |
|----------|------|--------|
| Números de suporte verificados | `_output/tmp/taxonomia-support-counts.md` | Pending (Step 1) |
| Seção de taxonomia (Rec 1) | `_output/communication/2026-07-06/taxonomia-arquetipos-fluxo.md` | Pending (Step 2) |
| Figura de timeline (follow-up UX) | `_output/communication/2026-07-06/timeline-faixas-paralelas.md` | Pending (Step 3) |
| Integração no relatório (opcional) | `relatorio/relatorio-inf2921-grupo-c.md` | Pending (Step 5, condicional) |

---

## Notes

- **Fonte única de conteúdo**: o relatório de pesquisa 000087 já contém toda a análise; estes steps são de *redação e figura*, não de nova mineração. O Step 1 apenas re-verifica os números de suporte para a reprodutibilidade exigida pela Rec 4.
- **Rec 3 (privacidade) é blocking para publicação** — o Step 4 deve passar antes de qualquer integração no texto (Step 5).
- **Mermaid `gantt` foi escolhido** por renderizar em Markdown/PDF sem assets externos (CSP-safe, offline, alinha com o princípio de dados/ferramentas locais do projeto). O fallback textual garante acessibilidade e robustez de renderização.
- **Steps 2 e 3 são independentes** (ambos dependem só do Step 1) — podem ser executados em paralelo por subagentes distintos.
- As demais recomendações da pesquisa 000087 (Rec 2 achado causal no texto, Rec 5 threats-to-validity, Rec 6 telemetria de fluxo no harness) **não** estão neste plano — foco nos dois follow-ups HIGH/UX pedidos. Rec 2 e 5 são conteúdo que naturalmente acompanha a seção de taxonomia quando integrada ao texto completo; podem virar um plano seguinte.

---

## Execution Summary (auto mode, 2026-07-06/07)

**Steps: 4/4 executados com SUCCESS (Step 5 condicional NÃO executado — usuário optou por manter os entregáveis standalone). Iterações: 4 de 20 (Steps 2 e 3 em subagentes paralelos). Rollback branch: `pre-plan-000088`.**

| Step | Resultado | Commit |
|------|-----------|--------|
| 1 — Verificar números de suporte | SUCCESS (script rodou as-is; 1 bloco aditivo de P(next\|current)) | `9d56f0f` |
| 2 — Seção de taxonomia | SUCCESS (subagente paralelo; commit pelo orquestrador) | `a9b593a` |
| 3 — Figura de timeline | SUCCESS (subagente paralelo; commit pelo orquestrador) | `6bef5a4` |
| 4 — Passe privacidade/LGPD | SUCCESS (aprovado, 0 correções) | `f8728aa` |
| 5 — Integração no relatório | NÃO executado (condicional; decisão do usuário 2026-07-06: manter standalone) | — |

**Artefatos produzidos:**
- `_output/tmp/taxonomia-support-counts.md` — números verificados (corpus congelado 96/120)
- `_output/communication/2026-07-06/taxonomia-arquetipos-fluxo.md` — seção autossuficiente (Rec 1)
- `_output/communication/2026-07-06/timeline-faixas-paralelas.md` — Mermaid gantt + fallback textual (follow-up UX)

**Quality gate (check-000090 validate, check-000091 review, test-runner):** testes 12/12 PASS; review depth light sem findings críticos (3 advisories LOW, deferidos: "(sic)" no roadmap-00001 antes da integração na tese; manter flag "não verificado" na linha de commits; nota de privacidade no tmp se promovido). Generator-critic: 0/2 iterações, nenhum finding crítico. Falhas do standards-checker são todas pré-existentes e fora do escopo do plano (templates de conventions, paths de SKILL.md, telemetria, vulns em fala-gavea-seguranca/python-scaffold, worktree órfão do repo pai).

**Learnings-chave (progress file):**
- Divergência material: suporte do arquétipo "ondas de roadmap" no fala-gavea é 15 planos (8 com Wave explícito), não os 12 do relatório de pesquisa — texto usa os verificados e marca o 12 como não reproduzido.
- O `briefs-index.md` do repo pai é vivo: reproduzir os números publicados exige cutoff <= 30/jun (a entrada da própria research-000087 desloca F4 de 16 para 17).
- `python` não está no PATH do Git Bash desta máquina; usar `uv run python`.
