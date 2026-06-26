# Communication 000077 | ACD/EVL | 2026-06-26 22:32 UTC | Timeline do Projeto

> **Timeline mestre do projeto fala-gávea** — insumo único para construir o *relatório* e a *apresentação* do capstone INF2921/CIS2114 (AI Systems Design, PUC-Rio, 2026.1). Equipe: Andrey, Mauro, Julia, Herbert, Natali, Sheila.
>
> Este documento consolida **todos os planos, reflexões e roadmaps** do repositório (repo-pai `inf2921-grupo-c` + submódulo `fala-gavea`, o produto a ser entregue), amarrando cada fase aos **casos de uso** e **protótipos** que a materializaram. As fases de gênese (0–6) atualizam e reusam a [comunicação 000075](../2026-06-19/communication-000075-academics.md); as fases 7–10 documentam a maturação do produto `fala-gavea` em si.

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

**Tese de uma frase (use na abertura):** *fala-gávea é o resultado de um "zoom in" deliberado e documentado — de um Atlas Digital da Amazônia em escala continental para um canal comunitário de segurança urbana no bairro da Gávea — preservando dois invariantes desde a origem: a camada geoespacial e a soberania de dados (toda inferência de IA roda localmente).*

---

## 1. Linha do tempo macro

O movimento central é um **zoom in**: do atlas de escala continental para um bairro, uma vertical temática (segurança) e dois personas concretos (cidadão e agente público). O produto final amadureceu em duas grandes ondas: a **gênese** (PoCs no repo-pai) e a **construção do produto** (submódulo `fala-gavea`).

| Fase | Período | Enquadramento | Marco / Protótipo | Artefatos-chave |
|------|---------|---------------|-------------------|-----------------|
| **0** | abr/2026 | Atlas da Amazônia (global) | kb-qa: RAG local (ChromaDB + MCP) | `Reuniao-23-04-2026.md`, advisory-000002 |
| **1** | mai/2026 | Participação cidadã | PoC Talk-to-the-City local (Docker + Ollama) | `casos-de-uso.md`, plan-000001 (TRL3) |
| **2** | jun/2026 | GaveaLab PoC | Pipeline textual em Streamlit (temas→claims→cruxes→UMAP) | plans 000008–000016 |
| **3** | jun/2026 | fala-gávea (1ª encarnação) | Streamlit: posts, likes, label feedback, seed, clusters | plans 000027–000043; reflection-000037 |
| **4** | **15/jun/2026** | **Zoom in para a Gávea** | Segurança urbana; personas cidadão + delegado; validação institucional | **reflection-000052**; diagnóstico FAPERJ 2023 |
| **5** | jun/2026 | Canal comunitário | Busca NL intent-to-filter; lacuna do feedback loop | reflection-000069; roadmap-000070 |
| **6** | jun/2026 | Clean architecture | Reescrita FastAPI; `fala-gavea` vira submódulo SEJA | roadmap-000071; plan-000072; check-000073 |
| **7** | jun/2026 | **Produto MVP** | Auth/roles + Reports + Forwardings + **React SPA** | fg:plan-000073/075/079/082 |
| **8** | jun/2026 | Camada de IA | Busca semântica, BERTopic, **chat NL RAG**, sugestão de tópicos | fg:plan-000089/094/099/100/174 |
| **9** | jun/2026 | Participação + transparência | Votos, comentários, relato anônimo, "meus relatos", cesta de relatos | fg:roadmap-000146/000151; plan-000152–000169 |
| **10** | jun/2026 (atual) | Meta-IA + empacotamento | Helper RAG self-docs (SEJA-aware), **AiBadge** de proveniência, Docker/Railway, showcase seed | fg:plan-000177/178/181/183 |

> Prefixo `fg:` = artefato do submódulo `fala-gavea` (que carrega seu próprio harness SEJA e numeração de planos até 000183, com 17 decisões D-001…D-017).

---

## 2. Fases detalhadas

### Fase 0 — Origem: Atlas da Amazônia (abr/2026)

