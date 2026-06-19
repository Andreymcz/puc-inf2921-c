# Communication 000075 | ACD | 2026-06-19 14:33 UTC | Academics

> Relatorio de desenvolvimento para a avaliacao academica do projeto de capstone INF2921/CIS2114 (AI Systems Design, PUC-Rio, 2026.1). Equipe: Andrey, Mauro, Julia, Herbert, Natali, Sheila.

## Visao geral

O projeto entregue hoje - "fala-gavea" - e o resultado de uma trajetoria de design que partiu de uma ambicao global (um Atlas Digital Georreferenciado da Amazonia assistido por IA) e convergiu, por sucessivas decisoes de escopo, para um caso de uso local, concreto e validado institucionalmente: um canal digital comunitario de seguranca urbana para o bairro da Gavea. O fio condutor que sobreviveu a todas as fases foi um principio de design - soberania de dados: toda a inferencia de IA roda localmente, heranca direta dos principios CARE/OCAP que orientavam o tratamento de dados de comunidades no atlas original.

Do ponto de vista academico, o projeto tem dois objetos de estudo sobrepostos. O primeiro e o produto: um sistema que aplica pipelines de LLM e tecnicas de embeddings a relatos de cidadaos. O segundo e o proprio processo de desenvolvimento: o sistema foi construido inteiramente sob um harness de engenharia assistida por IA (SEJA, sobre Claude Code), deixando um rastro auditavel de cerca de 75 artefatos numerados que documentam cada decisao - um corpus de pesquisa em si para a disciplina de AI Systems Design.

## Timeline: a genealogia do escopo

A narrativa abaixo descreve como o enquadramento do projeto evoluiu. O movimento central e um "zoom in": do atlas de escala continental para um bairro especifico, uma vertical tematica e dois personas concretos.

**Fase 0 - Origem: Atlas da Amazonia (abr/2026).** O conceito inicial era um Atlas Digital Georreferenciado da Amazonia assistido por IA: um atlas interativo de dados multimodais georreferenciados (PRODES/DETER/IMAZON/FUNAI via datazoom.amazonia; Nova Cartografia Social), com chat dotado de ferramentas de navegacao e soberania de dados. Ja existia uma ferramenta funcional - o kb-qa, um RAG local (ChromaDB + sentence-transformers + servidor MCP) integrado e testado no Claude. O diagnostico arquitetural foi honesto: o kb-qa cobria apenas 20-30% do necessario. Definiu-se entao uma arquitetura em camadas (RAG textual + engine geoespacial DuckDB spatial + ferramenta render_map), abstracao de LLM (local Ollama OU nuvem) e um servico autocontido dual MCP + REST.

**Fase 1 - Casos de uso e participacao cidada (mai/2026).** O foco migrou para um espaco virtual de participacao cidada. Sintetizaram-se plataformas de referencia (Decidim, Pol.is, Talk to the City, Consul, vTaiwan, UDT) e pesquisaram-se datasets abertos. Convergiu-se para Talk to the City (T3C), com deployment local e extensao para o caso GaveaLab; uma PoC TRL3 rodou ponta a ponta com Docker e Ollama local, usando um CSV de teste baseado no diagnostico real do GaveaLab (2023).

**Fase 2 - GaveaLab PoC: analise textual (jun/2026).** Construiu-se um PoC em Streamlit (SQLite via GaveaLabWorkspace + Ollama) com o pipeline de analise de relatos: upload de CSV, temas automaticos, claims, categorizacao manual e cruxes (deteccao de divergencias via embeddings). Em seguida vieram a visualizacao UMAP e a navegacao multipagina.

**Fase 3 - fala-gavea: relatos + feedback + clusters (jun/2026).** A plataforma ganhou o nome fala-gavea: backend de likes/label/feedback, dataset semente, rastreabilidade de interacoes, visualizacao de clusters UMAP com rotulos gerados por IA.

**Fase 4 - Zoom in: do Atlas para a Gavea (jun/2026).** A decisao-chave de escopo. Em vez de um atlas global, um bairro concreto (Gavea), uma vertical tematica (seguranca urbana) e dois personas: o cidadao, que reporta um problema (foto, localizacao, texto), e o delegado, que explora um dashboard georreferenciado e cura as demandas. O mapa passou a usar Google Maps/Leaflet (baixo custo). Houve validacao institucional - documento da stakeholder Fabiene atestando a relevancia de um caso de uso real. O insight central foi metodologico: o pipeline de clustering ja construido E o motor do caso de uso do delegado; a integracao com o mapa e uma nova camada de visualizacao, nao um novo projeto.

