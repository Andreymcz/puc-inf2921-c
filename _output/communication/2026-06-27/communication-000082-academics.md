# Communication 000082 | ACD | 2026-06-27 UTC | Academics

> **Relatorio de pesquisa para avaliacao academica** do capstone INF2921/CIS2114 (AI Systems Design, PUC-Rio, 2026.1). Equipe: Andrey, Mauro, Julia, Herbert, Natali, Sheila.
> Sucessor de [communication-000075](../2026-06-19/communication-000075-academics.md) (19/06): estende a narrativa das Fases 0-6 para as **Fases 7-10** (produto MVP, camada de IA, participacao/transparencia e meta-IA) e adiciona o enquadramento teorico (engenharia semiotica / metacomunicacao) e a agenda de pesquisa.
> Documento-mae da trajetoria: [communication-000077 — timeline do projeto](../2026-06-26/communication-000077-timeline-projeto.md). Casos de uso -> prototipos: [communication-000081](communication-000081-casos-de-uso-prototipos.md).

**Legenda de profundidade (mesma de [077](../2026-06-26/communication-000077-timeline-projeto.md)):** 🟢 visao geral · 🟡 artefato SEJA (plano / reflexao / research / roadmap) · 🔴 fonte original (`.md`, `.pdf`, codigo).

---

## 0. Sintese executiva (para o leitor academico)

Este documento descreve o **fala-gavea** — um canal comunitario digital de seguranca urbana para o bairro da Gavea (Rio de Janeiro) — como **objeto de pesquisa duplo**, relevante para quem investiga (a) engenharia de software assistida por IA, (b) interacao humano-computador e engenharia semiotica, e (c) sistemas de IA com humano-no-comando aplicados a participacao civica.

O argumento central tem tres camadas:

1. **Produto como artefato de design research.** O fala-gavea nao foi concebido de cima para baixo. Ele resultou de um **"zoom in" deliberado e documentado** — de um Atlas Digital Georreferenciado da Amazonia (escala continental) para um canal de seguranca de bairro — preservando **dois invariantes** desde a origem: a **camada geoespacial** e a **soberania de dados** (toda inferencia de IA roda localmente). A trajetoria e, ela propria, um estudo de caso de reducao de escopo iterativa ancorada em evidencia de campo. 🟡 [reflection-000052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md)

2. **Processo como corpus auditavel.** Todo o desenvolvimento ocorreu sob o harness **SEJA** sobre Claude Code, no ciclo `/research -> /plan -> /implement -> /check -> /document | /communicate -> /reflect`. O resultado e um corpus numerado e datado (planos, roadmaps, reflexoes, decisoes `D-NNN`, comunicacoes, telemetria) que permite reconstruir **o que, como e por que** de cada inflexao. Para uma disciplina de *AI Systems Design*, este corpus e dado empirico, nao apenas documentacao.

3. **Metacomunicacao como espinha dorsal.** O design intent do projeto e escrito na voz designer->usuario da **engenharia semiotica** ("eu projetei X para que voce Y"), tornando a *mensagem de metacomunicacao* um artefato inspecionavel — e levantando a questao de pesquisa de como essa mensagem se comporta quando **uma IA media o vao entre designer e usuario**.

A contribuicao que oferecemos a outro pesquisador nao e um produto acabado, e sim um **par (artefato, registro)** suficientemente completo para ser reconstruido, criticado ou usado como caso comparativo.

---

## 1. Fundamentacao teorica

> *Diataxis: Explanation.* Esta secao expoe os compromissos teoricos do projeto e os conecta a literatura. Distinguimos **afirmacoes apoiadas em evidencia** (marcadas como tal) de **hipoteses de design** (idem).

### 1.1 Engenharia semiotica e metacomunicacao

A engenharia semiotica (de Souza) trata a interface como uma **mensagem unidirecional do designer para o usuario** — uma metacomunicacao cujo conteudo e, em parafrase, *"eis o que eu, designer, entendi sobre quem voce e, o que voce quer, e como projetei este sistema para voce atingir esses objetivos desta forma."* A qualidade dessa mensagem e a **comunicabilidade**: a capacidade do sistema de transmitir, na propria interacao, a intencao de design.