**Enquadramento.** O conceito inicial era um *Atlas Digital Georreferenciado da Amazônia assistido por IA*: atlas interativo de dados multimodais georreferenciados (PRODES/DETER/IMAZON/FUNAI via datazoom.amazonia; Nova Cartografia Social), com chat dotado de ferramentas de navegação e soberania de dados.

**Protótipo existente.** O **kb-qa** — um RAG local (ChromaDB + sentence-transformers + servidor MCP) já integrado e testado no Claude Code. Diagnóstico arquitetural honesto: cobria apenas 20–30% do necessário. Definiu-se uma arquitetura em camadas (RAG textual + engine geoespacial DuckDB spatial + ferramenta `render_map`), abstração de LLM (Ollama local OU nuvem) e serviço dual MCP + REST.

**Documentos (kb-qa).** `Reuniao-23-04-2026.md` registra o **problema** ("acesso controlado e curado a informação multimodal georreferenciada") e o **produto** ("atlas digital e iterativo assistido por IA … mantido e curado por uma comunidade"). A reunião já listava três verticais temáticas — **segurança pública** (vigilância por câmeras, mapeamento de fluxos, revitalização de espaços), **educação** e **acesso à informação** — que prefiguram o produto final. Princípios **CARE/OCAP** (soberania de dados de comunidades) herdados do contexto indígena amazônico → tornam-se o invariante "inferência local".

### Fase 1 — Casos de uso e participação cidadã (mai/2026)

**Enquadramento.** Foco migra para um *espaço virtual de participação cidadã*. Sintetizaram-se plataformas de referência (Decidim, Pol.is, Talk to the City, Consul, vTaiwan, UDT); convergiu-se para **Talk to the City (T3C)** com deployment local.

**Protótipo.** Uma PoC TRL3 rodou ponta a ponta com Docker e Ollama local, sobre um CSV de teste baseado no diagnóstico real do GaveaLab (2023). (plan-000001 — TRL3 PoC tttc local Ollama.)

**Casos de uso (`casos-de-uso.md`).** Três casos seminais: (1) **cidadão** discute problemas do território; (2) **investidor/gestor** toma decisões embasadas em dados; (3) **GaveaLab** coleta e sintetiza pesquisas. As transcrições de stakeholders (`Reunioes-stakeholders-1-2.pdf`) registram o debate que moldou a arquitetura — Natali Garcia: *"a gente clusteriza, analisa com IA, descarta o que é lixo, faz uma classificação ligada a perfis e mostra um dashboard"*; Andrey Rodrigues: a IA *"não como um curador principal, mas um auxiliador na curadoria"*.

### Fase 2 — GaveaLab PoC: análise textual (jun/2026)

**Protótipo.** PoC em **Streamlit** (SQLite via `GaveaLabWorkspace` + Ollama) com o pipeline completo de análise de relatos: **upload de CSV → temas automáticos → claims → categorização manual → cruxes** (detecção de divergências via embeddings), seguido de **visualização UMAP** e navegação multipágina. (plans 000008–000016, 000021.)

**Caso de uso formal.** O documento da disciplina (`Casos_de_uso_10-06-2026_1.md`) formaliza **CU01: Consulta para tomada de decisão** — gestor público/investidor que quer conhecer os problemas do território para formular políticas baseadas em evidências. Introduz a **tríade sistêmica**: (1) base de conhecimento de relatos cidadãos; (2) perguntas de decisores; (3) ferramentas de IA com validação humana. Cita conformidade com **LGPD** e alinhamento ao **PL 2338** (Marco Regulatório da IA) como requisitos de design.

### Fase 3 — fala-gávea, 1ª encarnação: relatos + feedback + clusters (jun/2026)

**Protótipo.** A plataforma ganha o nome **fala-gávea**: backend FastAPI com entidade `CitizenPost`, `LikeModel`, use cases `ToggleLike`/`AddLabelFeedback`, app Streamlit com 4 páginas (Postagens, Nova Postagem, Validar Labels, Dashboard), seed de 1000 relatos, rastreabilidade de likes, paginação, nomes legíveis. (plans 000027–000043.)

