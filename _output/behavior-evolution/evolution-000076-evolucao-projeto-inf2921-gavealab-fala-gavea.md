# Behavior Evolution 000076 | INF2921-Grupo-C | 2026-06-25 19:44 UTC | Evolucao do projeto INF2921 -- GaveaLab + fala-gavea desde TRL1

---

## User Brief

behaviour-evolution -- also search artifacts in fala-gavea (there is a dedicated seja setup)

---

## Agent Interpretation

Este relatorio conta a historia de como o projeto INF2921 Grupo C evoluiu desde sua concepcao inicial em abril de 2026 ate o estado atual em junho de 2026. Cobre dois codebases:

1. **Repositorio principal** (`inf2921-grupo-c`): do kb-qa (ferramenta RAG generica) passando pela exploracao do Talk to the City ate o GaveaLab PoC (analise de relatos de cidadaos via Streamlit).
2. **Submodulo fala-gavea**: sistema de demandas cidadaos para seguranca urbana (FastAPI + React + ChromaDB + Ollama), que nasceu a partir do GaveaLab e evoluiu para um produto independente.

A narrativa esta organizada em fases cronologicas, cobrindo decisoes de arquitetura, mudancas de produto visives ao usuario, e os momentos de aprendizado e pivoterimento que moldaram o resultado final.

---

## Current Implementation Files

### Repositorio principal (inf2921-grupo-c)

- `gavealab-poc/app.py` -- Streamlit entry point (5 paginas de analise)
- `gavealab-poc/gavealab_poc/llm.py` -- OllamaClient (todos os LLM calls passam aqui)
- `gavealab-poc/gavealab_poc/workspace.py` -- GaveaLabWorkspace + AnalysisSession (SQLite)
- `gavealab-poc/gavealab_poc/pipeline/topics.py` -- auto-topicos via LLM
- `gavealab-poc/gavealab_poc/pipeline/claims.py` -- extracao de claims
- `gavealab-poc/gavealab_poc/pipeline/cruxes.py` -- deteccao de divergencias
- `gavealab-poc/gavealab_poc/pipeline/umap_viz.py` -- projecao UMAP + Plotly
- `src/kb_qa/` -- ferramenta RAG de suporte (kb-qa, manutencao apenas)

### Submodulo fala-gavea

- `fala-gavea/src/fala_gavea/domain/` -- entidades puras (User, Report, ReportType, Forwarding)
- `fala-gavea/src/fala_gavea/application/use_cases/` -- logica de negocio (CreateReport, CreateForwarding, etc.)
- `fala-gavea/src/fala_gavea/infrastructure/chromadb/` -- ChromaSearchClient (busca semantica)
- `fala-gavea/src/fala_gavea/infrastructure/llm/` -- OllamaClient + AnthropicClient
- `fala-gavea/src/fala_gavea/presentation/api/` -- FastAPI routers + dependencias JWT
- `fala-gavea/frontend/` -- SPA React 18 + Vite + TypeScript + Tailwind + react-leaflet

---

## Plan Files Mined

### Repositorio principal (inf2921-grupo-c)

- advisory-000002 (2026-04-24) -- Atlas Georreferenciado Amazonia IA
- advisory-000003 (2026-05-22) -- Casos de uso: espaco virtual para cidadaos e agentes
- advisory-000004 (2026-05-23) -- Talk to the City: deploy local e extensao
- plan-000001 (2026-05-24) -- TRL3 PoC -- Talk to the City local (Ollama)
- plan-000006 (2026-05-24) -- Mock Firebase Auth para PoC citizen user
- roadmap-000007 (2026-06-01) -- GaveaLab Claims Analysis PoC -- Streamlit
- plans 000008-000013 (2026-06-02) -- scaffold, CSV upload, topicos, claims, temas manuais, cruxes
- plan-000016 (2026-06-02) -- UMAP cluster visualization
- plan-000021 (2026-06-09) -- multipage app com pagina "todos os estudos"
- research-000023 (2026-06-11) -- Plataforma Fala Gavea: visao, casos de uso e roadmap
- plan-000025 (2026-06-11) -- SEJA skill: clean Python project template generator
- roadmap-000026/28 (2026-06-11) -- fala-gavea Streamlit app de participacao cidada
- plans 000029-000033 (2026-06-11) -- fala-gavea backend likes, frontend Streamlit, seed, traceabilidade
- plan-000039 (2026-06-11) -- UMAP cluster visualization de posts com AI labels
- roadmap-000054 (2026-06-16) -- Fala Gavea Seguranca: seja-clean-python + mapa Leaflet
- roadmap-000056 (2026-06-16) -- filtros-mapa-tags-ai-category
- reflection-000069 (2026-06-17) -- GaveaLab: feedback loop ausente na categorizacao por IA
- roadmap-000071 (2026-06-17) -- gavea-seguranca-demandas-app (roadmap fundador do novo fala-gavea)
- plan-000072 (2026-06-17) -- fala-gavea scaffold e seja-setup
- reflection-000052 (2026-06-15) -- Atlas da Amazonia -> zoom in para a Gavea

### Submodulo fala-gavea