No fala-gavea, essa mensagem nao fica implicita no codigo: ela e **textualizada** no design intent do produto, escrito na primeira pessoa do designer. Cada feature carrega uma *intencao de metacomunicacao* na forma "I have designed X so that you Y". Exemplos extraidos do registro do produto:

- *Upload/registro de relato:* "projetei o registro para criar uma demanda persistente imediatamente, para que voce sempre possa retornar a um acompanhamento sem reenviar seus dados."
- *Sugestao automatica de categoria:* "projetei a sugestao da IA como ponto de partida, nao como veredito — voce confirma ou corrige — para que a estrutura nunca trave a sua leitura do territorio."
- *AiBadge de proveniencia:* "marquei na UI todo conteudo gerado por IA para que voce sempre saiba o que e maquina e o que e humano."

🔴 [decisoes do fala-gavea (`product-design-as-intended.md`)](../../../fala-gavea/product-design/project/product-design-as-intended.md) · 🔴 [fg:plan-000178 — AiBadge](../../../fala-gavea/_output/plans/plan-000178-aibadge-provenance-marker.md)

> **Hipotese de design (H1).** Tornar a mensagem de metacomunicacao um *artefato de primeira classe* — versionado, ligado a decisoes `D-NNN` e a planos — aumenta a comunicabilidade do sistema porque a intencao deixa de ser inferida e passa a ser auditavel. Esta e uma hipotese; nao a medimos formalmente (ver §3, ameacas a validade).

### 1.2 O harness como sistema de atos comunicativos

A arquitetura do SEJA pode ser lida em chave semiotica: cada **skill** e um *ato comunicativo* com pre-condicoes e pos-condicoes; cada **perspectiva de revisao** (`/check`) e uma *lente de avaliacao*; cada **camada de onboarding** e um *andaime de conhecimento*. O ciclo `/research -> /plan -> /implement -> /check -> /document | /communicate -> /reflect` e uma cadeia de signos em que o output de um ato e o input interpretado do proximo. O proprio ato de `/communicate` (que produziu este documento) e a metacomunicacao do designer *sobre o processo*, dirigida a um publico-alvo especifico (aqui, o academico).

### 1.3 IA mediando o vao designer-usuario

O ponto teoricamente mais original do projeto e que **a IA aparece dos dois lados da mensagem**:

- **Na producao da mensagem (processo):** o agente (Claude, sob SEJA) co-redige planos, codigo, documentacao e *as proprias comunicacoes*. O designer humano permanece como *preposto* (na acepcao da engenharia semiotica) — quem responde pela intencao — mas parte da emissao e delegada a um interlocutor de IA.
- **Na recepcao e re-emissao (produto):** o fala-gavea categoriza, agrupa e responde em linguagem natural; e ate **explica a si mesmo** via um helper RAG (`POST /nl/help`) que reenvia ao usuario uma versao da intencao de design indexada na documentacao. 🔴 [fg:plan-000177](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md)

> **Questao de pesquisa (RQ).** Quando uma IA media o vao designer->usuario — emitindo a mensagem no processo e re-emitindo-a no produto — *de quem* e a metacomunicacao percebida pelo usuario final, e como medir sua comunicabilidade? (Desenvolvida em §4.)

### 1.4 Linhagem metodologica: deliberacao publica computacional

O produto herda a linhagem de **Talk to the City** (T3C) e **Polis/Pol.is** — sistemas que transformam grandes volumes de opiniao cidada em estrutura navegavel (topicos, claims, pontos de divergencia). A Fase 1 sintetizou explicitamente esse campo (Decidim, Pol.is, T3C, Consul, vTaiwan) antes de convergir para um T3C local. 🔴 [casos-de-uso.md](../../../knowledge/casos-de-uso.md) · 🟡 [plan-000001](../../plans/plan-000001-trl3-poc-tttc-local-ollama.md)