**Caso de uso (lado cidadão).** `Casos_de_uso_10-06-2026_2.md` introduz **"Morador registra e acompanha uma demanda local"**: um morador da Rocinha percebe que há três semanas a iluminação pública está apagada; via app descreve por **texto, voz ou foto**, a IA **categoriza automaticamente e infere a localização**, e outros moradores **confirmam com um clique** (validação coletiva). Este é o ancestral direto do `SecurityReport`.

**Reflexão-âncora (reflection-000037).** Diagnóstico de assimetria: *"o gavealab-poc analisa CSVs mas não tem plataforma de input; o fala-gávea tem input cidadão real mas não analisa o que coleta"*. O próximo passo natural: conectar os dois subsistemas.

### Fase 4 — Zoom in: do Atlas para a Gávea (15/jun/2026) ⭐ *decisão-chave*

**A inflexão.** Em vez de um atlas global: **um bairro** (Gávea), **uma vertical** (segurança urbana), **dois personas** — o **cidadão** que reporta um problema (foto, GPS, texto) e o **delegado/agente** que explora um dashboard georreferenciado e cura as demandas. O mapa passa a usar Google Maps/Leaflet (baixo custo).

**Reflexão-âncora (reflection-000052).** Documenta a conversa de equipe (15/06, 19:43–20:02). Três insights metodológicos: (1) *o clustering já construído É o motor do caso de uso do delegado* — a integração com o mapa é uma nova **camada de visualização**, não um novo projeto; (2) o custo computacional já estava resolvido (Ollama local + mapa com tier gratuito); (3) **Fabiene é stakeholder real, não só avaliadora** — há demanda institucional.

**Evidência empírica.** O **diagnóstico FAPERJ 2023** do GaveaLab (`Strategic Design 4 Smart City Lab — Gavea Lab diagnostico_onepage.pdf`) ancora a escolha de **SEGURANÇA**: pesquisa de campo jun–nov/2023 com **380 entrevistados** (Gávea-"asfalto" 137, Rocinha 132, Parque da Cidade 16, trabalhadores 95), coordenada pela Profa. Fabienne Torres Schiavo. O **Mapa de Forças Locais Atuantes (MFLA)** aponta SEGURANÇA (24%) e EDUCAÇÃO (22%) como temas alavancadores no "asfalto"; segurança aparece como maior dor (20% asfalto, 9% favelas). E o dado decisivo: **a percepção de segurança diverge radicalmente** — para o "asfalto" significa *mais polícia*; para a Rocinha/Parque da Cidade, *garantia de direitos e ausência de violência policial*. Esse contraste justifica uma plataforma que capture a **multiplicidade de vozes sobre o mesmo território**.

### Fase 5 — Busca inteligente + canal comunitário (jun/2026)

**Protótipo.** Chat em linguagem natural **"intent-to-filter"** (o usuário descreve a busca em NL; a IA a traduz para filtros da API). (plan-000068.)

**Reflexão-âncora (reflection-000069).** Detecta a **lacuna estrutural do feedback loop**: as correções do delegado (par `ai_suggested_category` × `category` confirmada) existiam no banco mas **não eram capturadas como sinal de treino**.

**Roadmap (roadmap-000070).** "Canal Digital Comunitário para Segurança Urbana" — um *"Waze comunitário"* que fecha o loop com: `CategoryCurationEvent` de **auditoria append-only**; **few-shot injection** no prompt (em vez de fine-tuning); clustering reaproveitando embeddings já no ChromaDB; urgência e encaminhamento institucional. Princípio: IA como auxiliar da curadoria humana — **human-in-the-loop barato e auditável**.

### Fase 6 — Reescrita em clean architecture (jun/2026)

**Protótipo / transição.** O fala-gávea é **reescrito do zero** como scaffold de clean architecture (FastAPI + SQLAlchemy + SQLite + Pydantic v2 + pytest) e passa a ser um **git submodule com seu próprio harness SEJA**. (roadmap-000071, plan-000072, check-000073 validado 6/6 PASS.)

