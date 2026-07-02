# Sistemas de IA para Participação Cidadã: GaveaLab e Fala-Gávea

**Disciplina:** INF2921/CIS2114 — AI Systems Design 2026.1  
**Instituição:** PUC-Rio  
**Grupo C:** Andrey, Mauro, Julia, Herbert, Natali  
**Data:** Julho de 2026

---

## Resumo

> **[PREENCHER — Coletivo: proposta de Andrey, revisão de todos]**
> *1 parágrafo (5-8 linhas) descrevendo o que o grupo fez, o problema que resolveu, as tecnologias centrais e o resultado entregue. Escrever ao final, depois que todas as seções individuais estiverem preenchidas.*
>
> *Rascunho sugerido:* Este trabalho descreve o processo de elaboração de dois sistemas de IA para participação cidadã desenvolvidos pelo Grupo C no âmbito da disciplina INF2921/CIS2114 (PUC-Rio, 2026.1): o **GaveaLab**, ferramenta de análise qualitativa de relatos de cidadãos inspirada no Talk to the City, e o **Fala-Gávea**, plataforma de registro e encaminhamento de demandas urbanas de segurança. O projeto evoluiu de uma prova de conceito TRL 3 do Talk to the City rodando localmente com Ollama, passando pelo GaveaLab como produto Streamlit, até o Fala-Gávea como aplicação FastAPI + React com busca semântica, filtros por linguagem natural e workflows de encaminhamento institucional. Os sistemas operam inteiramente em infraestrutura local, garantindo a soberania dos dados dos cidadãos. [completar com resultados e lições aprendidas]

---

## 1. Introdução

### 1.1 Contexto e Motivação