- roadmap-000071 (ref. em ambos) -- roadmap fundador
- roadmap-000088 (2026-06-18) -- wave2 espacos semanticos IA
- plan-000073 (2026-06-17) -- dominio completo + auth JWT
- plan-000075 (2026-06-17) -- ReportType CRUD
- plan-000079 (2026-06-17/18) -- Forwarding CRUD
- plan-000082 (2026-06-18) -- Frontend SPA React (4 telas)
- plan-000085 (2026-06-18) -- seed relatos (1 ano de dados sinteticos)
- plan-000089/090 (2026-06-19) -- Wave 0 semantica: ChromaDB infra + indexacao
- plan-000094 (2026-06-19) -- Wave 1 busca semantica + similares
- plan-000099/100 (2026-06-19) -- BERTopic + RAG chat
- plan-000104 (2026-06-19) -- Workspace grid + cross-filter + widgets IA
- plan-000109/112/113 (2026-06-20) -- Admin panel + seed CSV endpoint
- plan-000131/132/137 (2026-06-21) -- Filtros avancados + NL filter parser
- plan-000139/140 (2026-06-21/22) -- Saved filters + NL-to-filter assistant
- roadmap-000146 (2026-06-22) -- Cesta de relatos + citizen transparency journeys
- plan-000151 (2026-06-24) -- votes + comments + anonymization
- reflection-000144 (2026-06-22) -- transparency journeys: cesta de relatos

---

## The Story: TRL 1 -> Current State

### Fase 0: Concepcao e brainstorming do grupo (abril 2026)

A historia comeca antes de qualquer codigo. Em 23 de abril de 2026, o grupo se reuniu para discutir os temas do projeto da disciplina INF2921/CIS2114 (AI Systems Design, PUC-Rio). As anotacoes desta reuniao (knowledge/Reuniao-23-04-2026.md) revelam temas emergentes: seguranca publica, vigilancia, mapeamento de espacos, acesso a informacao. O grupo cogitou um "atlas digital e iterativo assistido por IA" -- algo como um Google Maps enriquecido por dados cidadaos e curado por uma comunidade.

Nesse mesmo periodo (24/04/2026), surge o advisory-000002: uma exploracao sobre um atlas georreferenciado para a Amazonia, com dados multimodal e curadoria comunitaria. A ideia era grande -- escala continental. O que nao se sabia ainda era que, ao longo das semanas seguintes, essa ideia passaria por um "zoom in" progressivo: da Amazonia para o Rio de Janeiro, do Rio para a Gavea.

**O que o usuario experimentava nessa fase:** Nada -- o projeto ainda nao existia como codigo. Mas a ideia-forca estava presente: dados de cidadaos + IA + mapa + gestao publica.

---

### Fase 1: Primeira exploracao tecnica -- Talk to the City e kb-qa (maio 2026)

O mes de maio foi o mes das exploracoes tecnicas. Dois caminhos foram abertos em paralelo.

**Caminho A: Talk to the City (22-24/05/2026)**

Em 22 de maio, o advisory-000003 cristalizou tres casos de uso para uma plataforma de participacao cidada. A pesquisa foi abrangente: comparou Decidim, Pol.is, Talk to the City, CitizenLab, Consul e vTaiwan. A conclusao foi clara: a arquitetura do Talk to the City (T3C) -- pipeline de embedding + clustering + rotulagem via LLM -- era buildavel sobre a stack ja existente (sentence-transformers + ChromaDB + SDK Anthropic).

Em 23 de maio, o advisory-000004 explorou como rodar o T3C completamente local, sem dependencias de nuvem. Existia um fork da comunidade (`tttc-light-js-ollama`) que ja substituia OpenAI por Ollama. A ideia: monorepo Node.js (Next.js + Express + pipeline worker), substituindo Firebase, Google Cloud Storage e Pub/Sub por equivalentes locais.

Em 24 de maio, o plan-000001 tentou executar esse TRL 3: clonar o fork, criar Docker Compose, gerar dados de teste do GaveaLab e rodar o pipeline local. Os steps 1, 2 e 3 foram executados. Steps 4 e 5 -- a demo final -- ficaram inconclusos. O sistema funcionou parcialmente, mas o esforco de adaptar o ecossistema Node.js para o contexto do grupo era maior do que o retorno.

**Caminho B: kb-qa (maio 2026)**

Enquanto o T3C era explorado, o time construiu o kb-qa: uma ferramenta RAG generica em Python para indexar documentos `.md` e `.pdf` via ChromaDB e expor `query_knowledge` como tool MCP para sessoes Claude Code. O kb-qa foi implementado com decisoes arquiteturais documentadas (D-001 a D-003): ChromaDB como vector store local, FastMCP como interface, nomic-embed-text-v1 como modelo de embedding. Esta ferramenta resolveu um problema imediato do proprio time -- consultar materiais de curso nas sessoes de IA -- e permanece ativa como ferramenta de suporte.

**O que o usuario experimentava:** Ao final de maio, existia uma ferramenta CLI (kb-qa) que permitia indexar PDFs de aula e consult-a-los via Claude. O T3C nao chegou a uma demo funcional end-to-end.

**A virada:** A tentativa com o T3C revelou algo importante. A stack JavaScript (Next.js + Express + worker) era pesada de manter, especialmente para substituir Firebase e GCS. Ao mesmo tempo, a equipe tinha o pipeline Python do T3C praticamente entendido. A pergunta que surgiu: e se reimplementassemos o pipeline em Python puro, com Streamlit, usando Ollama local?

---

### Fase 2: GaveaLab emerge como produto primario -- Streamlit PoC (1-11 junho 2026)

Em 01 de junho de 2026, uma unica noite de trabalho produziu o roadmap-000007, que mudou a direcao do projeto. O brief era simples: "quero re-implementar um fluxo de tratamento de relatos/claims de cidadaos em uma stack mais simples. quero implementar em python usando streamlit."

Pense nessa decisao como trocar um carro de competicao complicado por uma bicicleta elegante: perdeu-se a potencia bruta da plataforma T3C completa, mas ganhou-se velocidade de desenvolvimento, clareza de arquitetura e facilidade de demonstracao.