**Fase 5 - Busca inteligente + canal comunitario (jun/2026).** Introduziu-se um chat em linguagem natural "intent-to-filter" (o usuario descreve a busca em NL e a IA a traduz para filtros da API). Detectou-se uma lacuna: as correcoes do delegado (o par categoria-sugerida vs. categoria-confirmada) nao eram capturadas como sinal de treino. Surgiu entao o roadmap do "Canal Digital Comunitario para Seguranca Urbana" - um "Waze comunitario" que fecha o feedback loop com auditoria append-only, few-shot injection no prompt (em vez de fine-tuning), clustering reaproveitando embeddings ja no ChromaDB, urgencia e encaminhamento institucional.

**Fase 6 - Reescrita em clean architecture (jun/2026, estado atual).** O fala-gavea foi reescrito como scaffold de clean architecture (FastAPI + SQLAlchemy + SQLite + Pydantic v2 + pytest) e passou a ser um git submodule. O scaffold foi validado (6/6 PASS) e a pesquisa mais recente retorna explicitamente a camada geoespacial do atlas original, agora no nivel local do bairro.

| Fase | Periodo | Enquadramento | Marco |
|------|---------|---------------|-------|
| 0 | abr/2026 | Atlas da Amazonia (global) | kb-qa RAG + MCP; arquitetura em camadas |
| 1 | mai/2026 | Participacao cidada | Sintese de plataformas; PoC T3C local |
| 2 | jun/2026 | GaveaLab PoC | Pipeline textual em Streamlit (temas, claims, cruxes) |
| 3 | jun/2026 | fala-gavea | Feedback, dataset semente, clusters UMAP |
| 4 | 15/jun/2026 | Zoom in para a Gavea | Seguranca urbana; personas cidadao + delegado; validacao institucional |
| 5 | jun/2026 | Canal comunitario | Busca NL intent-to-filter; feedback loop few-shot |
| 6 | jun/2026 (atual) | Clean architecture | FastAPI + submodule; retorno a camada geoespacial |

## O que foi implementado (tecnologia)

O estado atual do produto - fala-gavea - e um backend FastAPI em clean architecture. A entidade central, SecurityReport, carrega category, ai_suggested_category, tags, status, urgency e routed_to. Os endpoints expoem: POST de auto-categorizacao; PATCH de category (confirma ou corrige - o ato de curadoria); filtros temporal (since/until), espacial (bbox) e por tag; GET /search (busca semantica via ChromaDB); e o chat NL intent-to-filter. O frontend e um mapa Leaflet com Alpine.js e popup de curadoria. A IA local e servida por um OllamaClient com um CATEGORIZE_PROMPT de 9 categorias, sobre um dataset semente de cerca de 250 relatos ficticios da Gavea.

A pilha tecnologica consolidada ao longo das fases:

- **Linguagem e gestao:** Python 3.13 + uv.
- **Web e persistencia:** Streamlit (PoCs iniciais) evoluindo para FastAPI clean architecture (atual); SQLite via SQLAlchemy.
- **Vetorial e embeddings:** ChromaDB; sentence-transformers (multilingual-e5-large, nomic-embed-text).
- **LLM local:** Ollama via endpoint OpenAI-compativel, com modelos qwen2.5/qwen3 locais.
- **Visualizacao:** Leaflet + Alpine.js (mapa); UMAP + HDBSCAN + Plotly (clusters).
- **Qualidade:** pytest, ruff, pyright.

O principio transversal e que toda inferencia roda local - soberania de dados.

## Uso de IA: dois eixos

Para a avaliacao academica importa separar a IA enquanto funcao do produto da IA enquanto metodo de construcao.

**1. IA no produto.** Inferencia local via Ollama; categorizacao automatica de relatos; clustering semantico (embeddings + UMAP + HDBSCAN); busca semantica (ChromaDB); chat NL traduzido para filtros de API; e um feedback loop few-shot com curadoria humana no comando. Este ultimo ponto e o mais relevante teoricamente: o delegado confirma ou corrige a categoria sugerida pela IA, e essa correcao alimenta o prompt por injecao few-shot (em vez de fine-tuning), configurando um padrao human-in-the-loop com aprendizado barato e auditavel.

**2. IA no processo de desenvolvimento.** O projeto inteiro foi desenvolvido com o harness SEJA sobre Claude Code, seguindo o ciclo /research -> /plan -> /implement -> /check -> /document ou /communicate -> /reflect. Ha rastro auditavel: cerca de 75 artefatos numerados (advisory logs, planos, roadmaps, reflexoes, QA logs, telemetria) e um historico de commits que documenta cada decisao de design. Esse corpus e, em si, um objeto de estudo de engenharia assistida por IA: permite reconstruir nao apenas o que foi construido, mas como e por que cada inflexao de escopo ocorreu - o tipo de material que a disciplina de AI Systems Design se propoe a examinar.