**Casos de uso consolidados (roadmap-000071, verbatim).**
- **CU1 (cidadão):** *"Um poste da minha rua está apagado. Abro um site, entro com a minha conta, tiro uma foto, envio a localização do GPS e escrevo uma mensagem. Quando aperto um botão, tudo é enviado para uma base de dados pública."*
- **CU2 (agente público):** *"Filtro demandas, seleciono demandas semelhantes/repetidas e crio um encaminhamento para um órgão. O encaminhamento tem um status e solução proposta."*

Entidades de domínio fixadas aqui: `User` (citizen/agent/admin), `ReportType` (dinâmico, CRUD do admin), `Report`, `Forwarding` (agregação many-to-many de relatos). A research-000074 retorna explicitamente à **camada geoespacial** do atlas original — agora em escala de bairro.

---

### As fases 7–10 são a construção do produto a ser entregue (`fala-gavea`, submódulo)

> A partir daqui, o desenvolvimento ocorre **dentro do submódulo `fala-gavea`**, que tem seu próprio ciclo SEJA (`/research → /plan → /implement → /check → /document`), numeração de planos até **000183** e **17 decisões de design** (D-001…D-017). O produto evoluiu de scaffold para uma **SPA React + API FastAPI** completa, com IA local, participação cidadã e empacotamento para deploy.

### Fase 7 — Produto MVP: domínio, auth e SPA (jun/2026)

**Protótipos entregues.**
- **Domínio + Auth + Reports** (fg:plan-000073): entidades, JWT Bearer (PyJWT + bcrypt), roles citizen/agent/admin, `POST /reports`, `GET /reports/geojson` com filtros (tipo, urgência, status, since/until, bbox).
- **ReportType CRUD** (fg:plan-000075): tipos de problema **dinâmicos** (admin), soft-delete, seed via API.
- **Forwarding CRUD** (fg:plan-000079): encaminhamento como **agregação de N relatos** selecionados, com status (aguardando → em andamento → finalizado) e solução proposta.
- **Frontend SPA React** (fg:plan-000082): migração de HTML estático para **React 18 + Vite + TypeScript + Tailwind + react-leaflet** — mapa, formulário de relato com geolocalização, painel do agente, login.

Realiza **CU1 (cidadão)** e **CU2 (agente)** end-to-end. (reflection-000086 confronta estado do CRUD vs. roadmap.)

### Fase 8 — Camada de IA: semântica, tópicos e chat (jun/2026)

**Protótipos entregues.**
- **Infra semântica** (fg:plan-000089/090): dependências de embeddings, portas Chroma, pipeline de **ingestão/indexação** de relatos com backfill.
- **Busca semântica + relatos similares** (fg:plan-000094): `GET /reports/search` e `/reports/{id}/similar` — o agente identifica **duplicatas** antes de encaminhar.
- **BERTopic topic modeling** (fg:plan-000099): modelagem de tópicos no backend.
- **Chat NL RAG** (fg:plan-000100): assistente de exploração (OllamaClient + RAG sobre relatos) que cita os relatos usados como contexto.
- **Sugestão de tipos de relato por IA** (fg:plan-000174 + reflection-000171): IA sugere `report_type` para relatos sem tópico — **estratégia plugável**, mantendo o humano no comando.

Realiza a tese de "IA como auxiliadora da curadoria" e materializa o **feedback loop** desenhado no roadmap-000070. (reflection-000097/000103: jornada de busca + visualização.)

### Fase 9 — Participação cidadã e transparência (jun/2026)

**Roadmaps.** roadmap-000146 ("cesta de relatos" — transparência ao cidadão) e roadmap-000151 (votos, comentários, anonimização).