**O roadmap-000007 definia 6 planos em 3 waves:**

Wave 0: scaffold + OllamaClient (plan-000008)
Wave 1: CSV upload + topicos automaticos + claims (plans 000009-000011)
Wave 2: categorizacao manual + deteccao de cruxes (plans 000012-000013)

Tudo isso foi executado em um unico dia (02 de junho de 2026). Os decisions D-004 e D-005 foram registrados: Streamlit + SQLite para UI e persistencia; Ollama como backend LLM.

Em seguida, plan-000016 adicionou a visualizacao UMAP -- um scatter plot 2D de claim embeddings via Plotly, onde a proximidade espacial indica similaridade semantica de opiniao. E plan-000021 adicionou multipage navigation com uma pagina "todos os estudos".

**Analogia para o leitor nao-tecnico:** O GaveaLab funciona como um assistente de pesquisa que le centenas de comentarios de cidadaos e automaticamente: (1) descobre os temas principais discutidos, como "transporte" e "seguranca"; (2) extrai as ideias-chave de cada tema em frases claras; (3) identifica onde os cidadaos genuinamente discordam; (4) gera um mapa visual onde comentarios semanticamente proximos aparecem agrupados.

```
Jornada do pesquisador no GaveaLab:
Upload CSV -> [LLM descobre topicos] -> revisar -> [LLM extrai claims] 
          -> [LLM detecta cruxes] -> ver mapa UMAP
```

**O que o usuario experimentava ao final da Fase 2:**

- Uma interface web local (Streamlit) com 5 paginas de analise
- Upload de CSV com coluna `text` cria sessao persistente no SQLite
- "Temas automaticos": LLM gera arvore de topicos/subtopicos dos relatos
- "Categorizar por temas": usuario define temas, LLM classifica relatos
- "Opinioes divergentes": cruxes identificados pelo LLM
- "Visualizar clusters": scatter plot 2D interativo (hover mostra texto da claim)
- Sessoes persistem entre navegacoes via SQLite

**Regras ativas:**
- Relatos < 10 caracteres sao descartados no upload
- Todos os LLM calls passam por `gavealab_poc/llm.py` (OllamaClient) -- T1
- Todo acesso ao SQLite passa por `GaveaLabWorkspace` -- T2
- `gavealab.db` e gitignored (dados de cidadaos nunca commitados) -- S2
- LLM roda local via Ollama (dados nao saem da maquina) -- C1

---

### Fase 3: A visao se divide -- dois produtos surgem (11-17 junho 2026)

Em 11 de junho, algo importante aconteceu: o time percebeu que estava construindo metade de um sistema maior. A pesquisa research-000023 (Plataforma Fala Gavea: visao, casos de uso e roadmap) sintetizou dois documentos de casos de uso da equipe e revelou a arquitetura completa.

**A metafora dos dois aneis:**

O GaveaLab era o "anel interno" -- o motor de analise. O pesquisador ingestava CSVs, rodava o pipeline de IA, revisava resultados. Mas faltava o "anel externo" -- a plataforma de participacao cidada onde o proprio cidadao envia problemas em tempo real.

```
SUBSISTEMA A: Camada de Input Cidadao (visao futura)
  App movel, web, totens fisicos
  -> submissao, validacao coletiva
  -> produz: CSV estruturado de relatos
              |
              v  (contrato de dados: CSV / API)
SUBSISTEMA B: Motor de Analise (GaveaLab PoC -- ja implementado)
  Upload CSV -> topics -> claims -> cruxes -> UMAP
  Revisao humana -> publicacao -> painel decisores
```

Esta arquitetura de dois subsistemas foi a decisao de design mais importante do projeto. Ela significava: o GaveaLab continuaria como motor de back-office de analise; um novo projeto -- fala-gavea -- seria o frontend civico de participacao.

**A equipe tambem produziu o SEJA skill (plan-000025):** um gerador de projetos Python com clean architecture, FastAPI, SQLite/SQLAlchemy, Pydantic v2 e pytest. Esta ferramenta interna foi fundamental para criar o fala-gavea com velocidade e consistencia.

**Primeira versao do fala-gavea (Streamlit, 11 junho):**

Os roadmaps 000026 e 000028 planejaram rapidamente um app Streamlit de participacao cidada com posts e likes. Os plans 000029-000033 implementaram: backend REST com likes e feedback de labels; app Streamlit consumindo a API; seed de dataset fake; traceabilidade de likes (saber quem curtiu quem). O plan-000039 adicionou visualizacao UMAP dos posts com labels gerados por IA.

Esta versao Streamlit do fala-gavea era funcional mas limitada. A equipe conseguia ver posts de cidadaos, dar likes, ver clusters de opiniao. Mas era uma interface de back-office, nao uma plataforma publica.

**A reflexao que mudou tudo (15 de junho):**

Em 15 de junho, o reflection-000052 capturou uma conversa de WhatsApp da equipe. Natali propos "nao recomecar, mas misturar o que ja existe (clustering) com um mapa georreferenciado." Andrey formalizou dois casos de uso: (1) cidadao que reporta problema de seguranca com foto e localizacao GPS; (2) delegado que explora dashboard georreferenciado com filtros e chat. Ele tambem revelou a linha genealogica: "do atlas da Amazonia para a Gavea". A ideia-forca original -- atlas georreferenciado -- havia retornado com maturidade tecnica acumulada.

---

### Fase 4: fala-gavea se torna produto independente (17-25 junho 2026)

Em 17 de junho, o roadmap-000071 ("gavea-seguranca-demandas-app") fundou o fala-gavea como produto independente. Era um documento de 5 decisoes arquiteturais (D-A a D-F) e uma estrutura de 3 waves.