## Evidencias empiricas que ancoram o escopo

A decisao de "zoom in" do atlas para a Gavea nao foi arbitraria. A equipe tinha acesso a dois corpos de evidencia concretos que informaram cada inflexao de escopo.

**Diagnostico GaveaLab 2023 (FAPERJ 20/2022).** O projeto se apoiou em uma pesquisa de campo pre-existente, realizada pela equipe do Laboratorio de Gestao em Design (LGD/PUC-Rio) entre junho e novembro de 2023, com 380 entrevistados (Gavea-"asfalto", Rocinha, Parque da Cidade). O diagnostico identificou SEGURANCA como o principal tema alavancador do territorio: 20% das citacoes espontaneas dos moradores do "asfalto" e 9% das favelas apontam seguranca como a maior dor. A pesquisa revelou tambem a percepcao radicalmente diferente entre os dois grupos - para os moradores do "asfalto", seguranca significa policiamento; para os moradores das favelas, seguranca e sinonimo de garantia de direitos fundamentais e ausencia de violencia policial. Esse dado empirico fundou a escolha da vertical de seguranca urbana e a necessidade de uma ferramenta que capture a multiplicidade de vozes sobre um mesmo territorio. A pesquisadora Fabienne Torres Schiavo (Doutora em Design, CAPES, coordenadora do diagnostico) e a stakeholder que atestou a relevancia do caso de uso real para a entrega academica.

**Casos de uso co-construidos com a equipe (jun/2026).** Em paralelo ao desenvolvimento tecnico, a equipe documentou casos de uso especificos para a Plataforma Fala Gavea. O documento resultante (elaborado para INF2921/CIS2114) registra dois cenarios centrais:

- *Caso de Uso 01: Cidadao registra e acompanha uma demanda local.* Um morador da Rocinha percebe que ha tres semanas a iluminacao publica da entrada da comunidade esta apagada. Ele nao sabe a qual orgao recorrer e experiencias anteriores com canais oficiais foram frustrantes. Via app, o morador descreve o problema por texto, voz ou foto; a IA categoriza automaticamente, infere a localizacao e sugere a prioridade com base em relatos similares. Outros moradores podem confirmar a demanda com um clique.

- *Caso de Uso 02: Gestor publico ou investidor consulta para tomada de decisao.* Um gestor publico quer conhecer os problemas e necessidades do territorio para formular politicas embasadas nas demandas reais dos cidadaos - acessando uma visao estruturada e segmentada das reivindicacoes, com conformidade com LGPD e alinhamento ao PL 2338 (Marco Regulatorio da IA no Brasil).

Esses dois casos de uso sao exatamente os que o produto atual implementa parcialmente: o cidadao que registra um SecurityReport com foto e localizacao, e o delegado (proxy do gestor publico) que explora o dashboard georreferenciado, cura as categorias sugeridas pela IA e encaminha as demandas.

**Reunioes de stakeholders como fonte de design.** As transcricoes das reunioes de equipe revelam o processo de sintese das ideias em tempo real. Em uma das sessoes, Natali Garcia descreveu com precisao o pipeline que seria construido: "a gente clusteriza, analisa com IA, descarta o que e lixo, faz uma classificacao ligada a perfis e mostra um dashboard". Andrey Rodrigues, em outra sessao, formulou o papel da IA no projeto: "nao como um curador principal, mas um auxiliador na curadoria". Essa formulacao - IA como auxiliar da curadoria humana, nao como substituta - e exatamente o padrao human-in-the-loop implementado no feedback loop do delegado.

## Fechamento: do Atlas global a Gavea local

O merito academico do projeto nao esta em ter chegado ao escopo inicial, e sim em ter feito o caminho inverso de forma deliberada e documentada. A trajetoria Atlas global -> Gavea local e um estudo de caso de reducao de escopo guiada por viabilidade, validacao institucional e reaproveitamento de capacidades ja construidas - o reconhecimento de que o pipeline de clustering do delegado ja existia e so precisava de uma nova camada de visualizacao. Os dois invariantes que sobreviveram a todas as fases - a camada geoespacial e a soberania de dados local - sao exatamente os que conectam o produto final a sua origem amazonica. O resultado e um artefato pequeno, executavel e validado, sustentado por um registro completo das decisoes de design que o produziram.
