---
marp: true
theme: default
paginate: true
title: "fala-gávea — Relatório & Apresentação"
author: "Andrey, Mauro, Julia, Herbert, Natali, Sheila"
---

<!--
Communication 000077 (v3) | ACD/EVL | INF2921/CIS2114 — AI Systems Design 2026.1
Documento único: RELATÓRIO + APRESENTAÇÃO (formato de slides, Marp).
- Para exportar slides: abrir no VS Code com a extensão "Marp for VS Code"
  → Export slide deck → PDF / PPTX / HTML.
- Para ler como relatório: abrir o .html gerado (md_to_html) ou este .md.
Cada slide tem notas de orador (este bloco de comentário) com a narrativa
do relatório, e links que aprofundam: 🟢 slide → 🟡 relatório SEJA → 🔴 artefato/código.
-->

# Fala Gávea
## Um canal comunitário de segurança urbana para a Gávea

**Relatório & Apresentação** — documento único · INF2921/CIS2114 (AI Systems Design, PUC-Rio, 2026.1)
**Equipe:** Andrey · Mauro · Julia · Herbert · Natali · Sheila
**Data:** 26/06/2026 · `communication-000077` (v3)

> *Tese:* fala-gávea é um **"zoom in" deliberado e documentado** — do Atlas Digital da Amazônia (continental) para um canal de **segurança urbana** no bairro da Gávea — preservando dois invariantes desde a origem: **camada geoespacial** e **soberania de dados** (toda IA roda localmente).

<!--
RELATÓRIO. Este documento serve a três propósitos ao mesmo tempo:
(1) apresentação para a banca/disciplina; (2) relatório escrito de desenvolvimento;
(3) índice da nossa base de conhecimento (KB). Ele foi gerado sob o harness SEJA e
é um "documento vivo": todos os artefatos citados são links para os arquivos originais.
-->

---

## Como ler este documento (modelo de profundidade)

**Um documento, três camadas — quanto mais fundo, mais técnico:**

- 🟢 **Slide** — a visão geral (o que você vê aqui).
- 🟡 **Relatório SEJA** — pesquisa, planos, reflexões e roadmaps (médio).
- 🔴 **Artefato / código / fonte** — `.md`, `.pdf`, planos do produto (técnico).