**Decisoes fundadoras do fala-gavea (roadmap-000071):**

- D-A: Novo projeto independente via python-scaffold (nao extensao do fala-gavea-seguranca anterior)
- D-B: Tipos de problema dinamicos via tabela `ReportType` -- admin adiciona categorias sem redeployar codigo
- D-C: JWT Bearer com roles `citizen`, `agent`, `admin` -- sem OAuth externo, registro simples
- D-D: Forwarding como agregacao many-to-many de relatos -- o agente nao responde relato a relato, agrupa e encaminha o conjunto
- D-E: IA como assistencia, nao automacao -- ChromaDB + sentence-transformers para busca semantica; chat NL para explorar padrao; o agente decide
- D-F: Frontend minimal HTML estatico + Leaflet (logo substituido por React)

**Wave 0 -- Scaffold + dominio (plan-000072, plan-000073, plan-000075):**

Em poucas horas, o fala-gavea foi criado do zero com o SEJA skill. O plan-000073 implementou o dominio completo: User (roles citizen/agent/admin), Report, ReportType, Forwarding, ForwardingReport. Autenticacao JWT Bearer. Endpoints: POST /auth/register, POST /auth/token, POST /reports, GET /reports/geojson (publico), GET /reports/{id}. O plan-000075 adicionou ReportType CRUD (apenas admin).

**Wave 1 -- Fluxo do agente publico (plan-000079, plan-000082):**

O plan-000079 implementou Forwarding CRUD: o agente seleciona relatos, cria encaminhamento para um orgao, atualiza status. Quando um encaminhamento e criado, todos os relatos incluidos transitam automaticamente para status `encaminhado` -- um invariante de dominio mantido por uma transacao SQLAlchemy. O plan-000082 deu o salto mais visivel: saiu das paginas estaticas HTML e adotou React 18 + Vite + TypeScript + Tailwind CSS + react-leaflet. Esta decisao (D-006 -> D-007 no design intent do fala-gavea) transformou a UI de paginas desconexas em uma SPA com estado compartilhado.

**Wave 2 -- IA: espacos semanticos (roadmap-000088, plans 000089-000100):**

Em 18-19 de junho, o roadmap-000088 substituiu a premissa de um unico modelo ChromaDB por uma arquitetura de multiplos espacos semanticos especializados por proposito:

- `falagavea_reports_search` (colecao ChromaDB): busca semantica e relatos similares, modelo `intfloat/multilingual-e5-base`
- BERTopic (artefato separado): clusterizacao de topicos, modelo `paraphrase-multilingual-MiniLM-L12-v2`

O plan-000089 criou a infraestrutura semantica. O plan-000090 adicionou indexacao na criacao de relatos (via porta de dominio `IReportIndexer` -- sem acesso direto a ChromaDB nos use cases). O plan-000094 implementou busca semantica (`GET /reports/search?q=&n=`) e relatos similares (`GET /reports/{id}/similar?n=`). O plan-000100 adicionou o RAG chat (`POST /chat`) com suporte a dois provedores de LLM: Ollama (local, default) e Anthropic (via SDK oficial, configuravel por env var).

**A decisao de provedor LLM e uma decisao etica:** O design intent explicita que `ollama` mantem os textos dos relatos locais; `anthropic` envia o contexto recuperado para API externa. O default `ollama` preserva a privacidade dos dados dos cidadaos.

**Frontend evoluindo (plans 000104-000140):**

A partir de 19 de junho, o frontend cresceu rapidamente:

- plan-000104: Workspace grid com Zustand store, cross-filter entre mapa e tabela, widgets IA (Topicos, Similares, chat RAG)
- plan-000109/112/113: Admin panel no frontend (upload de CSV de seed, wipe DB), endpoint de seed em bulk
- plans 000131/132/137: Overhaul do painel de filtros -- painel esquerdo em 4 secoes (presets, chips ativos, controles draft, NL assistant), modelo staged-draft/Apply, presets de data, tabela com sort + full-text + paginacao, filtro draw-area no mapa
- plans 000139/140: Saved filters (CRUD de filtros nomeados), NL-to-filter assistant (chat que converte intencao em parametros de filtro e sugere ao usuario aplicar)

**Cesta de relatos e transparencia do cidadao (roadmap-000146, plans 000151-000170):**

Em 22-24 de junho, o foco virou para as jornadas de usuario completas. O reflection-000144 capturou a visao do "carrinho de compras de relatos": o agente adiciona relatos a uma cesta sem sair da interface, ve o contador no canto superior direito, verifica similares em aberto, e cria o encaminhamento. O roadmap-000146 implementou esta visao em 3 waves (backend + cesta + citizen UX). O plan-000151 adicionou votos e comentarios. Os plans 000161-000170 fecharam jornadas do cidadao: login, ver meus relatos, ver encaminhamentos, visibilidade dos votos inline.

**Deploy (plan-000096, plan-000115):**

O plan-000096 criou um Dockerfile para deploy no Railway. O plan-000115 corrigiu problemas de configuracao: JWT_SECRET_KEY em .env.example, DATABASE_URL absoluto, /health com DB probe, remocao de frontend/dist/ do .dockerignore. O fala-gavea ficou deployavel em um servico de cloud com um unico Dockerfile.

---

## Evolution Timeline