A contribuicao incremental em relacao a esses sistemas e tripla: (i) **soberania de dados por construcao** (inferencia 100% local via Ollama, contra deployments em nuvem); (ii) **ancoragem geoespacial** dos claims (relatos georreferenciados + mapa colaborativo, o "Projeto 08"); e (iii) o **feedback loop few-shot human-in-the-loop** como alternativa de baixo custo ao fine-tuning.

---

## 2. Metodologia: design research documentado

> *Diataxis: Explanation, com componente de Reference no Anexo A.* Aqui descrevemos *como* o conhecimento foi produzido, em detalhe suficiente para reconstrucao ou critica.

### 2.1 Problema ancorado em evidencia de campo

O problema **nao foi inventado**. Ele deriva do **Diagnostico GaveaLab 2023 (FAPERJ No 20/2022)**, pesquisa de campo conduzida pelo Laboratorio de Gestao em Design (LGD/PUC-Rio) entre junho e novembro de 2023, com **380 entrevistados** em tres recortes territoriais do mesmo bairro (Gavea-"asfalto", Rocinha, Parque da Cidade). Achados que ancoram o escopo:

- O **Mapa de Forcas Locais Atuantes (MFLA)** identifica **SEGURANCA (24%)** e **EDUCACAO (22%)** como temas alavancadores no "asfalto"; para os moradores das favelas, os tres prioritarios sao EDUCACAO, DESENVOLVIMENTO ECONOMICO e SEGURANCA PUBLICA.
- Seguranca e a **maior dor** (20% das citacoes espontaneas no asfalto, 9% nas favelas).
- **Divergencia decisiva de sentido:** no asfalto, "seguranca" significa *mais policiamento*; nas favelas, significa *garantia de direitos e ausencia de violencia policial*.

Esse ultimo achado e o que justifica o produto: um instrumento que **capture a multiplicidade de vozes sobre o mesmo territorio**, em vez de uma media estatistica que apaga o conflito de sentido. Coordenacao do diagnostico: Profa. Fabienne Torres Schiavo (Doutora em Design, CAPES), com os Profs. Carlo Franzato e Claudio Freitas de Magalhaes.

🔴 [Diagnostico FAPERJ 2023 (PDF)](../../../knowledge/Strategic%20Design%204%20Smart%20City%20Lab%20_Gavea%20Lab%20diagnostico_onepage.pdf) · 🔴 [Reunioes de stakeholders (PDF)](../../../knowledge/Reunioes-stakeholders-1-2.pdf)

> 🔒 **Governanca de citacao.** O diagnostico FAPERJ e documentos do GaveaLab sao de terceiros: citar com credito e confirmar permissao de redistribuicao. O enunciado do **Projeto 08** e o documento de validacao (Fabiene) exigem **autorizacao previa** antes de reproducao publica. O dump de WhatsApp da equipe **nao** e fonte deste trabalho e nao deve ser publicado (ver [077 §Governanca / Anexo E](../2026-06-26/communication-000077-timeline-projeto.md)).

### 2.2 A linhagem de prototipos como iteracao de design research

Cada fase produziu um **prototipo executavel** que testou uma hipotese de design e gerou aprendizado registrado em uma reflexao. A reducao de escopo foi *guiada por viabilidade, validacao institucional e reaproveitamento de capacidades ja construidas* — nao por abandono.