**Protótipos entregues.**
- **Votos + comentários + relato anônimo** (fg:plan-000152–000158): schema de votos/comentários/anon-tokens, backends e UX — **validação coletiva** (o "confirmar com um clique" do CU de 10/jun) finalmente implementada.
- **"Meus relatos" + ordenação inline** (fg:plan-000164) e **"meus encaminhamentos" para o cidadão** (fg:plan-000169): o cidadão **acompanha** a demanda (fecha o "registra *e acompanha*" do CU01).
- **Filtros salvos + painel de exploração estendido** (fg:plan-000137/139), unificação da query de relatos (fg:plan-000132), refino de busca/filtros (fg:plan-000131), workspace grid com cross-filter (fg:plan-000104).

Fecha o ciclo de **corresponsabilidade** (cidadão ↔ instituições) previsto no roadmap-000070. (reflection-000144/000149/000163: jornadas de transparência e gaps.)

### Fase 10 — Meta-IA e empacotamento para entrega (jun/2026, estado atual)

**Protótipos entregues.**
- **Assistente de ajuda da plataforma (self-docs RAG)** (fg:plan-000177/000181): `POST /nl/help` responde perguntas **sobre a própria plataforma** a partir da documentação do projeto indexada no ChromaDB; para o admin, recebe um **enquadramento "meta" ciente do SEJA** (taxonomia/SDLC) como lente de interpretação (decisões D-017). A plataforma passa a **explicar a si mesma**.
- **AiBadge — marcador de proveniência de IA** (fg:plan-000178, D-015): todo conteúdo gerado por IA recebe um selo reutilizável — **transparência de proveniência** como princípio de UI.
- **Síntese de comentários de encaminhamento** (fg:plan-000179) e **embed da metodologia SEJA no helper** (fg:plan-000181).
- **Empacotamento:** Dockerfile + **deploy Railway** (fg:plan-000096/115); **pipeline de seed showcase** (fg:plan-000183) que popula todas as features (usuários, relatos, encaminhamentos, votos, comentários, filtros salvos, ciclo de vida) a partir de CSVs curados (200 linhas showcase / 5k full).
- **Documentação para 4 públicos** (fg:communication-000125 evaluators, 000126 clients, 000127 end-users, 000128 academics), acessível em `/docs/` no app em execução.

**Estado de entrega.** Produto executável localmente (API + SPA com hot-reload), via Docker, e publicável no Railway. Stack: **React 18 + FastAPI clean architecture + SQLite + ChromaDB + Ollama local**, com auth por roles, busca semântica, chat NL, votos/comentários, e um assistente que documenta o próprio sistema.

---

## 3. Mapa: casos de uso → protótipos

Como cada caso de uso atravessou o tempo até virar código entregue.

| Caso de uso (origem) | Fase de concepção | Protótipo intermediário | Implementação final (`fala-gavea`) |
|---|---|---|---|
| **Cidadão registra e acompanha demanda** (`Casos_de_uso_2`, 10/jun) | 3–4 | CitizenPost + likes (Streamlit, F3) | `POST /reports` + "Meus relatos" + votos/comentários (F7, F9) |
| **Gestor/investidor consulta para decisão** (`Casos_de_uso_1`, CU01) | 1–2 | Pipeline temas→claims→cruxes (GaveaLab PoC, F2) | Painel do agente + filtros + busca semântica + chat NL (F7–F8) |
| **Validação coletiva** ("confirmar com um clique") | 3 | likes/label feedback | Votos + comentários (fg:plan-000152–157, F9) |
| **Encaminhamento institucional** (CU2, roadmap-000071) | 5–6 | — | `Forwarding` many-to-many + status + síntese (F7, F10) |
| **IA categoriza/sugere com curadoria humana** | 1, 5 | `auto_categorize` + `PATCH /category` | Sugestão plugável de tópicos + AiBadge + feedback loop (F8, F10) |
| **Busca em linguagem natural** | 5 | intent-to-filter (plan-000068) | NL filter parser + chat RAG (fg:plan-000100/140) |
| **Camada geoespacial** (Atlas, F0) | 0 | `render_map` proposto | Mapa Leaflet + GeoJSON + bbox (F7) |
| **Plataforma se explica** (curadoria por perfil, reuniões) | 1 | — | Helper RAG self-docs SEJA-aware (fg:plan-000177/181, F10) |