| # | Data | Evento | Tipo | Impacto no usuario |
|---|------|--------|------|-------------------|
| 1 | 2026-04-24 | advisory-000002: Atlas Georreferenciado Amazonia -- ideias iniciais | Brainstorming | Nenhum (pre-produto) |
| 2 | 2026-05-22 | advisory-000003: 3 casos de uso para plataforma participativa cidada; pesquisa Decidim/Pol.is/T3C | Pesquisa | Nenhum (definicao de escopo) |
| 3 | 2026-05-23 | advisory-000004: exploracao do Talk to the City local com Ollama | Pesquisa tecnica | Nenhum |
| 4 | 2026-05-24 | plan-000001 + kb-qa: TRL3 PoC T3C rodando parcialmente; kb-qa funcional | Implementacao | Ferramenta RAG CLI disponivel para o time |
| 5 | 2026-06-01 | roadmap-000007: decisao de reimplementar pipeline T3C em Python + Streamlit | PIVOT | --  |
| 6 | 2026-06-02 | plans 000008-000013: GaveaLab PoC implementado em um dia (scaffold, CSV upload, topicos, claims, cruxes) | Implementacao | 1a interface de analise de relatos funcionando |
| 7 | 2026-06-02 | D-004 (Streamlit + SQLite) e D-005 (Ollama) registrados | Decisao arquitetural | Sessoes persistentes entre navegacoes |
| 8 | 2026-06-02 | plan-000016: UMAP cluster visualization | Implementacao | Mapa visual de opinoes no GaveaLab |
| 9 | 2026-06-09 | plan-000021: multipage app + pagina "todos os estudos" | Implementacao | Navegacao entre sessoes no GaveaLab |
| 10 | 2026-06-11 | research-000023: arquitetura de dois subsistemas (anel interno + anel externo) | Pesquisa/decisao | Clarificacao de escopo -- GaveaLab e o motor, fala-gavea e o frontend civico |
| 11 | 2026-06-11 | plan-000025: SEJA skill criado | Tooling | Gerador de projetos Python com clean architecture |
| 12 | 2026-06-11 | roadmaps 000026/028 + plans 000029-000033: fala-gavea v1 (Streamlit + likes + UMAP) | Implementacao | 1a versao de participacao cidada (Streamlit) |
| 13 | 2026-06-15 | reflection-000052: "zoom in da Amazonia para a Gavea"; mapa + seguranca urbana como foco | Reflexao/pivot | Definicao da vertical tematica: seguranca urbana, Gavea |
| 14 | 2026-06-17 | roadmap-000071: fala-gavea refundado como produto independente (FastAPI + React + JWT) | REFUNDACAO | Nova stack; novo produto |
| 15 | 2026-06-17 | plan-000072/073/075: scaffold + dominio completo + auth JWT + ReportType CRUD | Implementacao | 14 endpoints REST vivos; autenticacao funcional |
| 16 | 2026-06-18 | plan-000079: Forwarding CRUD (agente agrupa relatos e encaminha) | Implementacao | Jornada do agente publico completa (backend) |
| 17 | 2026-06-18 | plan-000082: SPA React substitui HTML estatico (D-007) | FRONTEND PIVOT | UI moderna, estado compartilhado, react-leaflet |
| 18 | 2026-06-18 | roadmap-000088 + plan-000089/090: espacos semanticos multiplos + indexacao na criacao | Implementacao | Busca semantica e RAG habilitados |
| 19 | 2026-06-19 | plans 000094/099/100: busca semantica + similares + BERTopic + RAG chat | Implementacao | Cidadao e agente podem buscar por conteudo, ver similares, chatear com IA |
| 20 | 2026-06-19 | plan-000104: workspace grid + Zustand + cross-filter + widgets IA | Implementacao | Interface exploratoria unificada (mapa + tabela + IA) |
| 21 | 2026-06-20 | plans 000109-000115: admin panel + seed CSV + deploy Railway | Implementacao | App deployavel em cloud; admin pode popular banco via frontend |
| 22 | 2026-06-21 | plans 000131-000140: filtros avancados + NL-to-filter assistant + saved filters | Implementacao | Usuario digita intencao em linguagem natural, IA sugere filtros |
| 23 | 2026-06-22 | roadmap-000146: cesta de relatos + citizen transparency journeys | Implementacao | Agente tem "carrinho de relatos"; cidadao ve seus relatos e encaminhamentos |
| 24 | 2026-06-24 | plans 000151-000170: votos + comentarios + meus relatos + encaminhamentos do cidadao | Implementacao | Jornadas de transparencia do cidadao completas |
| 25 | 2026-06-25 | reflection-000171: IA para sugerir topicos em relatos sem topico | Reflexao | Proximo passo: loop de feedback humano -> modelo |

---

## Key Architectural Shifts

### Shift 1: De Node.js (T3C) para Python + Streamlit (junho 2026)

**O que era:** Monorepo JavaScript (Next.js + Express + pipeline worker), dependente de ecossistema Firebase/GCS/PubSub, adaptado a partir do fork tttc-light-js-ollama.

**O que se tornou:** Aplicacao Python monolitica (Streamlit + SQLite + Ollama), 100% local, sem dependencias de servicos externos.

**Por que mudou:** O esforco de adaptar o ecossistema Node.js superava o valor para o escopo do curso. Python era a lingua nativa do time e do kb-qa existente. Streamlit permitia demos rapidas. A logica do pipeline (embed -> cluster -> label) era equivalente.

**Impacto no usuario:** O pesquisador ganha uma interface web local que abre em segundos, sem infraestrutura. Perde-se a visualizacao interativa rica do T3C, mas ganha-se a capacidade de modificar cada etapa do pipeline.

---

### Shift 2: De kb-qa como produto principal para GaveaLab + fala-gavea (junho 2026)

**O que era:** kb-qa era o entregavel principal do curso -- uma ferramenta RAG generica para indexar documentos de aula.

