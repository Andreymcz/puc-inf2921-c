# Communication 000077 (v2) | ACD/EVL | 2026-06-26 22:32 UTC | Timeline do Projeto

> **Timeline mestre do projeto fala-gávea** — insumo único para construir o *relatório* e a *apresentação* do capstone INF2921/CIS2114 (AI Systems Design, PUC-Rio, 2026.1). Equipe: Andrey, Mauro, Julia, Herbert, Natali, Sheila.
>
> **Documento vivo.** Cada artefato citado é um **link relativo** que abre o arquivo original do repositório (`.md`, `.pdf`, planos, reflexões, roadmaps, código). Ao abrir a versão **`.html`** localmente, os links levam direto às fontes. Veja o índice completo em [§10 Artefatos originais (abrir)](#10-artefatos-originais-abrir).
>
> **v2 (2026-06-26):** linha do tempo macro agora tem link para cada fase detalhada + coluna de frase-chave do artefato-chave; Fase 4 reescrita com a reunião da Fabiene e os Projetos 6 e 8; todos os artefatos viraram links para os originais. Estende a [comunicação 000075](../2026-06-19/communication-000075-academics.md).

---

## Como usar este documento

| Você quer… | Vá para |
|---|---|
| O esqueleto cronológico (1 slide / 1 tabela) | [§1 Linha do tempo macro](#1-linha-do-tempo-macro) |
| Narrar cada fase no relatório | [§2 Fases detalhadas](#2-fases-detalhadas) |
| Mostrar como casos de uso viraram protótipos | [§3 Casos de uso → protótipos](#3-mapa-casos-de-uso--prototipos) |
| Justificar decisões de design | [§4 Genealogia das decisões](#4-genealogia-das-decisoes) |
| Slide de tecnologia | [§5 Stack consolidada](#5-stack-tecnologica-consolidada) |
| O argumento central de IA | [§6 Uso de IA: dois eixos](#6-uso-de-ia-dois-eixos) |
| Provar que o escopo é fundamentado | [§7 Evidências empíricas](#7-evidencias-empiricas-que-ancoram-o-escopo) |
| Montar os slides direto | [§8 Roteiro de apresentação](#8-roteiro-de-apresentacao-sugerido) |
| Falar do método (corpus SEJA) | [§9 O corpus de desenvolvimento](#9-o-corpus-de-desenvolvimento-como-objeto-de-estudo) |
| Abrir os arquivos originais | [§10 Artefatos originais](#10-artefatos-originais-abrir) |

**Tese de uma frase (use na abertura):** *fala-gávea é o resultado de um "zoom in" deliberado e documentado — de um Atlas Digital da Amazônia em escala continental para um canal comunitário de segurança urbana no bairro da Gávea — preservando dois invariantes desde a origem: a camada geoespacial e a soberania de dados (toda inferência de IA roda localmente).*

---

## 1. Linha do tempo macro

O movimento central é um **zoom in**: do atlas de escala continental para um bairro, uma vertical temática (segurança) e dois personas concretos (cidadão e agente público). O produto amadureceu em duas ondas: a **gênese** (PoCs no repo-pai) e a **construção do produto** (submódulo `fala-gavea`).

> A coluna **Detalhe** leva à narrativa da fase. A coluna **Frase-chave (fonte)** traz a citação que melhor resume a fase, com link para o artefato original.

| Fase | Período | Enquadramento | Marco / protótipo | Frase-chave (fonte — clique para abrir) |
|------|---------|---------------|-------------------|------------------------------------------|
| [**0** →](#fase-0) | abr/2026 | Atlas da Amazônia (global) | kb-qa: RAG local (ChromaDB + MCP) | *"atlas digital e iterativo assistido por IA … mantido e curado por uma comunidade"* — [Reuniao-23-04-2026.md](../../../knowledge/Reuniao-23-04-2026.md) |
| [**1** →](#fase-1) | mai/2026 | Participação cidadã | PoC Talk-to-the-City local (Docker + Ollama) | *"a gente clusteriza, analisa com IA, descarta o que é lixo … e mostra um dashboard"* — [Reunioes-stakeholders-1-2.pdf](../../../knowledge/Reunioes-stakeholders-1-2.pdf), [casos-de-uso.md](../../../knowledge/casos-de-uso.md) |
| [**2** →](#fase-2) | jun/2026 | GaveaLab PoC | Pipeline textual em Streamlit (temas→claims→cruxes→UMAP) | *"tríade sistêmica: relatos → perguntas de decisores → IA com validação humana"* — [Casos_de_uso_10-06-2026_1.md](../../../knowledge/Casos_de_uso_10-06-2026_1.md) |
| [**3** →](#fase-3) | jun/2026 | fala-gávea (1ª encarnação) | Streamlit: posts, likes, label feedback, seed, clusters | *"o fala-gávea tem input cidadão real mas não analisa o que coleta"* — [reflection-000037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md) |
| [**4** →](#fase-4) | **15/jun/2026** | **Zoom in para a Gávea** | Segurança urbana; personas cidadão + agente; **validação da Fabiene** | *"o clustering já construído É o motor do caso de uso do delegado"* — [reflection-000052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md) |
| [**5** →](#fase-5) | jun/2026 | Canal comunitário | Busca NL intent-to-filter; lacuna do feedback loop | *"o humano pode curar, mas o feedback do humano não é usado para retroalimentar a IA"* — [reflection-000069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md), [roadmap-000070](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md) |
| [**6** →](#fase-6) | jun/2026 | Clean architecture | Reescrita FastAPI; `fala-gavea` vira submódulo SEJA | *"tiro uma foto, envio a localização do GPS … enviadas para uma base de dados pública"* — [roadmap-000071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md), [check-000073](../../check-logs/check-000073-validate-fala-gavea-scaffold.md) |
| [**7** →](#fase-7) | jun/2026 | **Produto MVP** | Auth/roles + Reports + Forwardings + **React SPA** | *"cidadão registra problema → agente cria encaminhamento para órgão"* — [fg:plan-000082 (SPA React)](../../../fala-gavea/_output/plans/plan-000082-feature-f-wave-1-item-4-frontend-spa-react.md), [README](../../../fala-gavea/README.md) |
| [**8** →](#fase-8) | jun/2026 | Camada de IA | Busca semântica, BERTopic, **chat NL RAG**, sugestão de tópicos | *"IA assiste exploração por busca semântica e chat NL"* — [fg:plan-000100 (RAG chat)](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md) |
| [**9** →](#fase-9) | jun/2026 | Participação + transparência | Votos, comentários, relato anônimo, "meus relatos", cesta de relatos | *"validação coletiva: outros moradores confirmam a demanda com um clique"* — [fg:roadmap-000151](../../../fala-gavea/_output/roadmaps/roadmap-000151-citizen-feedback-votes-comments-anonymization.md) |
| [**10** →](#fase-10) | jun/2026 (atual) | Meta-IA + empacotamento | Helper RAG self-docs (SEJA-aware), **AiBadge** de proveniência, Docker/Railway, showcase seed | *"a plataforma passa a explicar a si mesma"* — [fg:plan-000177 (helper)](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md), [fg:plan-000183 (seed)](../../../fala-gavea/_output/plans/plan-000183-local-showcase-seed-pipeline.md) |

> Prefixo `fg:` = artefato do submódulo [`fala-gavea`](../../../fala-gavea/) (que carrega seu próprio harness SEJA e numeração de planos até 000183, com 17 decisões D-001…D-017).

---

## 2. Fases detalhadas

<a id="fase-0"></a>
### Fase 0 — Origem: Atlas da Amazônia (abr/2026)

**Enquadramento.** O conceito inicial era um *Atlas Digital Georreferenciado da Amazônia assistido por IA*: atlas interativo de dados multimodais georreferenciados (PRODES/DETER/IMAZON/FUNAI via datazoom.amazonia; Nova Cartografia Social), com chat dotado de ferramentas de navegação e soberania de dados.

**Protótipo existente.** O **kb-qa** — um RAG local (ChromaDB + sentence-transformers + servidor MCP) já integrado e testado no Claude Code. Diagnóstico arquitetural honesto: cobria apenas 20–30% do necessário. Definiu-se uma arquitetura em camadas (RAG textual + engine geoespacial DuckDB spatial + ferramenta `render_map`), abstração de LLM (Ollama local OU nuvem) e serviço dual MCP + REST.

**Documentos.** [`Reuniao-23-04-2026.md`](../../../knowledge/Reuniao-23-04-2026.md) registra o **problema** ("acesso controlado e curado a informação multimodal georreferenciada") e o **produto** ("atlas digital e iterativo assistido por IA … mantido e curado por uma comunidade"). A reunião já listava três verticais temáticas — **segurança pública** (vigilância por câmeras, mapeamento de fluxos, revitalização de espaços), **educação** e **acesso à informação** — que prefiguram o produto final. Princípios **CARE/OCAP** (soberania de dados de comunidades) herdados do contexto indígena amazônico → tornam-se o invariante "inferência local".

<a id="fase-1"></a>
### Fase 1 — Casos de uso e participação cidadã (mai/2026)

**Enquadramento.** Foco migra para um *espaço virtual de participação cidadã*. Sintetizaram-se plataformas de referência (Decidim, Pol.is, Talk to the City, Consul, vTaiwan, UDT); convergiu-se para **Talk to the City (T3C)** com deployment local.

**Protótipo.** Uma PoC TRL3 rodou ponta a ponta com Docker e Ollama local, sobre um CSV de teste baseado no diagnóstico real do GaveaLab (2023). ([plan-000001 — TRL3 PoC tttc local Ollama](../../plans/plan-000001-trl3-poc-tttc-local-ollama.md).)

**Casos de uso.** [`casos-de-uso.md`](../../../knowledge/casos-de-uso.md) registra três casos seminais: (1) **cidadão** discute problemas do território; (2) **investidor/gestor** toma decisões embasadas em dados; (3) **GaveaLab** coleta e sintetiza pesquisas. As transcrições de stakeholders ([`Reunioes-stakeholders-1-2.pdf`](../../../knowledge/Reunioes-stakeholders-1-2.pdf)) registram o debate que moldou a arquitetura — Natali Garcia: *"a gente clusteriza, analisa com IA, descarta o que é lixo, faz uma classificação ligada a perfis e mostra um dashboard"*; Andrey Rodrigues: a IA *"não como um curador principal, mas um auxiliador na curadoria"*.

<a id="fase-2"></a>
### Fase 2 — GaveaLab PoC: análise textual (jun/2026)

**Protótipo.** PoC em **Streamlit** (SQLite via `GaveaLabWorkspace` + Ollama) com o pipeline completo de análise de relatos: **upload de CSV → temas automáticos → claims → categorização manual → cruxes** (detecção de divergências via embeddings), seguido de **visualização UMAP** e navegação multipágina. ([plan-000008 scaffold](../../plans/plan-000008-gavealab-poc-scaffold.md) … [plan-000016 UMAP](../../plans/plan-000016-gavealab-poc-umap-visualization.md), [plan-000021 multipage](../../plans/plan-000021-gavealab-poc-all-studies-page-multipage-nav.md).)

**Caso de uso formal.** O documento da disciplina [`Casos_de_uso_10-06-2026_1.md`](../../../knowledge/Casos_de_uso_10-06-2026_1.md) formaliza **CU01: Consulta para tomada de decisão** — gestor público/investidor que quer conhecer os problemas do território para formular políticas baseadas em evidências. Introduz a **tríade sistêmica**: (1) base de conhecimento de relatos cidadãos; (2) perguntas de decisores; (3) ferramentas de IA com validação humana. Cita conformidade com **LGPD** e alinhamento ao **PL 2338** (Marco Regulatório da IA) como requisitos de design.

<a id="fase-3"></a>
### Fase 3 — fala-gávea, 1ª encarnação: relatos + feedback + clusters (jun/2026)

**Protótipo.** A plataforma ganha o nome **fala-gávea**: backend FastAPI com entidade `CitizenPost`, `LikeModel`, use cases `ToggleLike`/`AddLabelFeedback`, app Streamlit com 4 páginas (Postagens, Nova Postagem, Validar Labels, Dashboard), seed de 1000 relatos, rastreabilidade de likes, paginação, nomes legíveis. ([plan-000027 setup](../../plans/plan-000027-fala-gavea-setup-streamlit.md) … [plan-000043 multipage refactor](../../plans/plan-000043-fala-gavea-multipage-streamlit-refactor.md).)

**Caso de uso (lado cidadão).** [`Casos_de_uso_10-06-2026_2.md`](../../../knowledge/Casos_de_uso_10-06-2026_2.md) introduz **"Morador registra e acompanha uma demanda local"**: um morador da Rocinha percebe que há três semanas a iluminação pública está apagada; via app descreve por **texto, voz ou foto**, a IA **categoriza automaticamente e infere a localização**, e outros moradores **confirmam com um clique** (validação coletiva). Este é o ancestral direto do `SecurityReport`.

**Reflexão-âncora.** A [reflection-000037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md) diagnostica a assimetria: *"o gavealab-poc analisa CSVs mas não tem plataforma de input; o fala-gávea tem input cidadão real mas não analisa o que coleta"*. O próximo passo natural: conectar os dois subsistemas.

<a id="fase-4"></a>
### Fase 4 — Zoom in: do Atlas para a Gávea (15/jun/2026) ⭐ *decisão-chave*

**A inflexão.** Em vez de um atlas global: **um bairro** (Gávea), **uma vertical** (segurança urbana), **dois personas** — o **cidadão** que reporta um problema (foto, GPS, texto) e o **agente público / delegado** que explora um dashboard georreferenciado e cura as demandas. O mapa passa a usar Google Maps/Leaflet (baixo custo).

**A reunião com a Fabiene e os Projetos 6 e 8.** Depois de apresentar a **1ª encarnação do fala-gávea** (Fase 3) à pesquisadora **Fabienne Torres Schiavo** — coordenadora do diagnóstico FAPERJ do GaveaLab —, ela **validou a relevância de um caso de uso real** e **encaminhou à equipe dois projetos/desafios do GaveaLab**, referidos como **Projeto 6 e Projeto 8**. O **Projeto 08** é a trilha que a equipe adotou e que dá título à pesquisa de arquitetura [research-000074 — "Camadas georreferenciadas para fala-gavea (Projeto 08)"](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md): *"ampliar o fala-gavea de sistema de registro de demandas individuais para um atlas territorial colaborativo"* — exatamente o retorno à camada geoespacial do atlas original, agora em escala de bairro.

> 📌 **Verificar referência original (ação para a equipe).** A indicação dos "Projetos 6 e 8" foi compartilhada como texto no WhatsApp da equipe. O *dump* disponível no repositório ([`dump-grupo-wpp-24-05-2026.txt`](../../../knowledge/dump-grupo-wpp-24-05-2026.txt)) é de **24/05/2026** e **antecede** essa reunião (15/jun), portanto não contém o texto. **Cole aqui a descrição oficial dos Projetos 6 e 8** (edital/lista de desafios do GaveaLab ou a mensagem da Fabiene) para fechar a citação. Material de seed já derivado desses desafios está em [`CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt`](../../../knowledge/CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt) (casos de uso de agentes públicos: iluminação, investimento social, mobilidade, educação, mulher e direitos humanos) e [`RELATOS_HERBERT.txt`](../../../knowledge/RELATOS_HERBERT.txt) (relatos de cidadãos sobre iluminação e segurança).

**Reflexão-âncora.** A [reflection-000052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md) documenta a conversa de equipe (15/06, 19:43–20:02). Três insights metodológicos: (1) *o clustering já construído É o motor do caso de uso do delegado* — a integração com o mapa é uma nova **camada de visualização**, não um novo projeto; (2) o custo computacional já estava resolvido (Ollama local + mapa com tier gratuito); (3) **Fabiene é stakeholder real, não só avaliadora** — há demanda institucional, e o documento dela pode ser anexado à entrega.

**Evidência empírica.** O **diagnóstico FAPERJ 2023** do GaveaLab ([`Strategic Design 4 Smart City Lab — Gavea Lab diagnostico_onepage.pdf`](../../../knowledge/Strategic%20Design%204%20Smart%20City%20Lab%20_Gavea%20Lab%20diagnostico_onepage.pdf)) ancora a escolha de **SEGURANÇA**: pesquisa de campo jun–nov/2023 com **380 entrevistados** (Gávea-"asfalto" 137, Rocinha 132, Parque da Cidade 16, trabalhadores 95), coordenada pela Profa. Fabienne Torres Schiavo. O **Mapa de Forças Locais Atuantes (MFLA)** aponta SEGURANÇA (24%) e EDUCAÇÃO (22%) como temas alavancadores no "asfalto"; segurança aparece como maior dor (20% asfalto, 9% favelas). E o dado decisivo: **a percepção de segurança diverge radicalmente** — para o "asfalto" significa *mais polícia*; para a Rocinha/Parque da Cidade, *garantia de direitos e ausência de violência policial*. Esse contraste justifica uma plataforma que capture a **multiplicidade de vozes sobre o mesmo território**.

<a id="fase-5"></a>
### Fase 5 — Busca inteligente + canal comunitário (jun/2026)

**Protótipo.** Chat em linguagem natural **"intent-to-filter"** (o usuário descreve a busca em NL; a IA a traduz para filtros da API). ([plan-000068](../../plans/plan-000068-chat-nl-intent-to-filter.md).)

**Reflexão-âncora.** A [reflection-000069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md) detecta a **lacuna estrutural do feedback loop**: as correções do delegado (par `ai_suggested_category` × `category` confirmada) existiam no banco mas **não eram capturadas como sinal de treino**.

**Roadmap.** O [roadmap-000070 — "Canal Digital Comunitário para Segurança Urbana"](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md) (um *"Waze comunitário"*) fecha o loop com: `CategoryCurationEvent` de **auditoria append-only**; **few-shot injection** no prompt (em vez de fine-tuning); clustering reaproveitando embeddings já no ChromaDB; urgência e encaminhamento institucional. Princípio: IA como auxiliar da curadoria humana — **human-in-the-loop barato e auditável**.

<a id="fase-6"></a>
### Fase 6 — Reescrita em clean architecture (jun/2026)

**Protótipo / transição.** O fala-gávea é **reescrito do zero** como scaffold de clean architecture (FastAPI + SQLAlchemy + SQLite + Pydantic v2 + pytest) e passa a ser um **git submodule com seu próprio harness SEJA**. ([roadmap-000071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md), [plan-000072](../../plans/plan-000072-fala-gavea-scaffold-e-seja-setup.md), [check-000073 validado 6/6 PASS](../../check-logs/check-000073-validate-fala-gavea-scaffold.md).)

**Casos de uso consolidados** ([roadmap-000071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md), verbatim):
- **CU1 (cidadão):** *"Um poste da minha rua está apagado. Abro um site, entro com a minha conta, tiro uma foto, envio a localização do GPS e escrevo uma mensagem. Quando aperto um botão, tudo é enviado para uma base de dados pública."*
- **CU2 (agente público):** *"Filtro demandas, seleciono demandas semelhantes/repetidas e crio um encaminhamento para um órgão. O encaminhamento tem um status e solução proposta."*

Entidades de domínio fixadas aqui: `User` (citizen/agent/admin), `ReportType` (dinâmico, CRUD do admin), `Report`, `Forwarding` (agregação many-to-many de relatos). A [research-000074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md) retorna explicitamente à **camada geoespacial** do atlas original — agora em escala de bairro (Projeto 08).

---

### As fases 7–10 são a construção do produto a ser entregue ([`fala-gavea`](../../../fala-gavea/), submódulo)

> A partir daqui, o desenvolvimento ocorre **dentro do submódulo `fala-gavea`**, que tem seu próprio ciclo SEJA (`/research → /plan → /implement → /check → /document`), numeração de planos até **000183** e **17 decisões de design** (D-001…D-017). O produto evoluiu de scaffold para uma **SPA React + API FastAPI** completa, com IA local, participação cidadã e empacotamento para deploy. Visão geral em [`fala-gavea/README.md`](../../../fala-gavea/README.md) e [`fala-gavea/CLAUDE.md`](../../../fala-gavea/CLAUDE.md).

<a id="fase-7"></a>
### Fase 7 — Produto MVP: domínio, auth e SPA (jun/2026)

**Protótipos entregues.**
- **Domínio + Auth + Reports** ([fg:plan-000073](../../../fala-gavea/_output/plans/plan-000073-feature-b-wave-0-item-1-domain-auth-reports.md)): entidades, JWT Bearer (PyJWT + bcrypt), roles citizen/agent/admin, `POST /reports`, `GET /reports/geojson` com filtros (tipo, urgência, status, since/until, bbox).
- **ReportType CRUD** ([fg:plan-000075](../../../fala-gavea/_output/plans/plan-000075-feature-b-wave-0-item-2-report-type-crud.md)): tipos de problema **dinâmicos** (admin), soft-delete, seed via API.
- **Forwarding CRUD** ([fg:plan-000079](../../../fala-gavea/_output/plans/plan-000079-feature-b-wave-1-item-3-forwarding-crud.md)): encaminhamento como **agregação de N relatos** selecionados, com status (aguardando → em andamento → finalizado) e solução proposta.
- **Frontend SPA React** ([fg:plan-000082](../../../fala-gavea/_output/plans/plan-000082-feature-f-wave-1-item-4-frontend-spa-react.md)): migração de HTML estático para **React 18 + Vite + TypeScript + Tailwind + react-leaflet** — mapa, formulário de relato com geolocalização, painel do agente, login.

Realiza **CU1 (cidadão)** e **CU2 (agente)** end-to-end. ([fg:reflection-000086 — estado do CRUD vs. roadmap](../../../fala-gavea/_output/reflections/reflection-000086-estado-atual-crud-vs-roadmap.md).)

<a id="fase-8"></a>
### Fase 8 — Camada de IA: semântica, tópicos e chat (jun/2026)

**Protótipos entregues.**
- **Infra semântica** ([fg:plan-000089](../../../fala-gavea/_output/plans/plan-000089-semantic-infra-deps-embeddings-portas-chroma.md), [fg:plan-000090](../../../fala-gavea/_output/plans/plan-000090-ingestion-pipeline-indexacao-relatos-backfill.md)): dependências de embeddings, portas Chroma, pipeline de **ingestão/indexação** de relatos com backfill.
- **Busca semântica + relatos similares** ([fg:plan-000094](../../../fala-gavea/_output/plans/plan-000094-semantic-search-similar-reports-wave1.md)): `GET /reports/search` e `/reports/{id}/similar` — o agente identifica **duplicatas** antes de encaminhar.
- **BERTopic topic modeling** ([fg:plan-000099](../../../fala-gavea/_output/plans/plan-000099-bertopic-topic-modeling-backend.md)): modelagem de tópicos no backend.
- **Chat NL RAG** ([fg:plan-000100](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md)): assistente de exploração (OllamaClient + RAG sobre relatos) que cita os relatos usados como contexto.
- **Sugestão de tipos de relato por IA** ([fg:plan-000174](../../../fala-gavea/_output/plans/plan-000174-pluggable-report-type-suggestion.md) + [fg:reflection-000171](../../../fala-gavea/_output/reflections/reflection-000171-ia-sugerir-topicos-relatos-sem-topico.md)): IA sugere `report_type` para relatos sem tópico — **estratégia plugável**, mantendo o humano no comando.

Materializa o **feedback loop** desenhado no [roadmap-000070](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md) e a tese de "IA como auxiliadora da curadoria".

<a id="fase-9"></a>
### Fase 9 — Participação cidadã e transparência (jun/2026)

**Roadmaps.** [fg:roadmap-000146 — "cesta de relatos" (transparência ao cidadão)](../../../fala-gavea/_output/roadmaps/roadmap-000146-cesta-de-relatos-citizen-transparency.md) e [fg:roadmap-000151 — votos, comentários, anonimização](../../../fala-gavea/_output/roadmaps/roadmap-000151-citizen-feedback-votes-comments-anonymization.md).

**Protótipos entregues.**
- **Votos + comentários + relato anônimo** ([fg:plan-000152](../../../fala-gavea/_output/plans/plan-000152-db-schema-votes-comments-anon-tokens.md)–[fg:plan-000158](../../../fala-gavea/_output/plans/plan-000158-anonymous-ux.md)): schema de votos/comentários/anon-tokens, backends e UX — **validação coletiva** (o "confirmar com um clique" do CU de 10/jun) finalmente implementada.
- **"Meus relatos" + ordenação inline** ([fg:plan-000164](../../../fala-gavea/_output/plans/plan-000164-meus-relatos-nav-inline-votes-sort.md)) e **"meus encaminhamentos" para o cidadão** ([fg:plan-000169](../../../fala-gavea/_output/plans/plan-000169-get-forwardings-mine-cidadao.md)): o cidadão **acompanha** a demanda (fecha o "registra *e acompanha*" do CU01).
- **Filtros salvos + painel de exploração** ([fg:plan-000137](../../../fala-gavea/_output/plans/plan-000137-phase-a-extended-panel-draft-filters-table.md), [fg:plan-000139](../../../fala-gavea/_output/plans/plan-000139-phase-b-saved-filters-backend-ux.md)), unificação da query de relatos ([fg:plan-000132](../../../fala-gavea/_output/plans/plan-000132-unified-reports-query-api-phase-b.md)), refino de busca ([fg:plan-000131](../../../fala-gavea/_output/plans/plan-000131-refine-data-exploration-search-filters.md)), workspace grid com cross-filter ([fg:plan-000104](../../../fala-gavea/_output/plans/plan-000104-frontend-workspace-grid-cross-filter.md)).

Fecha o ciclo de **corresponsabilidade** (cidadão ↔ instituições) previsto no roadmap-000070. ([fg:reflection-000144](../../../fala-gavea/_output/reflections/reflection-000144-transparency-journeys-cesta-de-relatos.md), [fg:reflection-000149](../../../fala-gavea/_output/reflections/reflection-000149-citizen-journeys-blueprint-gap-and-feedback.md).)

<a id="fase-10"></a>
### Fase 10 — Meta-IA e empacotamento para entrega (jun/2026, estado atual)

**Protótipos entregues.**
- **Assistente de ajuda da plataforma (self-docs RAG)** ([fg:plan-000177](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md), [fg:plan-000181](../../../fala-gavea/_output/plans/plan-000181-embed-seja-methodology-platform-helper.md)): `POST /nl/help` responde perguntas **sobre a própria plataforma** a partir da documentação do projeto indexada no ChromaDB; para o admin, recebe um **enquadramento "meta" ciente do SEJA** (taxonomia/SDLC) como lente de interpretação (decisão D-017). A plataforma passa a **explicar a si mesma**.
- **AiBadge — marcador de proveniência de IA** ([fg:plan-000178](../../../fala-gavea/_output/plans/plan-000178-aibadge-provenance-marker.md), D-015): todo conteúdo gerado por IA recebe um selo reutilizável — **transparência de proveniência** como princípio de UI.
- **Síntese de comentários de encaminhamento** ([fg:plan-000179](../../../fala-gavea/_output/plans/plan-000179-forwarding-comment-synthesis.md)).
- **Empacotamento:** Dockerfile + **deploy Railway** ([fg:plan-000096](../../../fala-gavea/_output/plans/plan-000096-dockerfile-railway-deploy.md), [fg:plan-000115](../../../fala-gavea/_output/plans/plan-000115-railway-deploy-fixes.md)); **pipeline de seed showcase** ([fg:plan-000183](../../../fala-gavea/_output/plans/plan-000183-local-showcase-seed-pipeline.md)) que popula todas as features (usuários, relatos, encaminhamentos, votos, comentários, filtros salvos, ciclo de vida) a partir de CSVs curados (200 linhas showcase / 5k full).
- **Documentação para 4 públicos** ([fg:communication-000125 evaluators](../../../fala-gavea/docs/communication-000125-evaluators.md), [000126 clients](../../../fala-gavea/docs/communication-000126-clients.md), [000127 end-users](../../../fala-gavea/docs/communication-000127-end-users.md), [000128 academics](../../../fala-gavea/docs/communication-000128-academics.md)), acessível em `/docs/` no app em execução.

**Estado de entrega.** Produto executável localmente (API + SPA com hot-reload), via Docker, e publicável no Railway. Stack: **React 18 + FastAPI clean architecture + SQLite + ChromaDB + Ollama local**, com auth por roles, busca semântica, chat NL, votos/comentários, e um assistente que documenta o próprio sistema.

---

## 3. Mapa: casos de uso → protótipos

Como cada caso de uso atravessou o tempo até virar código entregue.

| Caso de uso (origem) | Fase de concepção | Protótipo intermediário | Implementação final (`fala-gavea`) |
|---|---|---|---|
| **Cidadão registra e acompanha demanda** ([`Casos_de_uso_2`](../../../knowledge/Casos_de_uso_10-06-2026_2.md), 10/jun) | [3](#fase-3)–[4](#fase-4) | CitizenPost + likes (Streamlit, F3) | `POST /reports` + "Meus relatos" + votos/comentários ([F7](#fase-7), [F9](#fase-9)) |
| **Gestor/investidor consulta para decisão** ([`Casos_de_uso_1`](../../../knowledge/Casos_de_uso_10-06-2026_1.md), CU01) | [1](#fase-1)–[2](#fase-2) | Pipeline temas→claims→cruxes (GaveaLab PoC, F2) | Painel do agente + filtros + busca semântica + chat NL ([F7](#fase-7)–[F8](#fase-8)) |
| **Validação coletiva** ("confirmar com um clique") | [3](#fase-3) | likes/label feedback | Votos + comentários ([fg:plan-000152–157](../../../fala-gavea/_output/plans/plan-000156-votes-ux.md), [F9](#fase-9)) |
| **Encaminhamento institucional** (CU2, [roadmap-000071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md)) | [5](#fase-5)–[6](#fase-6) | — | `Forwarding` many-to-many + status + síntese ([F7](#fase-7), [F10](#fase-10)) |
| **IA categoriza/sugere com curadoria humana** | [1](#fase-1), [5](#fase-5) | `auto_categorize` + `PATCH /category` | Sugestão plugável de tópicos + AiBadge + feedback loop ([F8](#fase-8), [F10](#fase-10)) |
| **Busca em linguagem natural** | [5](#fase-5) | intent-to-filter ([plan-000068](../../plans/plan-000068-chat-nl-intent-to-filter.md)) | NL filter parser + chat RAG ([fg:plan-000100](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md)) |
| **Camada geoespacial** (Atlas, F0; **Projeto 08**) | [0](#fase-0) | `render_map` proposto | Mapa Leaflet + GeoJSON + bbox (F7); atlas territorial ([research-000074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md)) |
| **Plataforma se explica** (curadoria por perfil, reuniões) | [1](#fase-1) | — | Helper RAG self-docs SEJA-aware ([fg:plan-000177](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md), [F10](#fase-10)) |

---

## 4. Genealogia das decisões

Decisões que sobreviveram e moldaram o produto (D-NNN são as decisões formais do submódulo [`fala-gavea`](../../../fala-gavea/product-design/project/product-design-as-intended.md)):

| Decisão | Tema | Por quê importa para a narrativa |
|---|---|---|
| Inferência **local** (CARE/OCAP → Ollama) | Soberania de dados | Invariante desde o Atlas; é o argumento ético central |
| **Zoom in** Atlas→Gávea ([reflection-000052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md)) | Escopo | Redução de escopo guiada por viabilidade e validação institucional |
| Few-shot injection **em vez de** fine-tuning ([roadmap-000070](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md)) | Aprendizado | Human-in-the-loop barato e auditável; cabe no semestre |
| `CategoryCurationEvent` **append-only** | Auditoria | Captura o sinal de curadoria que faltava ([reflection-000069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md)) |
| Clean architecture + submódulo SEJA ([roadmap-000071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md)) | Engenharia | Permite o produto crescer com rastro auditável próprio |
| `ReportType` **dinâmico** (D-B) | Extensibilidade | Admin adiciona tipos sem redeploy |
| **AiBadge** de proveniência (D-015) | Transparência | Todo output de IA é marcado na UI |
| Helper **SEJA-aware** para admin (D-017) | Meta-comunicação | O sistema explica a si mesmo e ao próprio método de construção |

> O submódulo registra **17 decisões** (D-001…D-017); as acima são as de maior peso narrativo.

---

## 5. Stack tecnológica consolidada

Evolução da pilha ao longo das fases (o que mostrar no slide de tecnologia):

| Camada | Gênese (F0–F5) | Produto entregue (F6–F10) |
|---|---|---|
| Linguagem / gestão | Python 3.13 + uv | Python 3.13 + uv |
| Web / API | Streamlit (PoCs) | **FastAPI** (clean architecture: domain/application/infrastructure/presentation) |
| Frontend | Streamlit pages | **React 18 + Vite + TypeScript + Tailwind + react-leaflet** |
| Persistência | SQLite (`GaveaLabWorkspace`) | SQLite via **SQLAlchemy** |
| Auth | nenhuma (local) | **JWT Bearer (PyJWT + bcrypt)**, roles citizen/agent/admin |
| Vetorial / embeddings | ChromaDB + sentence-transformers | ChromaDB + sentence-transformers (multilingual-e5 / nomic) |
| LLM local | Ollama (qwen) | **Ollama** OpenAI-compatível (`qwen3:8b`) + provider plugável |
| Visualização | UMAP + HDBSCAN + Plotly | Leaflet + GeoJSON; BERTopic |
| Empacotamento | — | **Docker + Railway**; seed showcase (CSV 200/5k) |
| Qualidade | pytest, ruff, pyright | pytest + **Vitest/React Testing Library**, ruff, pyright |

**Princípio transversal:** toda inferência roda **localmente** — soberania de dados.

---

## 6. Uso de IA: dois eixos

A separação que dá força acadêmica ao trabalho.

**1. IA no produto.** Inferência local (Ollama); categorização/sugestão de relatos; clustering semântico (embeddings + UMAP/BERTopic); busca semântica (ChromaDB); relatos similares; chat NL traduzido para filtros de API; chat RAG de exploração; e um **feedback loop few-shot com curadoria humana no comando** (o agente confirma/corrige; a correção alimenta o prompt por injeção few-shot, não fine-tuning) → padrão **human-in-the-loop** auditável. Camada meta: o **helper RAG self-docs** faz a plataforma explicar a si mesma, e o **AiBadge** marca toda saída de IA.

**2. IA no processo de desenvolvimento.** O projeto inteiro foi construído sob o harness **SEJA** sobre Claude Code, no ciclo `/research → /plan → /implement → /check → /document | /communicate → /reflect`. Há um **rastro auditável** de centenas de artefatos numerados (advisory logs, planos, roadmaps, reflexões, QA logs, comunicações, telemetria) e o histórico de commits — um corpus que permite reconstruir não só *o que* foi construído, mas *como* e *por quê* cada inflexão de escopo ocorreu.

---

## 7. Evidências empíricas que ancoram o escopo

A decisão de "zoom in" não foi arbitrária — apoiou-se em corpos de evidência concretos.

**Diagnóstico GaveaLab 2023 (FAPERJ Nº 20/2022).** [Pesquisa de campo](../../../knowledge/Strategic%20Design%204%20Smart%20City%20Lab%20_Gavea%20Lab%20diagnostico_onepage.pdf) do Laboratório de Gestão em Design (LGD/PUC-Rio), jun–nov/2023, **380 entrevistados** (Gávea-"asfalto", Rocinha, Parque da Cidade), coordenação Prof. Carlo Franzato e Prof. Cláudio Freitas de Magalhães, com Fabienne Torres Schiavo (Doutora em Design, CAPES). Achados usados no projeto: SEGURANÇA como tema **alavancador e dor** dos dois grupos; **divergência de percepção** sobre o que é "segurança" (policiamento vs. direitos); GOVERNANÇA como maior insatisfação. Fabienne é a stakeholder que **atestou a relevância** do caso de uso real e **encaminhou os Projetos 6 e 8** (ver [Fase 4](#fase-4)).

**Casos de uso co-construídos (jun/2026).** Documentos formais da disciplina registram **CU01 (cidadão registra e acompanha)** ([Casos_de_uso_2](../../../knowledge/Casos_de_uso_10-06-2026_2.md)) e **CU02 (gestor consulta para decisão)** ([Casos_de_uso_1](../../../knowledge/Casos_de_uso_10-06-2026_1.md)), com conformidade **LGPD** e alinhamento ao **PL 2338**. Material de seed derivado: cenários de agentes públicos ([CENARIOS_…HERBERT.txt](../../../knowledge/CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt)) e relatos de cidadãos ([RELATOS_HERBERT.txt](../../../knowledge/RELATOS_HERBERT.txt)).

**Reuniões de stakeholders como fonte de design.** As [transcrições](../../../knowledge/Reunioes-stakeholders-1-2.pdf) mostram a síntese em tempo real: Natali descrevendo o pipeline ("clusteriza, analisa com IA, descarta lixo, classifica por perfis, mostra dashboard") e a ideia de um **painel de curadoria com personas de cada ator-chave**; Andrey definindo a IA como **auxiliadora, não curadora principal**. Essas falas são a origem direta do padrão human-in-the-loop e do helper por perfil de role.

---

## 8. Roteiro de apresentação (sugerido)

Sequência de slides pronta para montar a partir das seções acima.

1. **Capa** — *fala-gávea: um canal comunitário de segurança urbana para a Gávea* (equipe, disciplina). [tese de §0]
2. **O problema** — Gávea concentra realidades radicalmente distintas (asfalto, Rocinha, Parque da Cidade) sem canal unificado de escuta. [[§7](#7-evidencias-empiricas-que-ancoram-o-escopo), diagnóstico FAPERJ]
3. **A genealogia (zoom in)** — animar a [Tabela §1](#1-linha-do-tempo-macro) do Atlas global → bairro/segurança/2 personas. [[§2](#2-fases-detalhadas) F0–F4]
4. **Evidência que ancora o escopo** — MFLA, 380 entrevistados, divergência sobre "segurança"; reunião com a Fabiene → Projetos 6 e 8. [[§7](#7-evidencias-empiricas-que-ancoram-o-escopo), [Fase 4](#fase-4)]
5. **Os dois casos de uso** — cidadão registra/acompanha; agente filtra/encaminha. [[Fase 6](#fase-6)]
6. **Demo do produto** — registro com foto/GPS → mapa → busca semântica → chat NL → encaminhamento → votos/comentários. [[F7](#fase-7)–[F9](#fase-9)]
7. **IA no produto** — categorização + clustering + RAG + feedback loop human-in-the-loop. [[§6.1](#6-uso-de-ia-dois-eixos)]
8. **Meta: o sistema se explica** — helper RAG self-docs + AiBadge de proveniência. [[Fase 10](#fase-10), [§4](#4-genealogia-das-decisoes)]
9. **IA no processo** — desenvolvido com SEJA/Claude Code; corpus auditável de artefatos. [[§6.2](#6-uso-de-ia-dois-eixos), [§9](#9-o-corpus-de-desenvolvimento-como-objeto-de-estudo)]
10. **Stack & entrega** — clean architecture, Docker/Railway, testes. [[§5](#5-stack-tecnologica-consolidada)]
11. **Fechamento** — os dois invariantes (geoespacial + soberania de dados) ligam o produto final à origem amazônica; redução de escopo deliberada e documentada como mérito. [[§2 fechamento](#9-o-corpus-de-desenvolvimento-como-objeto-de-estudo)]

---

## 9. O corpus de desenvolvimento como objeto de estudo

Para o eixo "AI Systems Design", o método é parte do resultado.

- **Repo-pai (`inf2921-grupo-c`):** planos 000001–000077, reflexões [000037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md)/[000052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md)/[000069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md), roadmaps 000007–000071, comunicações (incl. a [000075](../2026-06-19/communication-000075-academics.md)).
- **Submódulo ([`fala-gavea`](../../../fala-gavea/)):** seu próprio harness SEJA — planos até **000183**, **4 roadmaps**, **11 reflexões**, **17 decisões D-NNN**, e **4 comunicações** ([125](../../../fala-gavea/docs/communication-000125-evaluators.md)–[128](../../../fala-gavea/docs/communication-000128-academics.md)) tornando o produto auto-documentado.
- Cada artefato é numerado, datado e rastreável a um commit — permite reconstruir a cadeia *pesquisa → decisão → plano → implementação → verificação → comunicação*.

**Fechamento.** O mérito do projeto não está em ter chegado ao escopo inicial, e sim em ter feito o caminho inverso de forma deliberada e documentada. A trajetória *Atlas global → Gávea local* é um estudo de caso de **redução de escopo guiada por viabilidade, validação institucional e reaproveitamento de capacidades** — o reconhecimento de que o pipeline de clustering do agente já existia e só precisava de uma nova camada (o mapa). Os dois invariantes que sobreviveram a todas as fases — **camada geoespacial** e **soberania de dados local** — são exatamente os que conectam o produto final à sua origem amazônica.

---

## 10. Artefatos originais (abrir)

Índice de links diretos. Abra a versão **`.html`** deste documento para clicar e abrir cada fonte localmente.

### Base de conhecimento (`knowledge/`)
- [Reuniao-23-04-2026.md](../../../knowledge/Reuniao-23-04-2026.md) — problema/produto do Atlas; verticais temáticas
- [casos-de-uso.md](../../../knowledge/casos-de-uso.md) — 3 casos de uso seminais
- [Casos_de_uso_10-06-2026_1.md](../../../knowledge/Casos_de_uso_10-06-2026_1.md) — CU01 gestor/decisor; tríade sistêmica
- [Casos_de_uso_10-06-2026_2.md](../../../knowledge/Casos_de_uso_10-06-2026_2.md) — CU01 cidadão registra/acompanha
- [Reunioes-stakeholders-1-2.pdf](../../../knowledge/Reunioes-stakeholders-1-2.pdf) — transcrições de design
- [Strategic Design 4 Smart City Lab — Gavea Lab diagnostico_onepage.pdf](../../../knowledge/Strategic%20Design%204%20Smart%20City%20Lab%20_Gavea%20Lab%20diagnostico_onepage.pdf) — diagnóstico FAPERJ 2023
- [CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt](../../../knowledge/CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt) — casos de uso de agentes públicos (seed)
- [RELATOS_HERBERT.txt](../../../knowledge/RELATOS_HERBERT.txt) — relatos de cidadãos (seed)
- [dump-grupo-wpp-24-05-2026.txt](../../../knowledge/dump-grupo-wpp-24-05-2026.txt) — WhatsApp da equipe (até 24/05)

### Artefatos SEJA (repo-pai `_output/`)
- Planos: [000001](../../plans/plan-000001-trl3-poc-tttc-local-ollama.md), [000008](../../plans/plan-000008-gavealab-poc-scaffold.md), [000016](../../plans/plan-000016-gavealab-poc-umap-visualization.md), [000021](../../plans/plan-000021-gavealab-poc-all-studies-page-multipage-nav.md), [000027](../../plans/plan-000027-fala-gavea-setup-streamlit.md), [000043](../../plans/plan-000043-fala-gavea-multipage-streamlit-refactor.md), [000068](../../plans/plan-000068-chat-nl-intent-to-filter.md), [000072](../../plans/plan-000072-fala-gavea-scaffold-e-seja-setup.md)
- Reflexões: [000037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md), [000052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md), [000069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md)
- Roadmaps: [000070](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md), [000071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md)
- Verificação/pesquisa: [check-000073](../../check-logs/check-000073-validate-fala-gavea-scaffold.md), [research-000074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md)
- Comunicação: [000075 (academics)](../2026-06-19/communication-000075-academics.md)

### Produto a entregar (`fala-gavea/`)
- [README.md](../../../fala-gavea/README.md) · [CLAUDE.md](../../../fala-gavea/CLAUDE.md)
- Planos-chave: [000073 domínio+auth](../../../fala-gavea/_output/plans/plan-000073-feature-b-wave-0-item-1-domain-auth-reports.md) · [000082 SPA React](../../../fala-gavea/_output/plans/plan-000082-feature-f-wave-1-item-4-frontend-spa-react.md) · [000100 chat RAG](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md) · [000177 helper self-docs](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md) · [000183 seed showcase](../../../fala-gavea/_output/plans/plan-000183-local-showcase-seed-pipeline.md)
- Docs por público: [125 evaluators](../../../fala-gavea/docs/communication-000125-evaluators.md) · [126 clients](../../../fala-gavea/docs/communication-000126-clients.md) · [127 end-users](../../../fala-gavea/docs/communication-000127-end-users.md) · [128 academics](../../../fala-gavea/docs/communication-000128-academics.md)

> ⚠️ **Links do submódulo `fala-gavea/`** abrem quando o submódulo está populado localmente (`git submodule update --init`). PDFs abrem no navegador a partir da versão `.html` deste documento.