---

## 4. Genealogia das decisões

Decisões que sobreviveram e moldaram o produto (D-NNN são as decisões formais do submódulo `fala-gavea`):

| Decisão | Tema | Por quê importa para a narrativa |
|---|---|---|
| Inferência **local** (CARE/OCAP → Ollama) | Soberania de dados | Invariante desde o Atlas; é o argumento ético central |
| **Zoom in** Atlas→Gávea (reflection-000052) | Escopo | Estudo de caso de redução de escopo guiada por viabilidade e validação institucional |
| Few-shot injection **em vez de** fine-tuning (roadmap-000070) | Aprendizado | Human-in-the-loop barato e auditável; cabe no semestre |
| `CategoryCurationEvent` **append-only** | Auditoria | Captura o sinal de curadoria que faltava (reflection-000069) |
| Clean architecture + submódulo SEJA (roadmap-000071) | Engenharia | Permite o produto crescer com rastro auditável próprio |
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

**1. IA no produto.** Inferência local (Ollama); categorização/sugestão de relatos; clustering semântico (embeddings + UMAP/BERTopic); busca semântica (ChromaDB); relatos similares; chat NL traduzido para filtros de API; chat RAG de exploração; e um **feedback loop few-shot com curadoria humana no comando** (o delegado confirma/corrige; a correção alimenta o prompt por injeção few-shot, não fine-tuning) → padrão **human-in-the-loop** auditável. Camada meta: o **helper RAG self-docs** faz a plataforma explicar a si mesma, e o **AiBadge** marca toda saída de IA.

**2. IA no processo de desenvolvimento.** O projeto inteiro foi construído sob o harness **SEJA** sobre Claude Code, no ciclo `/research → /plan → /implement → /check → /document | /communicate → /reflect`. Há um **rastro auditável** de centenas de artefatos numerados (advisory logs, planos, roadmaps, reflexões, QA logs, comunicações, telemetria) e o histórico de commits — um corpus que permite reconstruir não só *o que* foi construído, mas *como* e *por quê* cada inflexão de escopo ocorreu.

---

## 7. Evidências empíricas que ancoram o escopo

A decisão de "zoom in" não foi arbitrária — apoiou-se em dois corpos de evidência concretos.

**Diagnóstico GaveaLab 2023 (FAPERJ Nº 20/2022).** Pesquisa de campo do Laboratório de Gestão em Design (LGD/PUC-Rio), jun–nov/2023, **380 entrevistados** (Gávea-"asfalto", Rocinha, Parque da Cidade), coordenação Prof. Carlo Franzato e Prof. Cláudio Freitas de Magalhães, com Fabienne Torres Schiavo (Doutora em Design, CAPES). Achados usados no projeto: SEGURANÇA como tema **alavancador e dor** dos dois grupos; **divergência de percepção** sobre o que é "segurança" (policiamento vs. direitos); GOVERNANÇA como maior insatisfação. Fabienne é a stakeholder que **atestou a relevância** do caso de uso real para a entrega.

**Casos de uso co-construídos (jun/2026).** Documentos formais da disciplina registram **CU01 (cidadão registra e acompanha)** e **CU02 (gestor consulta para decisão)**, com conformidade **LGPD** e alinhamento ao **PL 2338**. São exatamente os casos que o produto atual implementa.

**Reuniões de stakeholders como fonte de design.** Transcrições (`Reunioes-stakeholders-1-2.pdf`) mostram a síntese em tempo real: Natali descrevendo o pipeline ("clusteriza, analisa com IA, descarta lixo, classifica por perfis, mostra dashboard") e a ideia de um **painel de curadoria com personas de cada ator-chave**; Andrey definindo a IA como **auxiliadora, não curadora principal**. Essas falas são a origem direta do padrão human-in-the-loop e do helper por perfil de role.

---

## 8. Roteiro de apresentação (sugerido)