**O que se tornou:** kb-qa ficou como ferramenta de suporte. GaveaLab emergiu como produto de analise de discurso civico. fala-gavea emergiu como plataforma de participacao cidada.

**Por que mudou:** O advisory-000003 revelou que o problema realmente interessante era cidadania participativa mediada por IA, nao RAG generico. Os casos de uso do GaveaLab (pesquisadora analisa relatos de consulta publica) e do fala-gavea (cidadao registra problema, delegado encaminha) eram mais ricos, mais academicamente interessantes, e tinham demanda institucional real (Fabiene e o GaveaLab).

---

### Shift 3: De fala-gavea Streamlit para fala-gavea FastAPI + React (junho 2026)

**O que era:** fala-gavea v1 era um app Streamlit sobre uma API REST simples, com posts e likes mas sem autenticacao real.

**O que se tornou:** FastAPI com clean architecture (domain/application/infrastructure/presentation), JWT Bearer com roles, React 18 + TypeScript + Tailwind + react-leaflet.

**Por que mudou:** Streamlit e um app de analise, nao uma plataforma civica. A jornada "cidadao registra problema no mapa, agente encaminha para orgao publico" exige: autenticacao com roles, UI de mapa interativo com geolocation do browser, estado compartilhado entre mapa e tabela, e frontend que funcione em mobile. Nada disso cabe bem em Streamlit.

O roadmap-000071 documentou esta decisao arquitetural explicitamente (D-A a D-F). O plan-000082 executou a mudanca de stack de frontend.

---

### Shift 4: De modelo semantico unico para multiplos espacos por proposito (junho 2026)

**O que era:** O design original do fala-gavea assumia uma unica colecao ChromaDB com um unico modelo de embedding.

**O que se tornou:** Um registry de provedores de embedding por proposito: `search`/`rag` usa `intfloat/multilingual-e5-base`; `topics` usa `paraphrase-multilingual-MiniLM-L12-v2` (backbone do BERTopic). Configuravel por env vars.

**Por que mudou:** BERTopic tem requisitos diferentes de um modelo de busca semantica. Modelos de topicos precisam de representacoes que capturem agrupamentos tematicos; modelos de busca precisam de representacoes que capturem similaridade de conteudo para consultas em linguagem natural. A abstracao via registry permite usar o modelo certo para cada proposito, e trocar sem modificar use cases.

---

### Shift 5: Da busca manual para exploração por linguagem natural (junho 2026)

**O que era:** O agente filtrava relatos por campos estruturados (tipo, urgencia, data, area geografica via bbox).

**O que se tornou:** Um assistente de NL no painel esquerdo que aceita intencoes em linguagem natural ("relatos de iluminacao da semana passada com urgencia alta") e sugere os parametros de filtro correspondentes para o usuario revisar e aplicar. Filtros nomeados podem ser salvos e reutilizados.

**Impacto no usuario:** O agente publico nao precisa mais saber que existe um campo `urgency` com valores `alta`/`media`/`baixa`. Pode descrever o que quer em portugues e revisar a interpretacao da IA antes de aplica-la. A distancia entre intencao e acao reduziu dramaticamente.

---

## How Behavior Changed for Users

### Para o pesquisador de dados civicos (GaveaLab)

**Antes (maio 2026):** Nenhuma ferramenta especifica. O pesquisador lia centenas de relatos manualmente, destacava temas, escrevia sumarios. Um processo de dias ou semanas para uma consulta media.

**Depois (junho 2026):** Upload de CSV -> LLM descobre temas automaticamente em minutos -> pesquisador revisa arvore de topicos -> claims extraidas por tema -> divergencias identificadas -> mapa visual de clusters semanticos. Um processo de horas, com resultados que retornam ao pesquisador para revisao humana antes de qualquer publicacao.

**O que nao mudou:** A decisao final e sempre do pesquisador. O LLM propoe; o humano valida. Este principio, enraizado no design intent desde o advisory-000003, foi mantido por todo o ciclo.

---

### Para o cidadao da Gavea

**Antes (maio 2026):** Sem canal digital local para relatos urbanos. O equivalente seria ligar para a prefeitura, enviar email, ou nao reportar.

**Depois (junho 2026, fala-gavea):** Entra no site, registra em sua conta, clica no mapa no ponto do problema, preenche formulario (tipo de problema, urgencia, descricao em texto livre), envia. O GPS do browser preenche a localizacao automaticamente. Pode ver lista de seus proprios relatos, ver encaminhamentos que incluem seus relatos, e votar em relatos de outros cidadaos que acha relevantes.

**O que o cidadao ve no mapa:** Todos os relatos publicos como marcadores coloridos por urgencia (vermelho = alta, laranja = media, azul = baixa). Ao clicar, ve detalhes do relato. Pode buscar relatos por descricao em linguagem natural ("buraco na rua perto do metro").

---

### Para o agente publico (delegado, gestor)

**Antes:** Dashboard estatico, planilhas, ligacoes de cidadaos. Sem agregacao automatica de problemas similares. Cada relato tratado individualmente.

**Depois (junho 2026, fala-gavea):** Acessa workspace grid com mapa e tabela sincronizados. Filtra relatos por tipo, urgencia, data, area geografica, ou descricao em linguagem natural. Adiciona relatos a uma "cesta" (analogia ao carrinho de compras) sem sair da interface. Verifica se existem relatos similares em aberto para adicionar ao conjunto. Cria um encaminhamento formal para um orgao (RioLuz, COMLURB, 9a Delegacia) com todos os relatos agrupados e a solucao proposta. O sistema atualiza automaticamente o status de cada relato para "encaminhado". Pode acompanhar o status do encaminhamento ate "finalizado".

