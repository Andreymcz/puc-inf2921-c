# Research 000023 | research/ | 2026-06-11 01:35 UTC | Plataforma Fala Gávea — Visão, Casos de Uso e Roadmap
tags: product-roadmap, fala-gavea, architecture, lgpd, citizen-engagement

## User Brief

Vincular os novos documentos de casos de uso (`Casos_de_uso_10-06-2026_1.md` e `Casos_de_uso_10-06-2026_2.md`) ao estado atual do repositório (gavealab-poc). O objetivo é entender o que seria a Plataforma Fala Gávea e planejar um roadmap de produto baseado no conhecimento acumulado e nas ferramentas já implementadas.

Contexto da equipe (chat, 2026-06-10, Andrey):
> "dado as ferramentas que a gente já tem, de análise do discurso... Podíamos pensar em um fórum online (seguindo a ideia do fala gavea)... começa com esse fórum virtual que as pessoas chegam e colocam comentários... pode ser território e comentário... o motor do sistema de IA seria desde a aquisição dos dados, passando por um processo com um humano para auditar e verificar tudo... imagina reescrever o Twitter, só que com a possibilidade de ter outros tipos de interações/ações etc"

## Agent Interpretation

A pesquisa responde três perguntas encadeadas:
1. O que é a Plataforma Fala Gávea (síntese dos dois documentos de casos de uso)?
2. Como os casos de uso se mapeiam para o que o PoC já implementa?
3. Qual é o roadmap de produto — fases, prioridades, escopo para a entrega do curso?

## Files Consulted

- `knowledge/Casos_de_uso_10-06-2026_1.md` — Documento institucional (Núcleo de Prática Jurídica / PUC-Rio): UC-01 Consulta para tomada de decisão + UC-02 Coleta, Síntese e Gestão da Base de Conhecimento
- `knowledge/Casos_de_uso_10-06-2026_2.md` — Documento do grupo (GaveaLab): UC-01 Morador registra demanda + UC-02 Agente público analisa demandas
- `gavealab-poc/app.py`, `gavealab-poc/gavealab_poc/workspace.py`, `gavealab-poc/gavealab_poc/llm.py`, `gavealab-poc/gavealab_poc/pages/`
- `product-design/project/product-design-as-intended.md`

---

## Q&A

### Q1: O que é a Plataforma Fala Gávea e como os dois documentos se relacionam?

**A:** Os dois documentos descrevem a mesma plataforma a partir de ângulos complementares, formando dois anéis concêntricos:

**Anel Interno — Ferramenta de Análise (Document 1 / escopo do PoC)**

O Documento 1 (Núcleo de Prática Jurídica) especifica o GaveaLab como operador de dados: uma equipe que ingesta CSVs de relatos coletados externamente, roda o pipeline de IA (tópicos → claims → cruxes), valida resultados com revisão humana e publica uma base de conhecimento curada para gestores públicos, pesquisadores e investidores. Líderes comunitários atuam como auditores secundários.

Este anel está quase completamente implementado no PoC atual.

**Anel Externo — Plataforma de Participação Cidadã (Document 2 / visão futura)**

O Documento 2 adiciona uma camada de input cidadão em tempo real: moradores submetem problemas via app móvel ou tótem físico (texto, voz, foto); outros moradores confirmam a demanda coletivamente; o agente público recebe a demanda classificada, define prazo de resposta; o morador acompanha via notificações; encerramentos sem resolução geram métricas de "abandono institucional". Após intervenção, a plataforma monitora o impacto.

Este anel é um produto greenfield — não tem equivalente no PoC.

**Arquitetura resultante — dois subsistemas:**

```
┌─────────────────────────────────────┐
│  SUBSISTEMA A: Camada de Input Cidadão                │
│  (Document 2 / anel externo / futuro)                 │
│  App móvel, tótem físico, web público                 │
│  → submissão, validação coletiva, notificações        │
│  → produz: CSV estruturado de relatos                 │
└─────────────────┬───────────────────┘
                  │  contrato de dados: CSV com (id, text, territory, ...)
                  ▼
┌─────────────────────────────────────┐
│  SUBSISTEMA B: Motor de Análise + Dashboard           │
│  (Document 1 / anel interno / PoC atual)              │
│  Upload CSV → topics → claims → cruxes → UMAP         │
│  Revisão humana → publicação → painel decisores       │
└─────────────────────────────────────┘
```

O PoC implementa completamente o Subsistema B. O Subsistema A é a visão de longo prazo.

---

### Q2: Como os casos de uso se mapeiam para o PoC?

**Documento 1 — UC-02 (Coleta e Gestão da Base de Conhecimento):**