Sequência de slides pronta para montar a partir das seções acima.

1. **Capa** — *fala-gávea: um canal comunitário de segurança urbana para a Gávea* (equipe, disciplina). [tese de §0]
2. **O problema** — Gávea concentra realidades radicalmente distintas (asfalto, Rocinha, Parque da Cidade) sem canal unificado de escuta. [§7, diagnóstico FAPERJ]
3. **A genealogia (zoom in)** — animar a Tabela §1 do Atlas global → bairro/segurança/2 personas. [§1, §2 F0–F4]
4. **Evidência que ancora o escopo** — MFLA, 380 entrevistados, divergência sobre "segurança". [§7]
5. **Os dois casos de uso** — cidadão registra/acompanha; agente filtra/encaminha. [§2 F6]
6. **Demo do produto** — registro com foto/GPS → mapa → busca semântica → chat NL → encaminhamento → votos/comentários. [§2 F7–F9]
7. **IA no produto** — categorização + clustering + RAG + feedback loop human-in-the-loop. [§6.1]
8. **Meta: o sistema se explica** — helper RAG self-docs + AiBadge de proveniência. [§2 F10, §4]
9. **IA no processo** — desenvolvido com SEJA/Claude Code; corpus auditável de artefatos. [§6.2, §9]
10. **Stack & entrega** — clean architecture, Docker/Railway, testes. [§5]
11. **Fechamento** — os dois invariantes (geoespacial + soberania de dados) ligam o produto final à origem amazônica; redução de escopo deliberada e documentada como mérito. [§2 fechamento]

---

## 9. O corpus de desenvolvimento como objeto de estudo

Para o eixo "AI Systems Design", o método é parte do resultado.

- **Repo-pai (`inf2921-grupo-c`):** planos 000001–000077, reflexões 000037/000052/000069, roadmaps 000007–000071, comunicações (incl. a 000075).
- **Submódulo (`fala-gavea`):** seu próprio harness SEJA — planos até **000183**, **4 roadmaps**, **11 reflexões**, **17 decisões D-NNN**, e **4 comunicações** (125–128) tornando o produto auto-documentado para evaluators/clients/end-users/academics.
- Cada artefato é numerado, datado e rastreável a um commit — permite reconstruir a cadeia *pesquisa → decisão → plano → implementação → verificação → comunicação*.

**Fechamento.** O mérito do projeto não está em ter chegado ao escopo inicial, e sim em ter feito o caminho inverso de forma deliberada e documentada. A trajetória *Atlas global → Gávea local* é um estudo de caso de **redução de escopo guiada por viabilidade, validação institucional e reaproveitamento de capacidades** — o reconhecimento de que o pipeline de clustering do agente já existia e só precisava de uma nova camada (o mapa). Os dois invariantes que sobreviveram a todas as fases — **camada geoespacial** e **soberania de dados local** — são exatamente os que conectam o produto final à sua origem amazônica.

---

## Fontes

**Base de conhecimento (kb-qa / `knowledge/`):** `Reuniao-23-04-2026.md`; `casos-de-uso.md`; `Casos_de_uso_10-06-2026_1.md`; `Casos_de_uso_10-06-2026_2.md`; `Reunioes-stakeholders-1-2.pdf`; `Strategic Design 4 Smart City Lab — Gavea Lab diagnostico_onepage.pdf` (FAPERJ 2023).

**Artefatos SEJA (repo-pai):** plans 000001–000077; reflections 000037, 000052, 000069; roadmaps 000007, 000026, 000028, 000054, 000056, 000070, 000071; [communication-000075](../2026-06-19/communication-000075-academics.md).

**Artefatos SEJA (`fala-gavea`):** plans 00002, 000073, 000075, 000079, 000082, 000089, 000090, 000094, 000096, 000099, 000100, 000104, 000131–000183; roadmaps 00001, 00002, 000146, 000151; reflections 000086–000173; decisões D-001…D-017; communications 000125–000128; `README.md`, `CLAUDE.md`.