A análise qualitativa de relatos de cidadãos — respostas abertas a consultas públicas, comentários em audiências, registros de problemas urbanos — é uma tarefa intensiva que normalmente exige codificação manual por pesquisadores ou analistas. Ferramentas como o [Talk to the City](https://github.com/AIObjectives/tttc-light-js) (AIObjectives / vTaiwan) demonstram que pipelines LLM podem automatizar a descoberta de temas, extração de afirmações-chave e identificação de divergências genuínas em corpora de opiniões. O precedente de Taiwan MODA (AI Alignment Assembly, 2023, 400+ participantes) mostrou que esta abordagem pode influenciar políticas públicas reais.

O GaveaLab (parceiro da disciplina) coleta relatos de cidadãos sobre problemas e necessidades da Gávea. O Grupo C identificou dois problemas concretos: (1) não existe ferramenta leve para analisar esses relatos localmente sem enviar dados para serviços de nuvem; (2) não existe canal digital para que o cidadão registre um problema no mapa, acompanhe seu encaminhamento e interaja com agentes públicos. Este trabalho descreve como o grupo abordou esses dois problemas ao longo de 8 semanas.

### 1.2 O que o grupo já conhecia

> **[PREENCHER — Andrey]**
> *Perguntas orientadoras:*
> - Qual era a sua experiência prévia com LLMs, RAG, embeddings, FastAPI, React antes da disciplina?
> - Você já conhecia o Talk to the City? O Pol.is? O vTaiwan?
> - Qual era o seu background com dados geoespaciais e Leaflet?
> *(2–3 parágrafos)*

---

> **[PREENCHER — Mauro]**
> *Perguntas orientadoras:*
> - Qual era a sua experiência prévia com sistemas de IA e desenvolvimento de software?
> - O que você já sabia sobre o problema de análise de feedback cidadão?
> - Qual ferramenta ou conceito da disciplina te surpreendeu mais?
> *(2–3 parágrafos)*

---

> **[PREENCHER — Julia]**
> *Perguntas orientadoras:*
> - Qual era a sua experiência com Python, TypeScript, bancos de dados antes da disciplina?
> - Você já tinha trabalhado com sistemas de participação cidadã ou civic tech?
> - O que você já sabia sobre embeddings e busca semântica?
> *(2–3 parágrafos)*

---

> **[PREENCHER — Herbert]**
> *Perguntas orientadoras:*
> - Qual era o seu background técnico e de domínio ao entrar na disciplina?
> - O que motivou seu interesse no tema de IA para participação cidadã?
> - Que conceitos ou ferramentas você trouxe de experiências anteriores?
> *(2–3 parágrafos)*

---

> **[PREENCHER — Natali]**
> *Perguntas orientadoras:*
> - Qual era a sua experiência com IA aplicada antes da disciplina?
> - Você já tinha contato com o GaveaLab ou com problemas de dados urbanos?
> - Que conhecimentos prévios foram mais úteis durante o projeto?
> *(2–3 parágrafos)*

---

## 2. Processo de Elaboração

### 2.1 Formação da equipe e primeiras discussões

O grupo se formou em 13 de abril de 2026, quando Andrey criou um grupo de WhatsApp e convidou os colegas identificados na plataforma EAD da disciplina. A equipe ficou com cinco membros ativos: Andrey, Natali, Julia, Mauro e Herbert. A comunicação principal ocorreu pelo WhatsApp, com reuniões presenciais antes das aulas de quinta-feira e encontros virtuais para decisões técnicas.

O primeiro encontro presencial (16 de abril) serviu para apresentações e brainstorming de temas. Em 23 de abril, o grupo registrou as primeiras ideias de produto em reunião documentada: segurança pública, mapeamento de espaços urbanos, acesso controlado à informação multimodal. A ideia inicial mais ambiciosa era um "atlas digital e iterativo assistido por IA" — algo como um repositório georreferenciado de informações urbanas curado por comunidades, inicialmente pensado para a escala da Amazônia.

> **[PREENCHER — Todos: adicionar perspectivas sobre a dinâmica inicial da equipe]**
> *Perguntas orientadoras:*
> - Como foi a primeira reunião? O que foi mais difícil de alinhar?
> - Como vocês definiram papéis e responsabilidades?
> - Houve divergências sobre o tema? Como foram resolvidas?
> *(1–2 parágrafos coletivos)*

### 2.2 Definição do tema e escopo — o "zoom in" progressivo

A trajetória do escopo do projeto foi de um progressivo afunilamento geográfico e temático. A sequência ficou conhecida internamente como o "zoom in": Amazônia → Rio de Janeiro → Gávea → segurança pública na Gávea.

Em 22 de maio, o grupo pesquisou ferramentas de participação cidadã existentes (Decidim, Pol.is, Talk to the City, CitizenLab, Consul, vTaiwan) e identificou o Talk to the City como a arquitetura mais adequada para o objetivo: pipeline LLM para descoberta de temas, extração de afirmações e visualização de divergências. Em paralelo, o grupo construiu o **kb-qa** — uma ferramenta RAG genérica para indexar os materiais da própria disciplina no ChromaDB e consultá-los via MCP no Claude Code. Esta ferramenta resolveu um problema imediato do grupo e estabeleceu a base técnica (sentence-transformers, ChromaDB, FastMCP) que seria reutilizada nos produtos seguintes.

O zoom final aconteceu em reflexão registrada (reflection-000052, 15 de junho): a equipe decidiu focar na Gávea, com o GaveaLab como parceiro real, trabalhando sobre o problema concreto de análise de relatos cidadãos do bairro.

> **[PREENCHER — Andrey / Natali: contexto do GaveaLab como stakeholder]**
> *Perguntas orientadoras:*
> - Como surgiu a conexão com o GaveaLab?
> - Qual foi o papel do GaveaLab nas decisões de produto?
> - O que os stakeholders do GaveaLab esperavam do projeto?
> *(1–2 parágrafos)*

### 2.3 Pesquisas iniciais: ferramentas e perguntas

As primeiras pesquisas técnicas foram conduzidas principalmente por Andrey usando o Claude Code com o harness SEJA (Skill-Enabled Journal Architecture), um sistema de gestão de sessões de IA que registra automaticamente perguntas, decisões e planos. Isso criou um log auditável de todo o processo de pesquisa.

**Ferramentas utilizadas:**
- Claude Code (Anthropic) com MCP para busca de código e documentação
- kb-qa (produto do próprio grupo) para consultar papers e materiais da disciplina
- GitHub para explorar os repositórios do Talk to the City e de projetos relacionados
- Docker para testar a PoC do T3C localmente

**Exemplos de perguntas de pesquisa que geraram advisory logs:**
- *"Como rodar o Talk to the City completamente local, sem dependências de nuvem?"* (advisory-000004)
- *"Quais são os principais casos de uso para uma plataforma de participação cidadã na Gávea?"* (advisory-000003)
- *"Como estruturar um plugin de ingestão multi-formato para o T3C usando LLM local?"* (advisory-000005)
- *"Qual o melhor pipeline para clustering de sentenças — cluster em alta dimensão primeiro ou reduzir primeiro?"* (research-000023)
- *"Como fazer deploy do Fala-Gávea via Docker no Railway?"* (research-000091)

> **[PREENCHER — Mauro / Julia / Herbert / Natali: como cada um fez suas próprias pesquisas]**
> *Perguntas orientadoras:*
> - Que ferramentas você usou para pesquisar sobre o tema do projeto?
> - Que perguntas você fez (ao Claude, ao Google, à literatura)?
> - Que fontes foram mais úteis? Papers, documentação, blogs, repositórios?
> *(1 parágrafo por membro)*

### 2.4 Como os resultados iniciais foram refinados

A evolução do projeto passou por três grandes ciclos de refinamento, cada um motivado por um aprendizado concreto:

**Ciclo 1: Do T3C para Python puro (maio → junho)**
O grupo implementou com sucesso uma PoC TRL 3 do Talk to the City rodando localmente: Docker Compose com três serviços (Ollama + servidor Express + cliente Next.js), incluindo patches para o pyserver Python interno do T3C e stubs de autenticação. A PoC funcionou — o pipeline gerou clusters e a visualização apareceu no browser sem internet. Mas o ecossistema JavaScript com Firebase/GCS/PubSub mockados era complexo de manter e evoluir. A pergunta que emergiu: *"e se reimplementássemos o pipeline em Python puro, com Streamlit, usando Ollama local?"* Em 1º de junho, um único dia de trabalho produziu o roadmap-000007 e o GaveaLab nasceu como produto Python.

**Ciclo 2: Do GaveaLab para Fala-Gávea (junho)**
Em 11 de junho, o research-000023 nomeou o que o grupo estava construindo: uma "arquitetura de dois anéis". O GaveaLab era o anel interno — ferramenta de análise de corpus existente. O Fala-Gávea seria o anel externo — canal de coleta de novos relatos em tempo real. A primeira versão do Fala-Gávea usou Streamlit, mas rapidamente o grupo percebeu que um SPA React com FastAPI seria mais adequado para o fluxo cidadão → agente público.

**Ciclo 3: Do HTML estático para React SPA (junho)**
A versão HTML estática do frontend do Fala-Gávea foi substituída por um SPA React 18 + Vite + TypeScript + Tailwind (plan-000082, roadmap-000056). A decisão foi motivada pela necessidade de estado dinâmico (mapa Leaflet interativo, filtros em tempo real, chat NL, cesta de relatos).

> **[PREENCHER — Todos: adicionar exemplos pessoais de refinamento]**
> *Perguntas orientadoras:*
> - Em que momento você percebeu que a abordagem inicial precisava mudar?
> - Como foi o processo de tomar uma decisão de pivotar?
> - Que evidência técnica ou de usuário motivou a mudança?
> *(1–2 parágrafos por membro)*

### 2.5 Surpresas e tentativas que não deram certo

> **[PREENCHER — Andrey]**
> *Perguntas orientadoras:*
> - Que aspecto técnico te surpreendeu mais (positivamente ou negativamente)?
> - Houve alguma abordagem que você tentou e abandonou? Por quê?
> - O que você teria feito diferente no início se soubesse o que sabe agora?
> *(2–3 parágrafos)*

---

> **[PREENCHER — Mauro]**
> *Mesmas perguntas orientadoras acima.*
> *(2–3 parágrafos)*

---

> **[PREENCHER — Julia]**
> *Mesmas perguntas orientadoras acima.*
> *(2–3 parágrafos)*

---

> **[PREENCHER — Herbert]**
> *Mesmas perguntas orientadoras acima.*
> *(2–3 parágrafos)*

---

> **[PREENCHER — Natali]**
> *Mesmas perguntas orientadoras acima.*
> *(2–3 parágrafos)*

### 2.6 Organização da comunicação da equipe

A equipe utilizou três canais complementares:

| Canal | Uso | Frequência |
|-------|-----|------------|
| **WhatsApp** | Coordenação rápida, combinação de horários, avisos | Diária durante o desenvolvimento |
| **GitHub** (git.tecgraf.puc-rio.br) | Controle de versão, revisão de código, histórico de decisões | A cada commit/push |
| **Claude Code + harness SEJA** | Registro automático de pesquisas, planos e implementações; log auditável de decisões | A cada sessão de trabalho |

O harness SEJA funcionou como um terceiro tipo de documentação: além do código (git) e das conversas (WhatsApp), cada sessão de trabalho gerou um log estruturado de perguntas, respostas, planos e resultados. Isso permitiu ao grupo retomar o trabalho entre sessões sem perder contexto.

> **[PREENCHER — Todos: adicionar perspectivas sobre a comunicação]**
> *Perguntas orientadoras:*
> - Como foi trabalhar remotamente vs. presencialmente?
> - Houve dificuldades de sincronização entre membros? Como foram resolvidas?
> - O que funcionou bem na organização do grupo?
> *(1–2 parágrafos coletivos)*

---

## 3. Arquitetura e Decisões Técnicas

### 3.1 Visão Geral da Arquitetura

O projeto entregou três artefatos interrelacionados:

```
┌─────────────────────────────────────────────────────────────┐
│                    INFRAESTRUTURA LOCAL                      │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FALA-GÁVEA (produto principal)                      │  │
│  │                                                      │  │
│  │  [React SPA] ←→ [FastAPI] ←→ [SQLite + SQLAlchemy]  │  │
│  │       ↕              ↕                               │  │
│  │  [Leaflet Map]  [ChromaDB] ←→ [sentence-transformers]│  │
│  │                     ↕                               │  │
│  │               [Ollama (qwen3:8b)]                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌───────────────────────┐  ┌──────────────────────────┐   │
│  │  GAVEALAB (suporte)   │  │  KB-QA (ferramenta RAG)  │   │
│  │                       │  │                          │   │
│  │  [Streamlit] ←→       │  │  [CLI click] + [FastMCP] │   │
│  │  [SQLite]  ←→ [Ollama]│  │  ←→ [ChromaDB]           │   │
│  │  [UMAP + Plotly]      │  │  ←→ [sentence-transformers│   │
│  └───────────────────────┘  └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Princípio arquitetural central:** nenhum dado do cidadão sai da máquina do analista. Todo processamento LLM ocorre via Ollama local. O banco de dados é SQLite local. O deploy para Railway (Fala-Gávea) usa containers Docker sem serviços gerenciados de nuvem para dados.

> **[PREENCHER — Arquitetura detalhada — aguarda `/explain architecture` (plan-000075 Step 4)]**
> *Esta seção será complementada com diagrama detalhado de componentes gerado pelo skill `/explain architecture`.*

### 3.2 Principais Decisões Técnicas

As decisões arquiteturais foram documentadas formalmente como entradas D-NNN nos arquivos de design intent do projeto. As cinco decisões centrais do GaveaLab + kb-qa:

**D-001: ChromaDB como vector store**  
*Contexto:* Precisávamos de um vector store local sem servidor. Alternativas: Qdrant (local ou remoto), FAISS (biblioteca apenas), pgvector (requer PostgreSQL).  
*Decisão:* ChromaDB com `PersistentClient`. Roda embutido, persiste em diretório local, zero ops overhead.  
*Consequências:* Setup rápido, não adequado para multi-host ou alta concorrência. API estável para nosso caso de uso.

**D-002: MCP (FastMCP) para exposição do kb-qa**  
*Contexto:* O caso de uso principal era injetar resultados da base de conhecimento em sessões Claude Code. Opções: MCP tool (controlado pelo modelo) ou REST API (controlado pelo usuário).  
*Decisão:* Expor `query_knowledge` como MCP tool via FastMCP. CLI (`kb-qa ask`) permanece disponível.  
*Consequências:* Funciona nativamente com Claude Code via settings.json. Composável com futuros consumidores MCP.

**D-003: nomic-ai/nomic-embed-text-v1 como modelo de embeddings**  
*Contexto:* Precisávamos de embeddings multilíngues (pt-BR + en-US), qualidade semântica alta, licença permissiva, tamanho razoável.  
*Decisão:* `nomic-ai/nomic-embed-text-v1` via sentence-transformers. MIT-licensed, multilíngue.  
*Consequências:* Primeiro download ~274MB. Atualizações de modelo exigem reingestão completa.

**D-004: Streamlit + SQLite para o GaveaLab**  
*Contexto:* Precisávamos de UI web leve para ferramenta local single-user. Alternativas: FastAPI + React (overhead alto para PoC), Gradio (multi-page limitado), Streamlit (Python nativo, multi-page, session state).  
*Decisão:* Streamlit para UI, SQLite (via `sqlite3` embutido) para persistência. Sem ORM — acesso direto via `GaveaLabWorkspace`.  
*Consequências:* Zero overhead de infraestrutura. SQLite limita acesso concorrente, aceitável para single-user.

**D-005: Ollama como backend LLM para o GaveaLab**  
*Contexto:* O pipeline LLM (tópicos, claims, cruxes) precisava de servidor de inferência local. Alternativas: llama.cpp (nível mais baixo), API de nuvem (viola princípio de privacidade).  
*Decisão:* Ollama em `http://localhost:11434/v1` com endpoint compatível com OpenAI. Modelo padrão: `qwen3:8b`.  
*Consequências:* Requer Ollama rodando como processo separado. Todas as chamadas LLM passam por `gavealab_poc/llm.py` (OllamaClient).

**Decisões adicionais do Fala-Gávea (D-A a D-G):**  
O Fala-Gávea acumulou decisões próprias documentadas no seu harness: FastAPI + SQLAlchemy + SQLite (vs. Django/Flask); JWT Bearer com roles citizen/agent/admin (vs. sessões); React 18 + Vite + TypeScript (vs. HTML estático); clean architecture em camadas domain/application/infrastructure/presentation; BERTopic para modelagem de tópicos; Railway para deploy via Docker.

### 3.3 Stack e Ferramentas

| Produto | Linguagem | Framework | Banco | Embeddings | LLM | Deploy |
|---------|-----------|-----------|-------|-----------|-----|--------|
| **kb-qa** | Python 3.13 | click + FastMCP | ChromaDB | nomic-embed-text-v1 | N/A (RAG puro) | Local |
| **GaveaLab** | Python 3.13 | Streamlit | SQLite | nomic-embed-text-v1 (UMAP) | Ollama qwen3:8b | Local |
| **Fala-Gávea** | Python 3.13 + TypeScript | FastAPI + React 18 + Vite | SQLite + ChromaDB | nomic-embed-text-v1 | Ollama qwen3:8b | Railway (Docker) |

**Ferramentas de suporte ao desenvolvimento:**
- **uv** (Python package manager — `pyproject.toml` + `uv.lock`)
- **Claude Code + harness SEJA** (sessões de IA com log estruturado de planos e decisões)
- **pytest** (testes)
- **ruff** (linting) + **pyright** (type checking)
- **Docker + Docker Compose** (containerização para Railway e para a PoC do T3C)

---

## 4. Requisitos para Sistemas Confiáveis, Seguros e Socialmente Responsáveis

### 4.1 Desafios identificados

O projeto enfrentou desafios em quatro dimensões:

**Privacidade e soberania dos dados**
Relatos de cidadãos podem conter informações pessoais sensíveis (localização, identidade, problemas de saúde, situação econômica). Qualquer arquitetura que envie esses dados para APIs de nuvem (OpenAI, Anthropic, Google) cria um risco de exposição. A disciplina de sistemas de IA socialmente responsáveis exige que o analista saiba exatamente onde os dados do cidadão estão e quem pode acessá-los.

**Viés algorítmico na análise de opiniões**
Modelos LLM têm vieses treinados sobre corpora predominantemente em inglês. Quando aplicados a relatos em português do Brasil sobre problemas urbanos da Gávea, podem: (1) classificar incorretamente o tom (ironia, gíria, código-misto); (2) superrepresentar temas com vocabulário mais formal; (3) criar cruxes (pontos de divergência) que são artefatos do modelo, não divergências reais entre cidadãos.

**Transparência e auditabilidade**
Em um sistema de participação cidadã, o analista precisa confiar nos outputs do LLM antes de apresentá-los a gestores públicos ou em audiências. Uma ferramenta que produz "black box outputs" — tópicos, claims, divergências — sem permitir inspeção do raciocínio viola princípios de transparência.

**Acessibilidade e exclusão digital**
Uma plataforma de registro de demandas urbanas (Fala-Gávea) que só funciona via smartphone com conexão de qualidade exclui justamente os cidadãos mais vulneráveis — aqueles com menores índices de letramento digital, dispositivos mais antigos ou acesso à internet instável.

### 4.2 Como os desafios foram endereçados

| Desafio | Princípio do projeto | Como implementado |
|---------|---------------------|-------------------|
| Privacidade dos dados | C1, C2 (Constituição do projeto) | Ollama local; SQLite na máquina do analista; ChromaDB gitignored; sem upload para APIs externas |
| Viés algorítmico | S4 (GaveaLab write isolation) | Todos os outputs LLM são exibidos na UI para revisão humana antes de serem tratados como resultado; botão "Re-run" para regenerar qualquer etapa |
| Transparência | T1 (OllamaClient centralizado) | Todos os LLM calls passam por `llm.py`; modelo e URL são configuráveis via env vars; prompts são constantes de módulo visíveis no código |
| Auditabilidade | T2 (GaveaLabWorkspace) | Sessões persistem no SQLite; analista pode revisar e comparar resultados anteriores; harness SEJA cria log de todas as decisões de desenvolvimento |
| Acessibilidade | — | **Não endereçado adequadamente** (ver §5.2 Limitações) |

> **[PREENCHER — Todos: perspectivas sobre os desafios de sistemas responsáveis]**
> *Perguntas orientadoras:*
> - Qual desses desafios você considera mais crítico para este tipo de sistema?
> - Houve um momento no projeto em que você percebeu que uma decisão técnica tinha implicações éticas?
> - Como a abordagem "local-first" afeta a escalabilidade e o alcance do sistema?

### 4.3 Perspectiva de cada membro sobre sistemas confiáveis, seguros e socialmente responsáveis

> **[PREENCHER — Andrey]**
> *Perguntas orientadoras:*
> - Em que medida a escolha de rodar tudo localmente (Ollama, SQLite, ChromaDB) é suficiente para garantir a privacidade dos dados cidadãos?
> - Quais são os limites éticos do uso de LLM para "interpretar" opiniões de cidadãos?
> - O que seria necessário para este sistema ser usado em um processo real de consulta pública?
> *(3–4 parágrafos)*

---

> **[PREENCHER — Mauro]**
> *Perguntas orientadoras:*
> - Como você avalia o risco de viés algorítmico nos outputs do GaveaLab (tópicos, claims, cruxes)?
> - Que salvaguardas adicionais você adicionaria ao sistema se fosse implantá-lo em produção?
> - O que significa "responsabilidade social" para um sistema de IA que analisa dados de cidadãos vulneráveis?
> *(3–4 parágrafos)*

---

> **[PREENCHER — Julia]**
> *Perguntas orientadoras:*
> - Como o design da interface do Fala-Gávea pode incluir ou excluir diferentes perfis de cidadãos?
> - Que riscos de segurança você identificou na implementação de JWT + roles no Fala-Gávea?
> - O que a literatura de design de sistemas de IA responsáveis (ex: Weisz et al., 2024) sugere que ainda falta no nosso sistema?
> *(3–4 parágrafos)*

---

> **[PREENCHER — Herbert]**
> *Perguntas orientadoras:*
> - Como garantir que o sistema de encaminhamento (Fala-Gávea) não se torne um "buraco negro" onde as demandas dos cidadãos somem sem resposta?
> - Qual é a responsabilidade do desenvolvedor quando um sistema de IA classifica incorretamente um relato de emergência?
> - Como a transparência algorítmica se aplica a modelos rodando localmente (sem API pública auditável)?
> *(3–4 parágrafos)*

---

> **[PREENCHER — Natali]**
> *Perguntas orientadoras:*
> - Qual é o impacto do viés de representação nos dados de treinamento dos modelos LLM quando usados para analisar vozes de comunidades periféricas?
> - Como o conceito de "crux" (ponto de divergência genuína) pode ser usado de forma responsável — ou irresponsável — em processos de consulta pública?
> - O que você aprendeu sobre os limites éticos da IA generativa neste projeto que não estava claro no início?
> *(3–4 parágrafos)*

---

## 5. Resultados e Estado Atual

### 5.1 Funcionalidades implementadas

**kb-qa (ferramenta RAG de suporte)**
- Ingestão incremental de arquivos `.md` e `.pdf` via ChromaDB (content-addressable, sem duplicatas)
- CLI `kb-qa ingest / status / ask` com barra de progresso
- MCP tool `query_knowledge` via FastMCP — consultado automaticamente pelo Claude Code em sessões da equipe
- Base de conhecimento indexada: materiais da disciplina, papers, anotações de reuniões

**GaveaLab (análise de relatos cidadãos)**
- Upload de CSV com coluna `text` ou `comment` — cria sessão persistente no SQLite
- **Temas automáticos**: LLM gera árvore tópico/subtópico dos relatos (qwen3:8b via Ollama)
- **Categorização manual**: usuário define temas, LLM classifica cada relato
- **Claims**: extração de afirmações-chave por tópico com citação do relato original
- **Cruxes**: detecção de pontos de divergência genuína entre claims
- **Visualização UMAP**: scatter plot 2D interativo (Plotly) das claims embedadas; hover mostra texto e tópico; coloração por tópico
- Sessões persistem entre navegações; botão "Re-run" em cada etapa

**Fala-Gávea (plataforma de demandas urbanas)**

*Autenticação e roles:*
- JWT Bearer com três perfis: cidadão, agente público, admin
- Registro e login de usuários; roles separadas por endpoints

*Registro de relatos (cidadão):*
- Mapa Leaflet interativo — cidadão clica para geoposicionar o relato
- Campos: texto livre, tipo de demanda (ReportType), urgência
- Upload de evidências; visualização dos próprios relatos

*Exploração e gestão (agente público):*
- Mapa de todos os relatos com filtros de tempo, tipo e território
- **Busca semântica**: query em linguagem natural retorna relatos semanticamente similares (ChromaDB + nomic-embed)
- **Filtros por intenção NL**: chat que converte linguagem natural em filtros estruturados ("relatos de ontem sobre iluminação pública")
- **Relatos similares**: para cada relato aberto, exibe os top-K mais próximos no espaço semântico
- **BERTopic**: modelagem de tópicos emergentes sobre o corpus de relatos
- **Encaminhamentos (Forwardings)**: agente cria encaminhamento formal para órgão responsável; cidadão acompanha status
- **Cesta de relatos**: agente seleciona múltiplos relatos relacionados para encaminhamento conjunto
- Painel admin: seeds, gestão de usuários, categorias

*Deploy:*
- Containerizado (Dockerfile + docker-compose); deployed no Railway

### 5.2 Limitações e Trabalho Futuro

| Limitação | Tipo | Prioridade |
|-----------|------|-----------|
| Acessibilidade para cidadãos com baixo letramento digital | Produto | Alta |
| Ausência de loop de feedback humano → modelo (fine-tuning com correções do agente) | IA | Alta |
| Exportação de resultados GaveaLab para CSV/JSON | Produto | Média |
| Filtro de tópico/território na visualização UMAP | Produto | Média |
| Indicadores de progresso (spinner + tempo estimado) nas etapas LLM | UX | Média |
| Scores de similaridade visíveis no kb-qa ask | Produto | Baixa |
| Síntese LLM no kb-qa ask (--synthesize) | Produto | Baixa |

---

## 6. Conclusão

> **[PREENCHER — Coletivo: proposta de Andrey, revisão de todos]**
> *Perguntas orientadoras:*
> - O que este projeto demonstrou sobre a viabilidade de sistemas de IA para participação cidadã rodando localmente?
> - Quais foram as lições mais importantes — técnicas, de processo e de design responsável?
> - O que você faria diferente se recomeçasse?
> - Que perguntas abertas este projeto deixou que merecem investigação futura?
> *(4–6 parágrafos coletivos)*

---

## Referências

> *Nota: completar com formatação ABNT ou norma definida pelo grupo.*

WEISZ, Justin D. et al. **Design Principles for Generative AI Applications**. In: *Proceedings of the CHI Conference on Human Factors in Computing Systems (CHI 2024)*. ACM, 2024. Disponível em: `knowledge/library/Weisz et al. - 2024 - Design Principles for Generative AI Applications.pdf`

EARTO. **The TRL Scale as a Research & Innovation Policy Tool: EARTO Recommendations**. EARTO, 2014. Disponível em: `knowledge/library/EARTO - 2014 - The TRL Scale as a Research Innovation Policy Tool.pdf`

> **[PREENCHER — adicionar o paper 2203.05794v1 após verificar autoria e título]**  
> Disponível em: `knowledge/library/2203.05794v1.pdf`

AIOBJECTIVOS. **Talk to the City (tttc-light-js)**. GitHub, 2023. Disponível em: https://github.com/AIObjectives/tttc-light-js

VTAIWAN. **vTaiwan: Public Deliberation with AI**. 2023. Disponível em: https://vtaiwan.tw

IPLAN RIO. **Portal de Dados Abertos — Prefeitura do Rio de Janeiro**. Disponível em: https://www.iplan.rio/

DATAZOOM PUC-Rio. **DataZoom: Microdados do Brasil**. Disponível em: https://github.com/datazoompuc

> **[PREENCHER — Todos: adicionar referências de papers ou livros usados individualmente]**

---

## Apêndice A: Linha do Tempo do Projeto

*Extraída do relatório de evolução evolution-000076.*

| # | Data | Evento | Tipo | Impacto para o usuário |
|---|------|--------|------|----------------------|
| 1 | 2026-04-13 | Formação da equipe — grupo de WhatsApp criado | Processo | — |
| 2 | 2026-04-23 | Reunião de brainstorming: segurança pública, atlas digital Amazônia | Pesquisa | — |
| 3 | 2026-05-22 | advisory-000003: pesquisa de ferramentas de participação cidadã (Pol.is, T3C, vTaiwan) | Pesquisa | — |
| 4 | 2026-05-23 | advisory-000004: exploração do Talk to the City local com Ollama | Pesquisa técnica | — |
| 5 | 2026-05-24 | **TRL3 alcançado**: PoC T3C rodando end-to-end (commit e625876 — pyserver patchado, auth stubs, clusters no browser); kb-qa funcional | Implementação | Pipeline T3C local demonstrado; ferramenta RAG CLI disponível |
| 6 | 2026-06-01 | **PIVOT**: roadmap-000007 — reimplementar pipeline T3C em Python + Streamlit | Decisão estratégica | — |
| 7 | 2026-06-02 | GaveaLab v1: 5 páginas Streamlit (upload, tópicos, claims, categorização manual, cruxes) — executado em 1 dia | Implementação | Análise completa de relatos: tópicos → claims → cruxes |
| 8 | 2026-06-02 | Decisões D-004 (Streamlit + SQLite) e D-005 (Ollama) registradas | Arquitetura | — |
| 9 | 2026-06-09 | Visualização UMAP: scatter plot 2D de claim embeddings | Feature | Mapa visual de clusters de opiniões |
| 10 | 2026-06-11 | research-000023: arquitetura de dois anéis nomeada (GaveaLab + Fala-Gávea) | Pesquisa | — |
| 11 | 2026-06-11 | Fala-Gávea v1 (Streamlit): posts de cidadãos, likes, clusters UMAP | Implementação | Cidadão pode registrar relato e ver cluster de opiniões |
| 12 | 2026-06-15 | reflection-000052: "zoom in" Amazônia → Gávea formalizado | Reflexão | — |
| 13 | 2026-06-17 | **PIVOT**: roadmap-000071 — Fala-Gávea refundado em FastAPI + clean architecture + JWT | Decisão estratégica | — |
| 14 | 2026-06-18 | Fala-Gávea v2: domínio completo (User/Report/ReportType/Forwarding), auth JWT, React SPA 4 telas | Implementação | Cidadão registra no mapa; agente cria encaminhamento |
| 15 | 2026-06-19 | Wave semântica: ChromaDB + busca semântica + relatos similares + BERTopic + RAG chat | Feature | Agente explora relatos por similaridade e chat NL |
| 16 | 2026-06-20 | Workspace grid + filtros avançados + NL filter parser | Feature | Filtros por intenção em linguagem natural |
| 17 | 2026-06-22 | Cesta de relatos + jornadas de transparência cidadã | Feature | Cidadão acompanha status do encaminhamento |
| 18 | 2026-06-24 | Fala-Gávea deployed no Railway (Docker) | Deploy | Sistema acessível via URL pública |

---

## Apêndice B: Jornadas de Usuário

### JM-TB-001: Pesquisadora analisa relatos com GaveaLab

**Persona:** Pesquisadora do GaveaLab com corpus de 200 relatos de consulta pública  
**Objetivo:** Transformar CSV bruto em insight estruturado

| # | Ação | Interface | Emoção | Dificuldade |
|---|------|-----------|--------|-------------|
| 1 | Abre o app Streamlit (`localhost:8501`) | Streamlit UI | Orientada | Nenhuma |
| 2 | Upload CSV com coluna `text`; nomeia a sessão | Página Upload | Confiante | Nenhuma |
| 3 | Clica "Gerar temas automáticos" | Página Auto-topics | Curiosa | LLM demora ~30s sem barra de progresso |
| 4 | Revisa árvore de tópicos gerada | Página Auto-topics | Satisfeita | Tópicos às vezes muito genéricos |
| 5 | Navega para "Visualizar clusters" — explora scatter plot | Plotly scatter | Deleitada | Primeiro run calcula embeddings (lento) |
| 6 | Hover sobre pontos — identifica cluster de reclamações sobre transporte | Plotly scatter | Insightful | — |
| 7 | Navega para "Opiniões divergentes" — lê cruxes | Página Cruxes | Reflexiva | Cruxes às vezes repetem em vez de contrastar |

### JM-TB-002: Cidadão registra demanda e agente cria encaminhamento (Fala-Gávea)

**Persona:** Cidadão da Gávea sem experiência técnica; Delegado como agente público  
**Objetivo:** Problema de iluminação pública registrado e encaminhado

| # | Quem | Ação | Interface | Emoção |
|---|------|------|-----------|--------|
| 1 | Cidadão | Abre o app; clica no mapa no ponto do problema | Leaflet map | Confiante |
| 2 | Cidadão | Preenche descrição do problema, seleciona tipo "Iluminação" | Form | Rápido |
| 3 | Agente | Recebe notificação de novo relato; abre na listagem | Admin panel | Atento |
| 4 | Agente | Busca "iluminação pública quebrada" no chat NL | NL filter | Satisfeito |
| 5 | Agente | Vê relatos similares; identifica padrão recorrente na rua X | Mapa + similares | Insightful |
| 6 | Agente | Seleciona 3 relatos relacionados para cesta | Cesta UI | Eficiente |
| 7 | Agente | Cria encaminhamento para RIOLUZ com os 3 relatos | Form | Confiante |
| 8 | Cidadão | Recebe status "Encaminhado para RIOLUZ" no app | Status view | Satisfeito |