| Fase | Quando | Prototipo (PoC) | Hipotese testada / aprendizado | Artefato-fonte |
|---|---|---|---|---|
| 0 | abr/26 | **kb-qa** (RAG local + MCP) | Recuperacao local ancora respostas de IA sem nuvem; cobre ~20-30% de um atlas completo | 🔴 [Reuniao-23-04](../../../knowledge/Reuniao-23-04-2026.md) |
| 1 | mai/26 | **T3C local** (Docker + Ollama, TRL3) | Deliberacao publica computacional roda local; convergencia para T3C | 🟡 [plan-000001](../../plans/plan-000001-trl3-poc-tttc-local-ollama.md) |
| 2 | jun/26 | **Streamlit + SQLite + Ollama** | Pipeline temas->claims->cruxes->UMAP e viavel; formaliza CU01/CU02 (LGPD, PL 2338) | 🟡 [plan-000008](../../plans/plan-000008-gavealab-poc-scaffold.md) · [plan-000016](../../plans/plan-000016-gavealab-poc-umap-visualization.md) |
| 3 | jun/26 | **fala-gavea "Twitter-like"** (FastAPI + Streamlit) | Relatos + likes + clusters; reflexao detecta pipeline de analise faltante | 🟡 [reflection-000037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md) · [plan-000027](../../plans/plan-000027-fala-gavea-setup-streamlit.md) |
| 4 | **15/jun** | **Zoom in p/ Gavea** | *O clustering ja construido E o motor do caso de uso do agente; o mapa e uma nova camada, nao um novo projeto.* Validacao da Fabiene -> Projeto 08 | 🟡 [reflection-000052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md) · [research-000074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md) |
| 5 | jun/26 | **Chat NL intent-to-filter** | Lacuna do feedback loop (correcoes do agente nao viravam sinal); roadmap do "Waze comunitario" | 🟡 [reflection-000069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md) · [roadmap-000070](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md) |
| 6 | jun/26 | **Clean architecture** (FastAPI + SQLAlchemy + Pydantic v2) | Reescrita testavel; `fala-gavea` vira submodulo com harness SEJA proprio | 🟡 [roadmap-000071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md) · [plan-000072](../../plans/plan-000072-fala-gavea-scaffold-e-seja-setup.md) · [check-000073](../../check-logs/check-000073-validate-fala-gavea-scaffold.md) |