| Passo | PoC Atual | Gap |
|---|---|---|
| 1. Upload CSV | ✅ Página Upload | — |
| 2. Normalizar (text, território, metadados) | ✅ parcial — territory existe; normalização mínima | Pequeno |
| 3. Extrair claims individuais | ✅ Pipeline claims | — |
| 4. Agrupar em tópicos/subtópicos | ✅ Pipeline auto-topics | — |
| 5. Identificar opiniões divergentes | ✅ Página Cruxes | — |
| 6. Revisor humano edita títulos de cluster, realoca claims | ❌ Não implementado | **Gap médio** — maior lacuna |
| 7. Publicar versão aprovada para o dashboard | ❌ Não implementado | Gap pequeno (flag no DB) |

**Documento 1 — UC-01 (Consulta para Tomada de Decisão):**

| Funcionalidade | PoC Atual | Gap |
|---|---|---|
| Dashboard com clusters temáticos | ✅ Página UMAP | — |
| Filtros por tema/urgência | ❌ Sem filtros | Gap médio |
| Relatos representativos e opiniões divergentes | ✅ Cruxes | Parcial |
| Comparativo por subterritório | ❌ Sem filtro por territory | Gap médio |
| Exportar relatório estruturado | ❌ Sem export | Gap pequeno |
| Validação por líder comunitário | ❌ Sem perfil diferenciado | Gap grande (requer auth) |

**Documento 2 — UC-01 (Morador registra demanda):** Totalmente fora do escopo do PoC. Requer app móvel, sistema de notificações, backend persistente, autenticação cidadã.

**Documento 2 — UC-02 (Agente público analisa demandas):** Parcialmente coberto pelo PoC (visualização de clusters). Gaps: mapa de calor georreferenciado, narrativa síntese por cluster (além do UMAP), monitoramento de impacto pós-intervenção.

---

### Q3: Qual é o roadmap de produto?

O roadmap é estruturado em três fases, considerando o contexto do curso (entrega junho 2026) e a visão de longo prazo.

---

## Roadmap — Plataforma Fala Gávea

### Fase 0 — PoC Atual (concluída)

| Feature | Status |
|---|---|
| Upload CSV + sessão persistente (SQLite) | ✅ |
| Pipeline LLM: topics → claims → cruxes | ✅ |
| Categorização manual por temas | ✅ |
| Visualização UMAP (Plotly scatter) | ✅ |
| Dashboard todos os estudos | ✅ |
| Suporte a campo territory no CSV | ✅ |

**Resultado:** Motor de análise de discurso funcional. Demonstra o loop analítico completo sobre dados CSV.

---

### Fase 1 — Completar o Anel Interno (junho 2026, entrega do curso)

Objetivo: Completar o Document 1 UC-02 end-to-end e fechar as lacunas de usabilidade para o decisor.

| Feature | Prioridade | Complexidade | Justificativa |
|---|---|---|---|
| **Interface de revisão humana** — editar títulos de cluster, realocar claims entre tópicos | ALTA | Média | Maior gap do UC-02. Usa `st.data_editor`. Faz do PoC uma ferramenta de curadoria real |
| **Export CSV/JSON** dos resultados de análise | ALTA | Baixa | UC-01 passo 7. Já no roadmap (§0 do design intent) |
| **Registro de versão do pipeline** — gravar model_version + timestamp nos results | ALTA | Muito baixa | Requisito de auditabilidade do UC-02. 1 coluna no SQLite |
| **Estado "publicado"** na sessão (badge no dashboard) | MÉDIA | Baixa | UC-02 passo 7 — "consolida versão aprovada" |
| **Filtro por territory** no UMAP e no dashboard | MÉDIA | Média | Requisito ético explícito: segmentar asfalto vs. favela |
| **Transcrição de áudio via Whisper** (local) | MÉDIA | Média | UC-02 fluxo alternativo. `faster-whisper` roda localmente, C1 mantido |
| **Documentação LGPD mínima** no security checklist | ALTA | Documentação | Professores são do Dpto. de Direito. Mostrar consciência é obrigatório |

**Entregável da Fase 1:** Demonstração completa do loop Documento 1 — CSV entrada → pipeline IA → revisão humana → publicação → export de relatório. Simular input cidadão com CSV pré-coletado de relatos reais/sintéticos da Gávea/Rocinha.

---

### Fase 2 — Ponte entre os Anéis (pós-curso, Q3 2026)

Objetivo: Preparar a arquitetura para receber o Subsistema A (input cidadão) sem reescrever o motor de análise.

| Feature | Prioridade | Complexidade | Justificativa |
|---|---|---|---|
| **Separar "painel do pesquisador" do "painel do decisor"** — views diferenciadas | ALTA | Média | UC-01 Doc 1 exige visão estruturada para gestores; UC-02 Doc 2 exige dashboards distintos |
| **API REST sobre o motor de análise** (FastAPI) | ALTA | Média-alta | Permite que Subsistema A (cidadão) envie dados sem depender de CSV manual |
| **Autenticação básica** — perfis: operador, revisor, decisor | ALTA | Alta | Pré-requisito para expor externamente. Sem auth, não há produção |
| **Migração SQLite → PostgreSQL** | MÉDIA | Média | SQLite não suporta escritas concorrentes; necessário para multi-usuário |
| **Mapa de calor georreferenciado** (Folium/Plotly com lat/lon) | MÉDIA | Média | Visão territorial UC-01 Doc 2 |
| **Anonimização de relatos** antes do armazenamento permanente | ALTA | Média | Requisito LGPD. Stripping de PII via heurísticas ou LLM local |