📎 **Para anexar à disciplina:** exportar como PDF/PPTX (Marp) ou anexar o `.html`.
🔗 **Documento vivo:** clique nos links para abrir os arquivos originais do repositório.
🧩 **Soma com o Dropbox:** este deck + a [pasta compartilhada no Dropbox](#anexo-d--base-de-conhecimento-kb) formam a **base de conhecimento (KB)** do projeto — ver [Anexo D](#anexo-d--base-de-conhecimento-kb).

<!--
RELATÓRIO. A ideia de profundidade progressiva resolve um problema real de
comunicação de projeto: a banca precisa do overview; o avaliador técnico precisa
do código e das decisões. Em vez de dois documentos, um só, com links que
descem do conceitual ao técnico.
-->

---

## O problema

A **Gávea** concentra realidades urbanas radicalmente distintas — moradores do "asfalto", comunidades da **Rocinha** e do **Parque da Cidade** — que dividem o mesmo território mas vivem em circuitos separados de representação.

> *"Não existe hoje um canal unificado, acessível e confiável para que essa diversidade de vozes chegue a quem pode agir sobre os problemas."*

Do lado dos agentes públicos: dados **fragmentados, não estruturados e de difícil acesso** → decisão lenta e descolada da realidade.

🔴 [Diagnóstico FAPERJ 2023 (PDF)](../../../knowledge/Strategic%20Design%204%20Smart%20City%20Lab%20_Gavea%20Lab%20diagnostico_onepage.pdf) · 🟡 [Evidências](#evidencia-que-ancora-o-escopo)

<!--
RELATÓRIO. O problema não foi inventado: vem do diagnóstico de campo do GaveaLab
(FAPERJ 2023, 380 entrevistados). Segurança é o tema alavancador e, ao mesmo tempo,
a maior dor — com percepções opostas entre asfalto e favela.
-->

---

## A tese: um "zoom in" documentado

**De um atlas continental a um bairro concreto** — uma redução de escopo guiada por viabilidade, validação institucional e reaproveitamento do que já existia.

| | Origem | Produto entregue |
|---|---|---|
| Escala | Amazônia (continental) | Bairro da Gávea |
| Vertical | múltipla | **Segurança urbana** |
| Personas | difusas | **Cidadão** + **Agente público** |
| Invariantes | geoespacial + soberania de dados | **geoespacial + soberania de dados** |

🟡 [§2 Fases detalhadas](#2-fases-detalhadas) · 🔴 [reflection-000052 — a decisão de zoom in](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md)

<!--
RELATÓRIO. O mérito acadêmico não está em ter alcançado o escopo inicial, e sim em
ter feito o caminho inverso de forma deliberada e registrada. Os dois invariantes
sobreviveram a todas as fases e ligam o produto final à origem amazônica.
-->

---

## Linha do tempo (visão macro)

| Fase | Quando | Enquadramento | Marco |
|---|---|---|---|
| [0](#fase-0) | abr/26 | Atlas da Amazônia | kb-qa (RAG local + MCP) |
| [1](#fase-1) | mai/26 | Participação cidadã | PoC Talk-to-the-City local |
| [2](#fase-2) | jun/26 | GaveaLab PoC | Pipeline temas→claims→cruxes→UMAP |
| [3](#fase-3) | jun/26 | fala-gávea (1ª) | Posts, likes, clusters (Streamlit) |
| [4](#fase-4) | **15/jun** | **Zoom in p/ Gávea** | Segurança; Fabiene → **Projeto 08** |
| [5](#fase-5) | jun/26 | Canal comunitário | Busca NL; feedback loop |
| [6](#fase-6) | jun/26 | Clean architecture | FastAPI; `fala-gavea` submódulo SEJA |
| [7](#fase-7) | jun/26 | **Produto MVP** | Auth/roles + Reports + Forwardings + **React SPA** |
| [8](#fase-8) | jun/26 | Camada de IA | Busca semântica, BERTopic, **chat NL RAG** |
| [9](#fase-9) | jun/26 | Participação + transparência | Votos, comentários, "meus relatos" |
| [10](#fase-10) | jun/26 | Meta-IA + entrega | Helper self-docs, AiBadge, Docker/Railway |

🟡 [§2 Fases detalhadas (cada uma com fontes)](#2-fases-detalhadas)

<!--
RELATÓRIO. Cada linha é clicável e leva à narrativa detalhada da fase, que por sua
vez aponta para os artefatos originais. As fases 0–6 são a gênese (repo-pai); 7–10
são a construção do produto a entregar (submódulo fala-gavea).
-->

---

## Evidência que ancora o escopo

**Diagnóstico GaveaLab 2023 (FAPERJ Nº 20/2022)** — campo jun–nov/2023, **380 entrevistados** (Gávea-asfalto, Rocinha, Parque da Cidade).

- **MFLA:** SEGURANÇA (24%) e EDUCAÇÃO (22%) = temas alavancadores no "asfalto".
- Segurança = maior dor (20% asfalto · 9% favelas).
- **Divergência decisiva:** asfalto → *mais polícia*; favela → *garantia de direitos e ausência de violência policial*.

→ Justifica capturar a **multiplicidade de vozes sobre o mesmo território**.

🔴 [Diagnóstico FAPERJ (PDF)](../../../knowledge/Strategic%20Design%204%20Smart%20City%20Lab%20_Gavea%20Lab%20diagnostico_onepage.pdf) · 🔴 [Reuniões de stakeholders (PDF)](../../../knowledge/Reunioes-stakeholders-1-2.pdf)

<!--
RELATÓRIO. Coordenação: Prof. Carlo Franzato, Prof. Cláudio Freitas de Magalhães,
com Fabienne Torres Schiavo (Doutora em Design, CAPES) — a stakeholder que validou
o caso de uso real e nos encaminhou o desafio (Projeto 08).
-->

---

## Projeto 08 — o desafio da Fabiene ⭐

Após apresentarmos a **1ª encarnação do fala-gávea**, a pesquisadora **Fabienne Torres Schiavo** validou a relevância e nos encaminhou o desafio do GaveaLab (texto copiado em [research-000074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md)):

> **PROJETO 08 — Mapa Colaborativo de Dados para Segurança e Planejamento do Bairro.**
> *Desafio: Como transformar dados públicos e colaborativos (Censo, mapas afetivos) em ferramentas úteis para o planejamento do bairro?* Reúne, em um mapa colaborativo, iluminação, áreas percebidas como inseguras, circulação, problemas urbanos, equipamentos e percepções dos moradores — de fontes públicas (Censo, bases oficiais) e de contribuições da população. Tem **dimensão educativa**: formar jovens e moradores para coletar, interpretar e usar dados locais.

🟡 *retorno à camada geoespacial do Atlas, agora em escala de bairro.*
🔴 [research-000074 (texto + arquitetura de camadas)](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md)

> 🔒 **Autorização:** confirmar com a Fabiene antes de reproduzir este texto na entrega pública. (Projeto 06 ainda a recuperar — ver notas.)

<!--
RELATÓRIO. Este é o "texto copiado" que faltava na v2. Ele fecha a Fase 4: o Projeto 08
é exatamente a camada geoespacial colaborativa que reconecta o produto à origem (Atlas).
Pedir à Fabiene autorização para citar o enunciado oficial e o documento de validação.
-->

---

## Os dois casos de uso

**CU1 — Cidadão** ([Casos_de_uso_2](../../../knowledge/Casos_de_uso_10-06-2026_2.md))
> *"Um poste da minha rua está apagado. Tiro uma foto, envio a localização do GPS, escrevo uma mensagem — e tudo vai para uma base pública."*
Registra **e acompanha** a demanda; outros moradores **confirmam com um clique**.

**CU2 — Agente público** ([Casos_de_uso_1](../../../knowledge/Casos_de_uso_10-06-2026_1.md))
> *"Filtro demandas, seleciono as semelhantes/repetidas e crio um encaminhamento para um órgão, com status e solução proposta."*
IA assiste a exploração: busca semântica, relatos similares, chat.

🔴 [CENÁRIOS de agentes públicos (seed)](../../../knowledge/CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt) · 🔴 [RELATOS de cidadãos (seed)](../../../knowledge/RELATOS_HERBERT.txt)

<!--
RELATÓRIO. Conformidade LGPD e alinhamento ao PL 2338 (Marco Regulatório da IA)
constam dos documentos formais da disciplina. Os dois CUs são exatamente o que o
produto implementa hoje.
-->

---

## O produto hoje — `fala-gavea`

**SPA React + API FastAPI (clean architecture), IA local.**

- **Backend:** Python 3.13 · FastAPI · SQLAlchemy/SQLite · JWT (citizen/agent/admin)
- **Frontend:** React 18 · Vite · TypeScript · Tailwind · react-leaflet
- **IA local:** ChromaDB + sentence-transformers · Ollama (`qwen3:8b`)
- **Entrega:** Docker + Railway · seed showcase (CSV 200/5k)

🟡 [§5 Stack consolidada](#anexo-b--stack-tecnologica) · 🔴 [README](../../../fala-gavea/README.md) · 🔴 [CLAUDE.md](../../../fala-gavea/CLAUDE.md)

<!--
RELATÓRIO. O produto está executável localmente (API + SPA com hot-reload), via Docker
e publicável no Railway. Tem auth por roles, busca semântica, chat NL, votos/comentários
e um assistente que documenta o próprio sistema.
-->

---

## Demo (fluxo a apresentar)

1. **Cidadão** registra relato → foto + GPS + texto.
2. Relato aparece no **mapa Leaflet** (GeoJSON).
3. **Agente** explora: filtros, **busca semântica**, **chat NL**, relatos similares.
4. Agente **agrega** relatos e cria **encaminhamento** (órgão + status + solução).
5. Cidadão **vota/comenta** e **acompanha** ("meus relatos").

> 🎯 **Amanhã:** demo **populado a partir do Projeto 08** (mapa colaborativo) via `make seed` (showcase).

🔴 [fg:plan-000183 — seed showcase](../../../fala-gavea/_output/plans/plan-000183-local-showcase-seed-pipeline.md)

<!--
RELATÓRIO. O seed showcase popula usuários, relatos, encaminhamentos, votos, comentários,
filtros salvos e ciclo de vida — exatamente o necessário para uma demo completa.
A camada de dados do Projeto 08 (IBGE/data.rio/OSM + percepção) é o próximo passo de demo.
-->

---

## IA no produto

**Human-in-the-loop, local e auditável.**

- Categorização/sugestão de relatos · clustering (embeddings + UMAP/BERTopic)
- Busca semântica (ChromaDB) · relatos similares · chat NL → filtros de API · chat RAG
- **Feedback loop few-shot:** o agente confirma/corrige; a correção alimenta o prompt (sem fine-tuning).
- **AiBadge:** todo conteúdo gerado por IA é marcado na UI (proveniência).

🔴 [fg:plan-000100 — chat RAG](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md) · 🔴 [roadmap-000070 — feedback loop](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md)

<!--
RELATÓRIO. Andrey definiu o papel da IA nas reuniões: "não como curador principal,
mas auxiliador na curadoria". O feedback loop few-shot é o ponto teoricamente mais
relevante: aprendizado barato, auditável e com humano no comando.
-->

---

## Meta: o sistema explica a si mesmo

`POST /nl/help` — assistente que responde perguntas **sobre a própria plataforma**, a partir da documentação do projeto indexada no ChromaDB (RAG self-docs).

- Para o **admin**: enquadramento "meta" ciente do **SEJA** (taxonomia/SDLC) — decisão **D-017**.
- A plataforma passa a ser **auto-documentada** para diferentes perfis.

🔴 [fg:plan-000177 — helper self-docs](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md) · 🔴 [fg:plan-000181 — SEJA no helper](../../../fala-gavea/_output/plans/plan-000181-embed-seja-methodology-platform-helper.md)

<!--
RELATÓRIO. Esta camada conecta os dois eixos de IA: o produto usa IA, e o produto
explica como foi construído com IA. É um diferencial para a disciplina de AI Systems Design.
-->

---

## IA no processo (o método como resultado)

O projeto inteiro foi construído sob o harness **SEJA** sobre **Claude Code**:
`/research → /plan → /implement → /check → /document | /communicate → /reflect`.

- **Rastro auditável:** centenas de artefatos numerados (planos, roadmaps, reflexões, QA, comunicações, telemetria) + histórico de commits.
- Permite reconstruir **o quê, como e por quê** de cada inflexão de escopo.

🟡 [Anexo C — Corpus SEJA](#anexo-c--o-corpus-de-desenvolvimento)

<!--
RELATÓRIO. Para "AI Systems Design", o corpus de desenvolvimento É um objeto de estudo:
um registro completo da cadeia pesquisa → decisão → plano → implementação → verificação
→ comunicação. O submódulo fala-gavea tem seu próprio harness (planos até 000183,
17 decisões D-NNN, 4 comunicações por público).
-->

---

## Base de conhecimento (KB)

A KB do projeto = **3 fontes** consultáveis por RAG (kb-qa / ChromaDB):

1. 🟢 **Este documento (077)** — índice vivo da trajetória.
2. 🟡 **Artefatos SEJA** — repo-pai + submódulo `fala-gavea`.
3. 🔴 **Pasta compartilhada (Dropbox)** — diagnósticos, atas, documentos institucionais → ingerir em `knowledge/`.

➡️ Ver [Anexo D](#anexo-d--base-de-conhecimento-kb) para o processo de ingestão.

<!--
RELATÓRIO. A pasta do Dropbox deve ser baixada para knowledge/ (ou um subdiretório) e
ingerida via `uv run kb-qa ingest`, passando a alimentar tanto o kb-qa (sessões de IA)
quanto o helper self-docs do fala-gavea. Assim o conteúdo do Dropbox "soma" com este deck.
-->

---

## Governança de dados (pendências) 🔒

| Item | Situação | Ação |
|---|---|---|
| Texto do **Projeto 08** ([research-074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md)) | copiado | **pedir autorização da Fabiene** para citar |
| **Dump do WhatsApp** da equipe ([arquivo](../../../knowledge/dump-grupo-wpp-24-05-2026.txt)) | no repo | **autorização de TODOS os membros** antes de tornar público |
| Diagnóstico FAPERJ / docs do GaveaLab | de terceiros | citar com crédito; confirmar permissão de redistribuição |
| Coordenadas de relatos | PII potencial | truncar lat/lon (privacidade) — [research-074 R3](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md) |

**Princípios:** soberania de dados (IA local) · LGPD · PL 2338.

<!--
RELATÓRIO. Ver a resposta detalhada sobre o dump do WhatsApp no Anexo E. Regra geral:
nada de terceiros (Fabiene, GaveaLab) ou da equipe vira documentação pública sem
consentimento explícito e registrado.
-->

---

## Próximos passos

1. 🎬 **Amanhã:** apresentar a **demo populada a partir do Projeto 08** (`make seed` showcase) — mapa + relatos + encaminhamentos.
2. 📨 **Feedback da Fabiene:** enviar link/vídeo do demo atual + roteiro de 5 perguntas (ver [Anexo F](#anexo-f--roteiro-de-feedback-fabiene)); pedir autorização para citar o Projeto 08 e o documento de validação.
3. ✅ **Autorizações:** coletar OK de todos os membros sobre o dump do WhatsApp; do GaveaLab sobre o diagnóstico.
4. 📥 **Dropbox → KB:** baixar a pasta compartilhada para `knowledge/` e rodar `kb-qa ingest`.
5. 🗺️ **Projeto 08 (técnico):** camadas IBGE/data.rio/OSM + percepção — [research-074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md).

<!--
RELATÓRIO. Os passos 1–2 são para amanhã. 3–4 destravam o uso pleno da KB. 5 é a
evolução técnica que materializa o Projeto 08 e fecha o ciclo de volta ao Atlas.
-->

---

## Fechamento

> O mérito não está em ter chegado ao escopo inicial, e sim em ter feito o **caminho inverso de forma deliberada e documentada**.

Os dois invariantes que sobreviveram a todas as fases — **camada geoespacial** e **soberania de dados local** — são exatamente os que ligam o produto final (fala-gávea) à sua origem amazônica (o Atlas).

**Obrigado.** · `communication-000077` · [Anexos →](#anexos-relatorio-detalhado)

<!--
RELATÓRIO. Encerramento da apresentação. A partir daqui seguem os ANEXOS: as fases
detalhadas, tabelas (stack, decisões, casos de uso→protótipo), o corpus SEJA, a KB,
a resposta sobre o WhatsApp, o roteiro de feedback e o índice de fontes originais.
Em uma apresentação Marp, funcionam como "slides de backup". Lidos como documento,
são o relatório técnico completo.
-->

---

# Anexos (relatório detalhado)

> Camada 🟡/🔴 — a profundidade técnica do documento. Cada item aponta para os arquivos originais (documento vivo).

---

## 2. Fases detalhadas

<a id="fase-0"></a>
### Fase 0 — Origem: Atlas da Amazônia (abr/2026)
Atlas Digital Georreferenciado da Amazônia assistido por IA. Protótipo: **kb-qa** (RAG local — ChromaDB + sentence-transformers + MCP). Arquitetura em camadas (RAG textual + engine geoespacial + `render_map`), LLM local-ou-nuvem, serviço dual MCP+REST. Princípios CARE/OCAP → invariante "inferência local".
🔴 [Reuniao-23-04-2026.md](../../../knowledge/Reuniao-23-04-2026.md)

<a id="fase-1"></a>
### Fase 1 — Casos de uso e participação cidadã (mai/2026)
Síntese de plataformas (Decidim, Pol.is, Talk to the City, Consul, vTaiwan). Convergência para **T3C** local; PoC TRL3 com Docker + Ollama. Três casos seminais (cidadão / gestor / GaveaLab).
🔴 [casos-de-uso.md](../../../knowledge/casos-de-uso.md) · [Reunioes-stakeholders-1-2.pdf](../../../knowledge/Reunioes-stakeholders-1-2.pdf) · [plan-000001](../../plans/plan-000001-trl3-poc-tttc-local-ollama.md)

<a id="fase-2"></a>
### Fase 2 — GaveaLab PoC: análise textual (jun/2026)
Streamlit + SQLite + Ollama: **upload → temas → claims → categorização manual → cruxes → UMAP**. CU01 formal (tríade sistêmica; LGPD; PL 2338).
🔴 [Casos_de_uso_1](../../../knowledge/Casos_de_uso_10-06-2026_1.md) · [plan-000008](../../plans/plan-000008-gavealab-poc-scaffold.md) · [plan-000016](../../plans/plan-000016-gavealab-poc-umap-visualization.md)

<a id="fase-3"></a>
### Fase 3 — fala-gávea, 1ª encarnação (jun/2026)
Backend FastAPI (`CitizenPost`, likes, label feedback) + Streamlit (4 páginas) + seed 1000 relatos. CU "cidadão registra e acompanha" (texto/voz/foto; validação coletiva).
🔴 [Casos_de_uso_2](../../../knowledge/Casos_de_uso_10-06-2026_2.md) · [reflection-000037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md) · [plan-000027](../../plans/plan-000027-fala-gavea-setup-streamlit.md)

<a id="fase-4"></a>
### Fase 4 — Zoom in para a Gávea (15/jun/2026) ⭐
Decisão-chave: um bairro, uma vertical (segurança), dois personas. **Reunião com a Fabiene** após apresentar a 1ª encarnação → ela validou o caso real e encaminhou o **Projeto 08** (e, conforme conversado, o Projeto 06 — *texto a recuperar/confirmar*). Insight: *o clustering já construído É o motor do caso de uso do agente*; o mapa é uma nova camada, não um novo projeto.
🔴 [reflection-000052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md) · [research-000074 (Projeto 08)](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md) · [Diagnóstico FAPERJ](../../../knowledge/Strategic%20Design%204%20Smart%20City%20Lab%20_Gavea%20Lab%20diagnostico_onepage.pdf)

> 🔒 Projeto 06: não localizei o enunciado oficial no repositório (o dump do WhatsApp disponível, de 24/05, antecede a reunião). Cole o texto aqui para fechar a citação.

<a id="fase-5"></a>
### Fase 5 — Busca inteligente + canal comunitário (jun/2026)
Chat NL **intent-to-filter**. Reflexão detecta a lacuna do **feedback loop** (correções do agente não viravam sinal de treino). Roadmap do "Waze comunitário": `CategoryCurationEvent` append-only, few-shot, clustering reaproveitando embeddings, urgência, encaminhamento.
🔴 [reflection-000069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md) · [roadmap-000070](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md) · [plan-000068](../../plans/plan-000068-chat-nl-intent-to-filter.md)

<a id="fase-6"></a>
### Fase 6 — Reescrita em clean architecture (jun/2026)
Reescrita FastAPI + SQLAlchemy + Pydantic v2 + pytest; `fala-gavea` vira **submódulo com harness SEJA próprio**. CU1/CU2 consolidados. Entidades: `User`, `ReportType` (dinâmico), `Report`, `Forwarding`.
🔴 [roadmap-000071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md) · [plan-000072](../../plans/plan-000072-fala-gavea-scaffold-e-seja-setup.md) · [check-000073](../../check-logs/check-000073-validate-fala-gavea-scaffold.md)

<a id="fase-7"></a>
### Fase 7 — Produto MVP: domínio, auth e SPA (jun/2026)
Auth JWT (roles) + Reports + ReportType CRUD + Forwarding (agregação N relatos) + **SPA React** (mapa, formulário c/ geolocalização, painel do agente, login).
🔴 [fg:plan-000073](../../../fala-gavea/_output/plans/plan-000073-feature-b-wave-0-item-1-domain-auth-reports.md) · [fg:plan-000082 (SPA)](../../../fala-gavea/_output/plans/plan-000082-feature-f-wave-1-item-4-frontend-spa-react.md)

<a id="fase-8"></a>
### Fase 8 — Camada de IA (jun/2026)
Infra de embeddings + ingestão; busca semântica + relatos similares; BERTopic; **chat NL RAG**; sugestão plugável de tópicos (humano no comando).
🔴 [fg:plan-000094 (busca)](../../../fala-gavea/_output/plans/plan-000094-semantic-search-similar-reports-wave1.md) · [fg:plan-000100 (RAG chat)](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md) · [fg:plan-000174 (sugestão)](../../../fala-gavea/_output/plans/plan-000174-pluggable-report-type-suggestion.md)

<a id="fase-9"></a>
### Fase 9 — Participação cidadã e transparência (jun/2026)
Votos + comentários + relato anônimo; "meus relatos" + "meus encaminhamentos"; filtros salvos; workspace grid cross-filter; "cesta de relatos".
🔴 [fg:roadmap-000151](../../../fala-gavea/_output/roadmaps/roadmap-000151-citizen-feedback-votes-comments-anonymization.md) · [fg:plan-000152](../../../fala-gavea/_output/plans/plan-000152-db-schema-votes-comments-anon-tokens.md) · [fg:plan-000164](../../../fala-gavea/_output/plans/plan-000164-meus-relatos-nav-inline-votes-sort.md)

<a id="fase-10"></a>
### Fase 10 — Meta-IA e empacotamento (jun/2026, atual)
Helper self-docs SEJA-aware (D-017); **AiBadge** de proveniência (D-015); síntese de comentários; Docker + Railway; seed showcase; docs para 4 públicos.
🔴 [fg:plan-000177 (helper)](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md) · [fg:plan-000178 (AiBadge)](../../../fala-gavea/_output/plans/plan-000178-aibadge-provenance-marker.md) · [fg:plan-000183 (seed)](../../../fala-gavea/_output/plans/plan-000183-local-showcase-seed-pipeline.md)

---

## Anexo A — Casos de uso → protótipos

| Caso de uso (origem) | Concepção | Protótipo intermediário | Implementação final |
|---|---|---|---|
| Cidadão registra e acompanha | [3](#fase-3)–[4](#fase-4) | CitizenPost + likes (Streamlit) | `POST /reports` + "meus relatos" + votos ([7](#fase-7),[9](#fase-9)) |
| Gestor consulta p/ decisão | [1](#fase-1)–[2](#fase-2) | Pipeline temas→claims→cruxes | Painel agente + busca + chat NL ([7](#fase-7)–[8](#fase-8)) |
| Validação coletiva (1 clique) | [3](#fase-3) | likes/label feedback | Votos + comentários ([9](#fase-9)) |
| Encaminhamento institucional | [5](#fase-5)–[6](#fase-6) | — | `Forwarding` many-to-many + status ([7](#fase-7)) |
| IA categoriza c/ curadoria | [1](#fase-1),[5](#fase-5) | `auto_categorize`+`PATCH /category` | Sugestão plugável + AiBadge ([8](#fase-8),[10](#fase-10)) |
| Busca em linguagem natural | [5](#fase-5) | intent-to-filter | NL parser + chat RAG ([8](#fase-8)) |
| **Camada geoespacial (Projeto 08)** | [0](#fase-0) | `render_map` | Mapa Leaflet + GeoJSON; atlas territorial ([research-074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md)) |
| Plataforma se explica | [1](#fase-1) | — | Helper RAG self-docs ([10](#fase-10)) |

---

## Anexo B — Stack tecnológica

| Camada | Gênese (F0–F5) | Produto entregue (F6–F10) |
|---|---|---|
| Linguagem / gestão | Python 3.13 + uv | Python 3.13 + uv |
| Web / API | Streamlit | **FastAPI** (clean architecture) |
| Frontend | Streamlit pages | **React 18 + Vite + TS + Tailwind + react-leaflet** |
| Persistência | SQLite (`GaveaLabWorkspace`) | SQLite via **SQLAlchemy** |
| Auth | nenhuma (local) | **JWT (PyJWT+bcrypt)** roles citizen/agent/admin |
| Embeddings | ChromaDB + sentence-transformers | idem (multilingual-e5 / nomic) |
| LLM local | Ollama (qwen) | **Ollama** (`qwen3:8b`) + provider plugável |
| Visualização | UMAP + HDBSCAN + Plotly | Leaflet + GeoJSON; BERTopic |
| Entrega | — | **Docker + Railway**; seed showcase |
| Qualidade | pytest, ruff, pyright | + **Vitest/RTL** |

**Decisões de maior peso:** inferência local (CARE/OCAP→Ollama) · zoom in Atlas→Gávea · few-shot em vez de fine-tuning · `CategoryCurationEvent` append-only · clean architecture + submódulo SEJA · `ReportType` dinâmico · AiBadge (D-015) · helper SEJA-aware (D-017). 🔴 [decisões do fala-gavea](../../../fala-gavea/product-design/project/product-design-as-intended.md)

---

## Anexo C — O corpus de desenvolvimento

- **Repo-pai (`inf2921-grupo-c`):** planos 000001–000077; reflexões [037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md)/[052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md)/[069](../../reflections/reflection-000069-gavealab-feedback-loop-categorizacao.md); roadmaps 000007–000071; comunicação [000075](../2026-06-19/communication-000075-academics.md).
- **Submódulo (`fala-gavea`):** harness SEJA próprio — planos até **000183**, 4 roadmaps, 11 reflexões, **17 decisões D-NNN**, 4 comunicações ([125](../../../fala-gavea/docs/communication-000125-evaluators.md)–[128](../../../fala-gavea/docs/communication-000128-academics.md)).
- Cada artefato é numerado, datado e rastreável a um commit: cadeia *pesquisa → decisão → plano → implementação → verificação → comunicação*.

---

## Anexo D — Base de conhecimento (KB)

**Objetivo:** unificar este deck + os artefatos SEJA + a **pasta do Dropbox** numa KB consultável por RAG.

**Como integrar o Dropbox:**
1. Baixar a pasta compartilhada para `knowledge/` (ou `knowledge/dropbox/`).
2. Conferir formatos suportados (`.md`, `.pdf`) — converter `.docx`/`.pptx` para PDF se necessário.
3. Rodar `uv run kb-qa ingest` (repo-pai) → indexa em ChromaDB; consultável via `query_knowledge` (MCP) nas sessões de IA.
4. No produto, `scripts/reindex_selfdocs.py` (fala-gavea) indexa a documentação para o **helper `/nl/help`**.
5. Registrar a proveniência de cada documento (autor, permissão de uso) — ver [Anexo E](#anexo-e--dump-do-whatsapp-como-documentacao-publica).

> Assim, o conteúdo do Dropbox "soma" com este documento: vira contexto recuperável tanto no kb-qa quanto no assistente da plataforma.

---

## Anexo E — Dump do WhatsApp como documentação pública?

**Pergunta:** *podemos usar o dump das conversas do WhatsApp como documentação pública na disciplina?*

**Resposta curta:** sim, com valor real como evidência de processo — **mas só após (1) consentimento explícito de todos os participantes e (2) anonimização/curadoria**. Não publicar o dump bruto.

**Por quê / como:**
- **Consentimento (LGPD):** mensagens privadas contêm dados pessoais. Cada participante (Andrey, Mauro, Julia, Herbert, Natali, Sheila) precisa autorizar por escrito o uso do conteúdo na entrega. Terceiros mencionados também (ex.: Fabiene) → pedir OK ou remover/anonimizar.
- **Curadoria, não dump bruto:** o valor acadêmico está nos **trechos que mostram decisões de design** (ex.: "clusteriza, analisa com IA… mostra dashboard"; "IA como auxiliadora da curadoria"). Extrair citações datadas e atribuídas, não o log inteiro.
- **Minimização:** remover telefones, endereços, dados de saúde, assuntos pessoais não relacionados ao projeto. O dump atual já contém conteúdo sensível (ex.: saúde mental, moradia) — **não** deve ir para um anexo público.
- **Formato sugerido:** um apêndice "Excertos de conversas da equipe (com autorização)" com data, autor (ou inicial), citação e a decisão que ela embasou. Vincular a reflexões/decisões SEJA correspondentes.
- **Soberania de dados:** coerente com o princípio do projeto — só publicamos o que foi consentido.

🔴 [dump-grupo-wpp-24-05-2026.txt](../../../knowledge/dump-grupo-wpp-24-05-2026.txt) (uso interno até autorização)

---

## Anexo F — Roteiro de feedback (Fabiene)

**Objetivo:** validar o demo atual e destravar autorizações.

**Mensagem (rascunho):** *"Fabienne, evoluímos o fala-gávea a partir do seu encaminhamento (Projeto 08). Segue um demo de 3 min [link]. Poderia nos dar um retorno e autorizar citarmos o enunciado do Projeto 08 e seu documento de validação na entrega da disciplina?"*

**5 perguntas para o feedback:**
1. O fluxo cidadão→agente reflete a necessidade real do território?
2. As categorias/tópicos de segurança fazem sentido para a Gávea/Rocinha?
3. O mapa colaborativo (Projeto 08) endereça o desafio que vocês formularam?
4. Há sensibilidades de dados/representação a respeitar (favela × asfalto)?
5. Podemos citar o Projeto 08 e anexar seu documento de validação?

**Anexos a pedir:** enunciado oficial dos Projetos 06 e 08; documento de validação do caso de uso real.

---

## Anexo G — Índice de fontes originais (documento vivo)

**Knowledge (`knowledge/`):** [Reuniao-23-04-2026.md](../../../knowledge/Reuniao-23-04-2026.md) · [casos-de-uso.md](../../../knowledge/casos-de-uso.md) · [Casos_de_uso_1](../../../knowledge/Casos_de_uso_10-06-2026_1.md) · [Casos_de_uso_2](../../../knowledge/Casos_de_uso_10-06-2026_2.md) · [Reunioes-stakeholders-1-2.pdf](../../../knowledge/Reunioes-stakeholders-1-2.pdf) · [Diagnóstico FAPERJ (PDF)](../../../knowledge/Strategic%20Design%204%20Smart%20City%20Lab%20_Gavea%20Lab%20diagnostico_onepage.pdf) · [CENARIOS…HERBERT.txt](../../../knowledge/CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt) · [RELATOS_HERBERT.txt](../../../knowledge/RELATOS_HERBERT.txt) · [dump-wpp](../../../knowledge/dump-grupo-wpp-24-05-2026.txt)

**SEJA repo-pai (`_output/`):** [research-074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md) · [check-073](../../check-logs/check-000073-validate-fala-gavea-scaffold.md) · [roadmap-070](../../roadmaps/roadmap-000070-canal-digital-comunitario-seguranca-urbana.md) · [roadmap-071](../../roadmaps/roadmap-000071-gavea-seguranca-demandas-app.md) · [reflection-052](../../reflections/reflection-000052-atlas-da-amazonia-zoom-in-gavea.md) · [comm-075](../2026-06-19/communication-000075-academics.md)

**Produto (`fala-gavea/`):** [README](../../../fala-gavea/README.md) · [CLAUDE.md](../../../fala-gavea/CLAUDE.md) · [plan-073](../../../fala-gavea/_output/plans/plan-000073-feature-b-wave-0-item-1-domain-auth-reports.md) · [plan-082 SPA](../../../fala-gavea/_output/plans/plan-000082-feature-f-wave-1-item-4-frontend-spa-react.md) · [plan-100 RAG](../../../fala-gavea/_output/plans/plan-000100-rag-chat-nl-assistant.md) · [plan-177 helper](../../../fala-gavea/_output/plans/plan-000177-chat-helper-plataforma-rag-self-docs.md) · [plan-183 seed](../../../fala-gavea/_output/plans/plan-000183-local-showcase-seed-pipeline.md) · docs: [125](../../../fala-gavea/docs/communication-000125-evaluators.md)/[126](../../../fala-gavea/docs/communication-000126-clients.md)/[127](../../../fala-gavea/docs/communication-000127-end-users.md)/[128](../../../fala-gavea/docs/communication-000128-academics.md)

> ⚠️ Links de `fala-gavea/` requerem o submódulo populado (`git submodule update --init`). PDFs abrem a partir do `.html` aberto localmente.