A leitura detalhada de cada fase e os casos de uso associados estao em [communication-000081](communication-000081-casos-de-uso-prototipos.md) e nas Fases 0-6 da [077](../2026-06-26/communication-000077-timeline-projeto.md#2-fases-detalhadas).

### 2.3 Continuacao da timeline: Fases 7-10 (novidade em relacao a 075)

A comunicacao academica anterior ([075](../2026-06-19/communication-000075-academics.md)) parou na Fase 6. Desde entao, o submodulo `fala-gavea` evoluiu de scaffold para **produto MVP entregavel**, com seu **proprio corpus SEJA** (planos ate ~000183, 4 roadmaps, 11 reflexoes, **17 decisoes `D-NNN`**, 4 comunicacoes por publico).

| Fase | Marco | Significado para a pesquisa | Artefato-fonte |
|---|---|---|---|
| **7** — Produto MVP | Auth JWT por roles (citizen/agent/admin) + Reports + `ReportType` dinamico + `Forwarding` (agregacao N relatos) + **SPA React** (mapa, formulario com geolocalizacao, painel do agente) | Materializa CU1 (cidadao) e CU2 (agente); o `Forwarding` many-to-many e a operacionalizacao do "encaminhamento institucional" | 🔴 [fg:plan-000073](../../../fala-gavea/_output/plans/plan-000073-feature-b-wave-0-item-1-domain-auth-reports.md) · [fg:plan-000082 (SPA)](../../../fala-gavea/_output/plans/plan-000082-feature-f-wave-1-item-4-frontend-spa-react.md) |
| **8** — Camada de IA | Embeddings + ingestao; busca semantica + relatos similares; **BERTopic**; **chat NL RAG**; sugestao plugavel de `ReportType` (humano no comando) | Reintroduz o pipeline de clustering como servico do produto; substitui UMAP/HDBSCAN exploratorio por BERTopic de producao | 🔴 [fg:plan-000094 (busca)](../../../fala-gavea/_output/plans/plan-000094-semantic-search-similar-reports-wave1.md) · [fg:plan-000100 (RAG chat)](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md) · [fg:plan-000174 (sugestao plugavel)](../../../fala-gavea/_output/plans/plan-000174-pluggable-report-type-suggestion.md) |
| **9** — Participacao + transparencia | Votos + comentarios + relato anonimo; "meus relatos" / "meus encaminhamentos"; filtros salvos; grid cross-filter | Operacionaliza a "validacao coletiva com 1 clique" do diagnostico; transparencia do ciclo de vida da demanda | 🔴 [fg:roadmap-000151](../../../fala-gavea/_output/roadmaps/roadmap-000151-citizen-feedback-votes-comments-anonymization.md) · [fg:plan-000164](../../../fala-gavea/_output/plans/plan-000164-meus-relatos-nav-inline-votes-sort.md) |
| **10** — Meta-IA + entrega | Helper self-docs SEJA-aware (**D-017**); **AiBadge** de proveniencia (**D-015**); sintese de comentarios; Docker + Railway; seed showcase; docs para 4 publicos | A plataforma **explica a si mesma** e marca a proveniencia da IA — o no onde os dois eixos de IA (produto e processo) se encontram | 🔴 [fg:plan-000177 (helper)](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md) · [fg:plan-000178 (AiBadge)](../../../fala-gavea/_output/plans/plan-000178-aibadge-provenance-marker.md) · [fg:plan-000183 (seed)](../../../fala-gavea/_output/plans/plan-000183-local-showcase-seed-pipeline.md) |

---

## 3. Decisoes de design de IA, com racional

> *Diataxis: Explanation.* Cada decisao e apresentada como *contexto -> escolha -> consequencia*, a forma DRR usada nas decisoes `D-NNN` do projeto.

### 3.1 Dois eixos de IA

Para a avaliacao academica, separamos **IA no produto** de **IA no processo**.

**IA no produto (local, auditavel, human-in-the-loop):**

- Inferencia local via **Ollama** (`qwen3:8b`), endpoint OpenAI-compativel, modelo configuravel por variavel de ambiente.
- **Categorizacao/sugestao** de relatos; **clustering semantico** (embeddings + BERTopic; UMAP/HDBSCAN na linhagem exploratoria).
- **Busca semantica** (ChromaDB) e relatos similares; **chat NL -> filtros de API** (intent-to-filter) e **chat RAG**.
- **Feedback loop few-shot:** o agente confirma ou corrige a categoria sugerida; a correcao e gravada como evento append-only (`CategoryCurationEvent`) e **injetada no prompt** da proxima categorizacao — *sem fine-tuning*.
- **AiBadge:** todo conteudo gerado por IA e marcado na UI (proveniencia).

**IA no processo (o metodo como resultado):** o ciclo SEJA descrito em §1.2 e §2, cujo corpus e o objeto de estudo.

🔴 [fg:plan-000100 — chat RAG](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md) · 🟡 [roadmap-000070 — feedback loop](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md)

### 3.2 Decisoes-chave (racional resumido)

| Decisao | Contexto | Escolha | Consequencia |
|---|---|---|---|
| **Inferencia local** | Dados de cidadaos/comunidades; principios CARE/OCAP herdados do Atlas amazonico | Ollama local, sem nuvem | Soberania de dados por construcao; custo de hardware e latencia local |
| **Few-shot em vez de fine-tuning** | Correcoes do agente sao escassas e continuas; fine-tuning e caro e opaco | Injecao few-shot a partir de `CategoryCurationEvent` append-only | Aprendizado barato, **auditavel** e com humano no comando; teto de capacidade do prompt |
| **Zoom in Atlas -> Gavea** | Atlas continental inviavel no prazo; existia clustering reaproveitavel e validacao institucional | Reduzir a 1 bairro, 1 vertical (seguranca), 2 personas | Artefato pequeno, executavel e validado; perda de abrangencia geografica |
| **AiBadge (D-015)** | Necessidade de distinguir conteudo humano de gerado por IA | Marcar proveniencia na UI | Transparencia (alinha a PL 2338); custo de design de UI |
| **Helper SEJA-aware (D-017)** | A plataforma deveria poder se explicar a diferentes perfis | RAG self-docs com enquadramento "meta" para admin | Auto-documentacao; risco de exposicao de detalhes internos -> escopo por role |

🔴 [decisoes do fala-gavea (`D-NNN`)](../../../fala-gavea/product-design/project/product-design-as-intended.md)

> **Afirmacao apoiada por evidencia.** O papel da IA "como auxiliadora da curadoria, nao como curador principal" e uma formulacao registrada da equipe (transcricoes de reuniao) e implementada como o padrao human-in-the-loop do agente. 🔴 [Reunioes-stakeholders-1-2.pdf](../../../knowledge/Reunioes-stakeholders-1-2.pdf)

---

## 4. Agenda de pesquisa (questoes em aberto)

> *Diataxis: Explanation.* O projeto, lido como artefato de pesquisa, abre questoes que excedem a entrega da disciplina. Sao **convites a estudo**, nao resultados.

- **RQ1 — Metacomunicacao mediada por IA.** Quando o agente co-emite a mensagem de design (processo) e o produto a re-emite (helper RAG), de quem e a comunicabilidade percebida? Metodo sugerido: estudo de comunicabilidade adaptado (MAC/MIS) com etiquetas de rupturas comunicativas, comparando interfaces com e sem AiBadge.
- **RQ2 — Efeito do registro estruturado.** A textualizacao da intencao ("I designed X so that you Y") ligada a `D-NNN` melhora mensuravelmente a manutenibilidade e a fidelidade designer-codigo? Metodo: estudo de caso comparativo com/sem o registro, medindo *spec-drift* ao longo do tempo.
- **RQ3 — Few-shot auditavel vs. fine-tuning.** Em curadoria continua de baixo volume, qual a curva de qualidade/custo do feedback loop few-shot append-only frente ao fine-tuning? Metodo: experimento controlado sobre o corpus de `CategoryCurationEvent`.
- **RQ4 — Limites do modelo do harness.** Onde o ciclo SEJA falha como modelo comunicativo? (Ex.: quando a intencao do designer e tacita; quando a IA "alucina" intencao; quando a reflexao pos-hoc reescreve a historia.) Metodo: analise critica do proprio corpus, buscando descontinuidades entre `reflection-NNN` e os commits que ela narra.
- **RQ5 — Etica da multiplicidade de vozes.** Como evitar que clustering e medias apaguem o conflito de sentido (asfalto x favela) documentado no diagnostico? Metodo: avaliacao de fairness por subgrupo territorial sobre as categorias sugeridas pela IA.

---

## 5. Etica e governanca

O projeto adota tres compromissos formais, alinhados a constituicao do projeto e aos documentos da disciplina:

- **Soberania de dados (data sovereignty).** Toda inferencia roda localmente (Ollama); relatos de cidadaos e resultados de analise nunca deixam a maquina local. Heranca direta dos principios **CARE/OCAP** do contexto do Atlas amazonico.
- **LGPD.** Minimizacao e anonimizacao de dados pessoais; relato anonimo suportado; coordenadas de relatos tratadas como PII potencial (truncar lat/lon — ver [research-000074 R3](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md)).
- **PL 2338 (Marco Regulatorio da IA no Brasil).** Transparencia da proveniencia (AiBadge), human-in-the-loop obrigatorio antes de tratar saida de IA como resultado, e inspecionabilidade de modelo/prompts.

**Limitacoes e ameacas a validade (declaradas):**

- **Validacao externa pendente.** O caso de uso real foi atestado pela stakeholder (Fabiene), mas o produto ainda nao foi avaliado em uso por moradores/agentes; as hipoteses H1 e as RQ permanecem nao medidas.
- **Vies de embedding/clustering.** A proximidade espacial no mapa de claims e artefato do modelo de embedding; pode sugerir consenso/divergencia inexistentes (mitigacao: claim visivel no hover, curadoria humana).
- **Dataset semente.** As demos correm sobre relatos sinteticos/seed; generalizacao para dados reais e hipotese, nao resultado.
- **Reflexividade do corpus.** Como o registro SEJA e co-produzido por IA, ele pode racionalizar decisoes *a posteriori* (ver RQ4) — o que e simultaneamente um risco de validade e um objeto de estudo.

> 🔒 **Notas de governanca de terceiros.** Projeto 08 e documento de validacao (Fabiene/GaveaLab): citacao requer autorizacao. Dump de WhatsApp da equipe: nunca reproduzir; nao e fonte deste trabalho. Diagnostico FAPERJ e docs do GaveaLab: citar com credito, confirmar redistribuicao.

---

## 6. Reprodutibilidade e como construir sobre este trabalho

> *Diataxis: How-to / Reference.* Detalhe suficiente para que outro pesquisador reconstrua, critique ou estenda.

### 6.1 Obter o corpus e o produto

```bash
# repo-pai (corpus SEJA das Fases 0-6 + comunicacoes) + submodulo do produto:
git clone --recurse-submodules https://github.com/Andreymcz/puc-inf2921-c
# se ja clonou sem submodulos:
git submodule update --init fala-gavea
```

Os links 🔴 que apontam para `fala-gavea/` exigem o submodulo populado. Os links para `knowledge/` e `_output/` resolvem direto no repo-pai.

### 6.2 Onde olhar (mapa do corpus)

| O que voce quer estudar | Onde | Tipo |
|---|---|---|
| A trajetoria completa (espinha) | [077 — timeline](../2026-06-26/communication-000077-timeline-projeto.md) | 🟢/🟡/🔴 |
| Casos de uso -> prototipos | [081](communication-000081-casos-de-uso-prototipos.md) | 🟡 |
| As decisoes de inflexao de escopo | reflections [037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md) / [052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md) / [069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md) | 🟡 |
| O retorno a camada geoespacial | [research-000074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md) | 🟡 |
| As decisoes `D-NNN` do produto | [`product-design-as-intended.md`](../../../fala-gavea/product-design/project/product-design-as-intended.md) | 🔴 |
| A IA do produto (planos) | fg:[100 RAG](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md) · [177 helper](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md) · [178 AiBadge](../../../fala-gavea/_output/plans/plan-000178-aibadge-provenance-marker.md) | 🔴 |
| O produto executavel | [README](../../../fala-gavea/README.md) · [CLAUDE.md](../../../fala-gavea/CLAUDE.md) | 🔴 |

### 6.3 Estender o harness ou comparar (ganchos de pesquisa)

- **Replicar o metodo:** o ciclo SEJA (`/research -> /plan -> /implement -> /check -> /document | /communicate -> /reflect`) e reproduzivel em outro dominio; o corpus deste projeto serve de *baseline* comparativo para estudos de engenharia de software assistida por IA.
- **Instrumentar a comunicabilidade:** as comunicacoes por publico (EVL/CLT/USR/ACD) sao geradas pelo skill `/communicate` a partir das mesmas fontes — um terreno para estudar como a *mesma intencao de design* e re-enquadrada por audiencia.
- **Auditar o feedback loop:** o `CategoryCurationEvent` append-only e um dataset pronto para estudar aprendizado human-in-the-loop few-shot (RQ3).

### 6.4 Stack consolidada (referencia)

| Camada | Genese (F0-F5) | Produto entregue (F6-F10) |
|---|---|---|
| Linguagem / gestao | Python 3.13 + uv | Python 3.13 + uv |
| Web / API | Streamlit | **FastAPI** (clean architecture) |
| Frontend | Streamlit pages | **React 18 + Vite + TS + Tailwind + react-leaflet** |
| Persistencia | SQLite (`GaveaLabWorkspace`) | SQLite via **SQLAlchemy** |
| Auth | nenhuma (local) | **JWT** roles citizen/agent/admin |
| Embeddings | ChromaDB + sentence-transformers | idem (multilingual-e5 / nomic) |
| LLM local | Ollama (qwen) | **Ollama** (`qwen3:8b`) + provider plugavel |
| Visualizacao | UMAP + HDBSCAN + Plotly | Leaflet + GeoJSON; **BERTopic** |
| Entrega | — | **Docker + Railway**; seed showcase |
| Qualidade | pytest, ruff, pyright | + **Vitest/RTL** |

---

## 7. Fechamento

> O merito academico nao esta em ter alcancado o escopo inicial, e sim em ter feito o **caminho inverso de forma deliberada e documentada** — e em deixar esse caminho *legivel* como objeto de pesquisa.

Os dois invariantes que sobreviveram a todas as fases — **camada geoespacial** e **soberania de dados local** — ligam o produto final (fala-gavea) a sua origem amazonica (o Atlas). Em torno deles, o projeto oferece tres contribuicoes ao leitor academico: um **artefato de design research** rastreavel ate evidencia de campo (FAPERJ, 380 respondentes); um **corpus de processo** que documenta IA-assistindo-engenharia ponta a ponta; e uma **mensagem de metacomunicacao textualizada** que torna inspecionavel — e estudavel — o vao entre designer e usuario quando uma IA o medeia.

**Equipe:** Andrey · Mauro · Julia · Herbert · Natali · Sheila · `communication-000082` · INF2921/CIS2114 (AI Systems Design, PUC-Rio, 2026.1)

---

## Anexo A — Indice de fontes (documento vivo)

**Knowledge (`knowledge/`):** [Reuniao-23-04-2026.md](../../../knowledge/Reuniao-23-04-2026.md) · [casos-de-uso.md](../../../knowledge/casos-de-uso.md) · [Casos_de_uso_1](../../../knowledge/Casos_de_uso_10-06-2026_1.md) · [Casos_de_uso_2](../../../knowledge/Casos_de_uso_10-06-2026_2.md) · [Reunioes-stakeholders-1-2.pdf](../../../knowledge/Reunioes-stakeholders-1-2.pdf) · [Diagnostico FAPERJ (PDF)](../../../knowledge/Strategic%20Design%204%20Smart%20City%20Lab%20_Gavea%20Lab%20diagnostico_onepage.pdf) · [CENARIOS…HERBERT.txt](../../../knowledge/CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt) · [RELATOS_HERBERT.txt](../../../knowledge/RELATOS_HERBERT.txt)

**SEJA repo-pai (`_output/`):** [research-000074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md) · [check-000073](../../check-logs/check-000073-validate-fala-gavea-scaffold.md) · [roadmap-000070](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md) · [roadmap-000071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md) · reflections [037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md) / [052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md) / [069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md) · planos [000001](../../plans/plan-000001-trl3-poc-tttc-local-ollama.md) / [000008](../../plans/plan-000008-gavealab-poc-scaffold.md) / [000016](../../plans/plan-000016-gavealab-poc-umap-visualization.md) / [000027](../../plans/plan-000027-fala-gavea-setup-streamlit.md) / [000072](../../plans/plan-000072-fala-gavea-scaffold-e-seja-setup.md)

**Comunicacoes relacionadas:** [077 — timeline](../2026-06-26/communication-000077-timeline-projeto.md) · [081 — casos de uso -> prototipos](communication-000081-casos-de-uso-prototipos.md) · [075 — academicos (anterior)](../2026-06-19/communication-000075-academics.md)

**Produto (`fala-gavea/`):** [README](../../../fala-gavea/README.md) · [CLAUDE.md](../../../fala-gavea/CLAUDE.md) · [`product-design-as-intended.md` (D-NNN)](../../../fala-gavea/product-design/project/product-design-as-intended.md) · planos [073](../../../fala-gavea/_output/plans/plan-000073-feature-b-wave-0-item-1-domain-auth-reports.md) / [082 SPA](../../../fala-gavea/_output/plans/plan-000082-feature-f-wave-1-item-4-frontend-spa-react.md) / [094 busca](../../../fala-gavea/_output/plans/plan-000094-semantic-search-similar-reports-wave1.md) / [100 RAG](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md) / [174 sugestao](../../../fala-gavea/_output/plans/plan-000174-pluggable-report-type-suggestion.md) / [177 helper](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md) / [178 AiBadge](../../../fala-gavea/_output/plans/plan-000178-aibadge-provenance-marker.md) / [183 seed](../../../fala-gavea/_output/plans/plan-000183-local-showcase-seed-pipeline.md) · roadmap [151](../../../fala-gavea/_output/roadmaps/roadmap-000151-citizen-feedback-votes-comments-anonymization.md)

> ⚠️ Links de `fala-gavea/` requerem o submodulo populado (`git submodule update --init`). PDFs abrem a partir do `.html` aberto localmente.