**O chat RAG:** O agente pode perguntar em portugues "quais sao os problemas mais urgentes de iluminacao registrados nos ultimos 30 dias?" e receber uma resposta contextualizada com links para os relatos citados. Esta funcionalidade e restrita a agentes e admins -- cidadaos nao tem acesso ao chat (decisao de permissao documentada).

---

### Para o administrador do sistema

**Antes:** Tipos de problema hardcoded no codigo -- adicionar uma nova categoria exigia redeploy.

**Depois:** CRUD dinamico de ReportType via admin panel no frontend. Upload de CSV com relatos em bulk. Wipe de banco com confirmacao. Criacao de contas seed para testes. Sem redeploy necessario para operacoes administrativas rotineiras.

---

## What Didn't Work

### Tentativa 1: Talk to the City completo (maio 2026)

O plan-000001 tentou validar o TRL 3 do T3C rodando local. Os steps de criacao do Docker Compose e configuracao de ambiente funcionaram. A demo end-to-end (submit CSV, ver clusters no browser) ficou incompleta. O ecossistema JavaScript do T3C -- com Firebase, GCS, PubSub e BullMQ como dependencias -- era mais pesado do que o escopo do projeto. A alternativa correta foi reimplementar o pipeline em Python, que a equipe conhecia melhor.

**Licao aprendida:** Adaptar um monorepo complexo de terceiros para remover dependencias de nuvem pode custar mais do que reimplementar o nucleo funcional na linguagem preferida do time.

---

### Tentativa 2: fala-gavea como extensao do projeto anterior (junho 2026)

Em meados de junho, existia um `fala-gavea-seguranca/` -- um projeto anterior com algumas rotas basicas. O roadmap-000071 tomou a decisao explicita de nao extende-lo, mas criar um novo projeto do zero via `/python-scaffold` (decisao D-A). O motivo: o projeto anterior nao tinha clean architecture, nao tinha autenticacao robusta, e nao tinha a estrutura de testes necessaria para crescer com a velocidade que o roadmap demandava.

**Licao aprendida:** Partir de um scaffold limpo, mesmo perdendo algum codigo ja escrito, pode ser mais rapido do que carregar divida tecnica acumulada.

---

### Tentativa 3: Frontend HTML estatico (junho 2026)

O roadmap-000071 (D-F) especificou inicialmente "Frontend minimal -- HTML estatico + Leaflet". Esta decisao foi explicitamente revertida em plan-000082 (D-007). HTML estatico funcionou para validar o backend, mas nao suportava o modelo de estado compartilhado que as funcionalidades de IA exigiam: filtros que afetam simultaneamente o mapa, a tabela e os widgets de IA requerem um store global (Zustand). O React + TypeScript deu a base necessaria para crescer a UI sem que o estado se tornasse ingerenciavel.

**Licao aprendida:** "Minimal" no frontend pode ser uma falsa economia quando a interatividade entre multiplos componentes e o requisito central.

---

### Tentativa 4: Feedback loop ausente na categorizacao por IA (junho 2026)

O reflection-000069 identificou uma lacuna importante: o sistema capturava correces do delegado (quando ele editava a categoria sugerida pela IA), mas nao usava esses pares (sugestao IA -> correcao humana) como dados de treinamento ou avaliacao. O loop humano-IA existia na interface mas nao fechava no modelo.

**Estado atual:** Este gap foi identificado mas nao resolvido dentro do prazo do curso. A reflection-000171 retomou o tema em 25 de junho, explorando como a IA poderia sugerir topicos para relatos sem topico -- um primeiro passo para o loop de feedback.

**Licao aprendida:** Capturar feedback humano e facil; usa-lo para melhorar o modelo e um problema de engenharia de ML diferente, com requisitos proprios de dataset, fine-tuning e avaliacao.

---

## Current State Summary

### GaveaLab (repositorio principal, produto de analise)

O GaveaLab e um app Streamlit local para analise de discurso civico a partir de CSVs. O pesquisador sobe um arquivo com coluna `text`, nomeia a sessao, e tem acesso a um pipeline de IA em 5 etapas:

1. **Upload + sessao**: CSV carregado, sessao persistida no SQLite. Relatos < 10 chars descartados.
2. **Temas automaticos**: LLM (qwen3:8b via Ollama) gera arvore de topicos/subtopicos.
3. **Categorizacao manual**: pesquisador define temas, LLM classifica cada relato.
4. **Claims**: LLM extrai afirmacoes distiladas por topico, cada uma com citacao do relato original.
5. **Cruxes**: LLM identifica pontos de genuina divergencia entre claims do mesmo topico.
6. **Visualizacao UMAP**: scatter plot 2D interativo de claim embeddings; hover mostra texto e topico.

Sessoes persistem entre navegacoes. Re-run em qualquer etapa nao afeta as outras. Dados nao saem da maquina (C1). Produto de curso demonstrado; em manutencao.

---

### fala-gavea (submodulo, produto de participacao civica)

O fala-gavea e uma plataforma web para demandas cidadaos de seguranca urbana na Gavea (Rio de Janeiro). Em producao via Railway (Dockerfile), com seed de ~5000 relatos sinteticos de 1 ano.

**O que funciona hoje:**

- **Cidadao**: cria conta, registra relato no mapa (click -> formulario inline), ve seus relatos, ve encaminhamentos com seus relatos, vota em relatos de outros cidadaos
- **Agente publico**: explora relatos em workspace grid (mapa + tabela sincronizados), filtra por tipo/urgencia/data/area/texto em NL, adiciona relatos a cesta, cria encaminhamento para orgao, atualiza status
- **Administrador**: CRUD de tipos de problema, upload de CSV de seed, wipe de banco, gestao de usuarios
- **IA habilitada**: busca semantica (`GET /reports/search?q=`), relatos similares (`GET /reports/{id}/similar?n=`), clusterizacao por topicos (BERTopic, `GET /reports/topics`), RAG chat (`POST /chat` para agents/admins), NL-to-filter assistant no painel esquerdo, filtros salvos (CRUD)