**Entregável da Fase 2:** Motor de análise exposto como API. Pronto para integrar com o Subsistema A. Autenticação básica permite acesso externo seguro.

---

### Fase 3 — Subsistema A: Camada Cidadã (2026 Q4 / 2027)

Objetivo: Construir a interface cidadã do Document 2.

| Feature | Prioridade | Complexidade | Justificativa |
|---|---|---|---|
| **Web app público** (mobile-first) para submissão de relatos | ALTA | Alta | Core do UC-01 Doc 2 |
| **Input por voz** na interface cidadã | ALTA | Média | Inclusão de baixa alfabetização |
| **Validação coletiva** (upvoting de demandas) | ALTA | Média | Sinal de prioridade coletiva |
| **Notificações** (SMS/push) para o cidadão | MÉDIA | Alta | Acompanhamento da demanda |
| **Perfil de líder comunitário** com dashboard de auditoria | ALTA | Alta | Doc 1 UC-01 fluxo alternativo + Doc 2 UC-02 passo 3 |
| **Monitoramento de impacto** pós-intervenção | MÉDIA | Alta | Doc 2 UC-02 passo 5 |
| **Tótem físico** (interface offline simplificada) | BAIXA | Alta | Para comunidades com baixa conectividade |
| **Métricas de abandono institucional** | MÉDIA | Média | Demanda encerrada sem resolução → contador público |

**Entregável da Fase 3:** Plataforma completa Fala Gávea. Loop end-to-end: cidadão submete → IA analisa → humano valida → decisor age → impacto monitorado.

---

## Decisões Arquiteturais Destacadas

### A separação dos subsistemas é a decisão mais importante

O maior risco de produto é tentar construir a camada cidadã (Subsistema A) em Streamlit. Streamlit é síncrono, stateless, desktop-first e inadequado para mobile-first, offline, voice input e notificações assíncronas. A separação explícita de subsistemas A e B via contrato de dados (CSV/API) permite que o motor de análise (Streamlit + SQLite + Ollama) permaneça sem reescrita enquanto o frontend cidadão é desenvolvido independentemente.

### LGPD não é optional para a Fase 1

Os dois documentos mencionam explicitamente LGPD e PL 2338. Os professores são do Departamento de Direito. A demonstração do curso deve mostrar consciência dos requisitos — pelo menos: (1) log de versão do modelo no pipeline, (2) checklist de anonimização documentado, (3) remoção de PII antes do armazenamento.

### O "Fala Gávea" completo é o Twitter cívico descrito nos documentos do grupo

O Documento 2 elaborado pelo grupo articula exatamente essa visão, que o Andrey também sintetizou no chat da equipe. O PoC atual é o "motor de back-office" (análise e curadoria). O Subsistema A é o "frontend cívico" (participação e engajamento). Juntos, formam uma plataforma onde dados fluem do cidadão → IA → humano → decisor → impacto mensurável. O PoC demonstra que o motor funciona. A Fase 1 completa o motor. As Fases 2 e 3 conectam os dois lados.

---

## Recomendações

1. **[ALTA]** Implementar a interface de revisão humana (cluster title editing + realocação de claims) — fecha o maior gap do UC-02 Doc 1. Usar `st.data_editor` ou componente drag-drop no Streamlit.

2. **[ALTA]** Adicionar registro de versão do modelo e timestamp de execução ao resultado do pipeline — requisito de auditabilidade, impacto mínimo (1 coluna SQLite).

3. **[ALTA]** Documentar os requisitos LGPD no security checklist e adicionar um passo de anonimização documentado antes da entrega do curso — os professores são do Departamento de Direito.

4. **[ALTA]** Definir formalmente a arquitetura de dois subsistemas no product-design-as-intended §1 e §2, e adicionar entrada D-006 sobre o boundary de escopo do curso.

5. **[MÉDIA]** Implementar export CSV/JSON e filtro por territory em paralelo — independentes, baixo risco, alto impacto na demo.

6. **[MÉDIA]** Adicionar estado "publicado" na sessão (badge + coluna `published_at`) para completar o fluxo do UC-02 passo 7.

7. **[MÉDIA]** Integrar Whisper local para transcrição de áudio — UC-02 fluxo alternativo, sem dependência de cloud.

8. **[BAIXA]** Planejar o Subsistema A (camada cidadã) como brief separado para pós-curso — FastAPI backend + React/Flutter frontend, PostgreSQL, auth.