**Stack tecnologica atual:**
- Backend: FastAPI + SQLAlchemy + SQLite + PyJWT + ChromaDB + sentence-transformers + BERTopic + Ollama/Anthropic (plugavel)
- Frontend: React 18 + Vite + TypeScript + Tailwind + shadcn-style + react-leaflet + Zustand
- Deploy: Railway (Dockerfile)

**O que ainda nao esta implementado:**

- Loop de feedback: pares (sugestao IA -> correcao humana) como dados de treino
- Sugestao automatica de topicos para relatos sem topico (reflection-000171)
- Notificacoes push para cidadaos sobre andamento de encaminhamentos
- Export de resultados para CSV/JSON
- Testes de frontend (apenas backend pytest)

---

## Active Rules and Constraints (Estado atual)

### GaveaLab

| Regra | Tipo | Origem |
|-------|------|--------|
| Relatos < 10 chars descartados no upload | Validacao | design intent §10 |
| Todos os LLM calls passam por `gavealab_poc/llm.py` | Arquitetural (T1) | constitution v2 |
| Todo acesso SQLite passa por `GaveaLabWorkspace` | Arquitetural (T2) | constitution v2 |
| `gavealab.db` gitignored -- dados nao commitados | Seguranca (S2) | constitution v2 |
| Ollama roda local -- dados nao saem da maquina | Privacidade (C1) | constitution v2 |
| Uma instancia de `GaveaLabWorkspace` por processo via `@st.cache_resource` | Arquitetural (T5) | constitution v2 |

### fala-gavea

| Regra | Tipo | Origem |
|-------|------|--------|
| Todos os LLM calls e buscas semanticas passam pelo `infrastructure/` | Arquitetural (CONV-1) | CLAUDE.md fala-gavea |
| Nenhum router acessa JWT diretamente -- usar `dependencies.py` | Seguranca (CONV-2) | CLAUDE.md fala-gavea |
| Type annotations obrigatorias em todas funcoes publicas | Qualidade (CONV-3) | CLAUDE.md fala-gavea |
| LLM model e URL vem de env vars (nao hardcoded) | Seguranca (CONV-3) | CLAUDE.md fala-gavea |
| Relatos sem hard delete -- permanentes para auditoria civica | Dominio | design intent fala-gavea §2 |
| `n_results` cap 20 no kb-qa MCP | Limite de consumo (T8) | constitution v1 |
| Cidadao nao acessa /chat (apenas agent/admin) | Permissao | roadmap-000088 D-F |
| `database.db` gitignored -- dados cidadaos nao commitados | Seguranca | constitution fala-gavea |

---

## Metacommunication Message

### Versao resumida (para uso em apresentacao do curso)

Nos partimos de uma ideia grande -- um atlas georreferenciado assistido por IA -- e chegamos a dois produtos concretos que demonstram como IA pode servir a democracia participativa sem substituir o julgamento humano. O GaveaLab permite que pesquisadores transformem centenas de relatos de cidadaos em insight estruturado (temas, afirmacoes, divergencias, mapa visual) em horas. O fala-gavea permite que cidadaos da Gavea registrem problemas urbanos e que agentes publicos os explorem, agrupem e encaminhem com apoio de busca semantica, relatos similares e chat em linguagem natural. Em ambos os sistemas, a IA propoe e o humano decide.

### Versao detalhada (perspectiva de evolucao)

Eu sei que voce e um pesquisador, agente publico ou estudante que precisa lidar com grandes volumes de vozes cidadas -- relatos de consultas publicas, demandas de seguranca, problemas urbanos -- e que a alternativa atual e ler tudo manualmente, perder nuances e demorar dias. Por isso projetamos dois sistemas que se complementam.

O GaveaLab cuida do problema de analise: pega um CSV de relatos e retorna uma estrutura analitica -- temas, afirmacoes, divergencias, mapa de clusters -- em minutos. Cada resultado e revisavel pelo pesquisador antes de qualquer publicacao. Nenhum dado sai da maquina.

O fala-gavea cuida do problema de coleta e encaminhamento: cidadaos registram problemas no mapa em tempo real, agentes publicos exploram esses registros com ferramentas de IA (busca semantica, relatos similares, filtros por intencao em portugues) e criam encaminhamentos formais para os orgaos responsaveis. O cidadao pode acompanhar o status.

A trajetoria de TRL 1 (brainstorming de abril) a TRL 4-5 (produto deployado de junho) em 8 semanas foi possivel porque o time foi disciplinado em tomar decisoes arquiteturais explicitas -- documentadas em decisions D-001 a D-005 no GaveaLab e D-A a D-G no fala-gavea -- e em pivotar quando o caminho nao funcionava (T3C -> Streamlit; HTML estatico -> React).

O que ficou por fazer e o que o projeto revelou como proximo passo natural: o loop de feedback humano -> modelo. Cada vez que o delegado corrige a categoria sugerida pela IA, esse par e um dado de treinamento. Quando houver pares suficientes, e possivel afinar o modelo local para o contexto especifico da Gavea. Esse e o passo que transforma o PoC em uma plataforma que aprende com o uso.

---

*Gerado por behavior-evolution agent | INF2921-Grupo-C | 2026-06-25 19:44 UTC*
