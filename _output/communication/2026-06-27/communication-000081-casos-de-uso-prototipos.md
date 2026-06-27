# Casos de uso e provas de conceito por protótipo

**Material de apoio para o relatório final** · INF2921/CIS2114 (AI Systems Design, PUC-Rio, 2026.1)
**Equipe:** Andrey · Mauro · Julia · Herbert · Natali · Sheila
**Data:** 27/06/2026 · `communication-000081`
**Referência-mãe:** [communication-000077 — timeline do projeto](../2026-06-26/communication-000077-timeline-projeto.md)

> **Para que serve este documento.** É um *scaffold de fontes* para você escrever, com suas próprias palavras, a seção do relatório dedicada aos **casos de uso** e às **provas de conceito (PoCs)** de cada protótipo. Cada fase reúne: (1) o protótipo daquela etapa, (2) **2–3 casos de uso** levantados/formalizados, e (3) os **links de fonte in-place** (🔴) para os artefatos originais — para que cada afirmação do relatório seja rastreável. O texto aqui é deliberadamente enxuto: a redação final é sua.

**Legenda de profundidade (mesma de [077](../2026-06-26/communication-000077-timeline-projeto.md)):** 🟢 visão geral · 🟡 artefato SEJA (plano/reflexão/research) · 🔴 fonte original (`.md`, `.pdf`, código).

---

## Fase 0 — Origem: Atlas da Amazônia · protótipo **kb-qa** (abr/2026)

**Protótipo (PoC):** **kb-qa** — RAG local (ChromaDB + sentence-transformers + MCP). Recuperação de trechos de documentos para ancorar respostas de IA, com inferência 100% local.

**Intenção futura (não implementada):** arquitetura em camadas (RAG textual + *engine* geoespacial + `render_map`), LLM local-ou-nuvem, serviço dual MCP+REST. Princípios **CARE/OCAP** → invariante **"inferência local"**.

**Casos de uso (eixos do Atlas Digital Georreferenciado da Amazônia):**

- **UC-0.1 — Acesso curado a informação georreferenciada.** *Problema:* acesso controlado e curado a informação **multimodal referenciada geograficamente** (datazoom.amazônia, Nova Cartografia Social da Amazônia). *Produto:* atlas digital iterativo assistido por IA para buscar informação **armazenada, mantida e curada por uma comunidade**.
- **UC-0.2 — Segurança pública territorial.** Vigilância (uso de câmeras), **mapeamento de espaços, territórios e fluxos**, revitalização de espaços de menor fluxo.
- **UC-0.3 — Educação.** Eixo nomeado na concepção inicial (sem detalhamento).

> 🔎 *Nota de continuidade:* a **camada geoespacial** e a **soberania de dados (IA local)** nascem aqui e sobrevivem a todas as fases — são os dois invariantes do projeto.

🔴 [Reuniao-23-04-2026.md](../../../knowledge/Reuniao-23-04-2026.md) · 🟡 [077 §Fase 0](../2026-06-26/communication-000077-timeline-projeto.md#fase-0)

---

## Fase 1 — Casos de uso e participação cidadã · PoC **Talk to the City local** (mai/2026)

**Protótipo (PoC):** estudo comparativo de plataformas de participação cidadã (**Decidim, Pol.is, Talk to the City, Consul, vTaiwan**) → convergência para **Talk to the City local**; PoC em **TRL3 com Docker + Ollama**.

**Casos de uso (três casos seminais, levantados após reunião com stakeholders):**

- **UC-1.1 — Cidadão.** "Como **cidadão**, quero um espaço virtual para discutir problemas e ideias a respeito do meu território."
- **UC-1.2 — Gestor / Investidor.** "Como **investidor / gestor público**, quero conhecer os problemas de um território para tomar decisões embasadas nas necessidades do cidadão."
- **UC-1.3 — GaveaLab.** "Como **GaveaLab**, quero uma ferramenta que ajude a coletar e sintetizar pesquisas com cidadãos, democratizar o acesso à informação e consolidar perfis e necessidades."

🔴 [casos-de-uso.md](../../../knowledge/casos-de-uso.md) · 🔴 [Reunioes-stakeholders-1-2.pdf](../../../knowledge/Reunioes-stakeholders-1-2.pdf) · 🟡 [plan-000001 (PoC TRL3 TTTC local)](../../plans/plan-000001-trl3-poc-tttc-local-ollama.md)

---

## Fase 2 — GaveaLab PoC: análise textual · PoC **Streamlit + SQLite + Ollama** (jun/2026)

**Protótipo (PoC):** **Streamlit + SQLite + Ollama**, stack simplificada. Pipeline: **upload → temas → reivindicações (claims) → categorização manual → reivindicações contraditórias (cruxes) → clusterização com UMAP**. Mantém os casos de uso da Fase 1, agora **formalizados** sobre a **tríade sistêmica** (relatos cidadãos + perguntas dos decisores + ferramentas de IA com validação humana), com **LGPD** e **PL 2338**.

**Casos de uso (formalizados):**

- **UC-2.1 — CU01: Consulta para tomada de decisão** (*Ator: Gestor Público / Investidor*). Visão estruturada e segmentada das reivindicações. *Fluxo:* dashboard por território (Rocinha / Gávea-asfalto / Parque da Cidade) → painel de **clusters temáticos** (segurança, mobilidade, saúde, educação) → filtros por tema/urgência → aprofundamento em relatos representativos e **opiniões divergentes** → **exporta relatório** para embasar política/investimento. *Ética:* anonimização (LGPD); segmentação obrigatória **asfalto × favela** para evitar médias enganosas.
- **UC-2.2 — CU02: Coleta, Síntese e Gestão da Base de Conhecimento** (*Ator: GaveaLab*). *Fluxo:* upload de CSV → normalização (texto + metadados origem/data/território) → pipeline de IA (extrai claims → agrupa em tópicos/subtópicos → identifica opiniões divergentes) → **revisão humana** (valida/edita títulos, move claims) → consolida versão aprovada no dashboard (alimenta o CU01). *Fluxo alternativo:* coleta por **áudio** (transcrição speech-to-text; áudio original descartado para anonimato). *Ética:* **validação humana obrigatória** antes de publicar qualquer síntese de IA.

🔴 [Casos_de_uso_1 (CU01 + CU02 formais)](../../../knowledge/Casos_de_uso_10-06-2026_1.md) · 🟡 [plan-000008 (scaffold PoC)](../../plans/plan-000008-gavealab-poc-scaffold.md) · 🟡 [plan-000016 (UMAP)](../../plans/plan-000016-gavealab-poc-umap-visualization.md)

---

## Fase 3 — fala-gávea, 1ª encarnação · PoC **FastAPI + Streamlit "Twitter-like"** (jun/2026)

**Protótipo (PoC):** protótipo **"Twitter-like"** — usuários **postam relatos** com opção de **like**; o sistema **clusteriza e cria tópicos**. Backend **FastAPI** (`CitizenPost`, likes, *label feedback*) + **Streamlit** (4 páginas) + **seed de 1000 relatos**.

**Casos de uso (versão de campo, centrada no território da Gávea/Rocinha/Parque da Cidade):**

- **UC-3.1 — CU01: Morador registra e acompanha uma demanda local** (*Ator: cidadão · canal: app móvel ou tótem físico*). *Contexto exemplo:* iluminação pública apagada há três semanas na entrada da Rocinha. *Fluxo:* acesso inclusivo (suporte offline básico) → **registro simplificado** por texto/voz/foto, IA **categoriza, infere localização e sugere prioridade** com base em relatos similares → **validação coletiva** (outros moradores confirmam com 1 clique) → triagem e encaminhamento ao órgão com prazo → **acompanhamento** com notificações; reabertura sem resolução vira **métrica de abandono institucional**.
- **UC-3.2 — CU02: Agente público analisa demandas e formula intervenção baseada em dados** (*Ator: agente de decisão · canal: painel web*). *Fluxo:* **visão territorial** (mapa de calor por micro-área, asfalto × comunidade; filtros por tema/período/urgência) → **análise qualitativa com IA** (resumo narrativo com nuances que a média estatística esconde) → **priorização colaborativa** (lideranças comunitárias auditam a lista da IA) → **formulação da intervenção** com referências diretas aos relatos → **monitoramento de impacto** pós-intervenção.

🔴 [Casos_de_uso_2 (CU01 cidadão + CU02 agente)](../../../knowledge/Casos_de_uso_10-06-2026_2.md) · 🟡 [reflection-000037 (pipeline de análise faltante)](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md) · 🟡 [plan-000027 (setup Streamlit)](../../plans/plan-000027-fala-gavea-setup-streamlit.md)

---

## Fase 4 — Novo fala-gávea: relatos georreferenciados · produto **clean architecture** (jun/2026)

**Protótipo (produto):** após a reunião com a **Fabiene** (acesso aos **Projetos 06 e 8** do GaveaLab), novo protótipo: o **cidadão envia relatos georreferenciados**; o app ajuda **agentes públicos** a **categorizar, clusterizar e encaminhar demandas para os órgãos responsáveis**. Retorno explícito à **camada geoespacial** da Fase 0, agora em escala de bairro.

**Casos de uso (os dois CUs consolidados no produto):**

- **UC-4.1 — CU1: Cidadão.** "Um poste da minha rua está apagado. Tiro uma foto, envio a localização do GPS, escrevo uma mensagem — e tudo vai para uma base pública." **Registra e acompanha** a demanda; outros moradores **confirmam com um clique**.
- **UC-4.2 — CU2: Agente público.** "Filtro demandas, seleciono as semelhantes/repetidas e crio um **encaminhamento** para um órgão, com status e solução proposta." A **IA assiste a exploração**: busca semântica, relatos similares, chat em linguagem natural.
- **UC-4.3 — Projeto 08: Mapa colaborativo de dados** (desafio da Fabiene). Reunir, em um **mapa colaborativo**, iluminação, áreas percebidas como inseguras, circulação e percepções dos moradores, a partir de fontes públicas (Censo, bases oficiais) e contribuições da população — com **dimensão educativa**.

🔴 [Casos_de_uso_2 (CU1 cidadão)](../../../knowledge/Casos_de_uso_10-06-2026_2.md) · 🔴 [Casos_de_uso_1 (CU2 agente)](../../../knowledge/Casos_de_uso_10-06-2026_1.md) · 🔴 [CENÁRIOS de agentes públicos (seed)](../../../knowledge/CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt) · 🔴 [RELATOS de cidadãos (seed)](../../../knowledge/RELATOS_HERBERT.txt) · 🟡 [research-000074 (Projeto 08 — camadas geo)](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md)

> 🔒 *Governança:* o enunciado do **Projeto 08** e o documento de validação são de terceiros (Fabiene/GaveaLab) — **pedir autorização** antes de reproduzir na entrega pública (ver [077 §Governança](../2026-06-26/communication-000077-timeline-projeto.md)).

---

## Síntese — caso de uso → protótipo ao longo das fases

Tabela-âncora para o relatório (estende o [Anexo A da 077](../2026-06-26/communication-000077-timeline-projeto.md)):

| Caso de uso (família) | Concepção | Protótipo intermediário | Implementação final |
|---|---|---|---|
| Cidadão registra e acompanha | F1 (UC-1.1) → F3 (UC-3.1) | Post + like (FastAPI/Streamlit) | Relato georreferenciado + "meus relatos" (F4, UC-4.1) |
| Gestor/agente consulta para decidir | F1 (UC-1.2) → F2 (UC-2.1) | Pipeline temas→claims→cruxes (Streamlit) | Painel do agente + busca + chat NL (F4, UC-4.2) |
| GaveaLab coleta e sintetiza | F1 (UC-1.3) → F2 (UC-2.2) | Upload CSV + clusterização + revisão humana | Ingestão + clustering + curadoria humana (F4) |
| Validação coletiva (1 clique) | F3 (UC-3.1) | likes / label feedback | Confirmação coletiva / votos (F4) |
| Encaminhamento institucional | F3 (UC-3.2) | triagem no painel | `Forwarding` órgão + status + solução (F4, UC-4.2) |
| Camada geoespacial | F0 (UC-0.1/0.2) | `render_map` (intenção) | Mapa + relatos georreferenciados; Projeto 08 (F4, UC-4.3) |

---

### Fontes consultadas para este documento

- 🔴 Knowledge: [Reuniao-23-04-2026.md](../../../knowledge/Reuniao-23-04-2026.md) · [casos-de-uso.md](../../../knowledge/casos-de-uso.md) · [Casos_de_uso_1](../../../knowledge/Casos_de_uso_10-06-2026_1.md) · [Casos_de_uso_2](../../../knowledge/Casos_de_uso_10-06-2026_2.md) · [Reunioes-stakeholders-1-2.pdf](../../../knowledge/Reunioes-stakeholders-1-2.pdf) · [CENARIOS…HERBERT.txt](../../../knowledge/CENARIOS_AGENTS_PUBLICOS_TOPICOS_HERBERT.txt) · [RELATOS_HERBERT.txt](../../../knowledge/RELATOS_HERBERT.txt)
- 🟡 SEJA: [communication-000077](../2026-06-26/communication-000077-timeline-projeto.md) · [research-000074](../../research-logs/research-000074-camadas-georeferenciadas-fala-gavea.md) · [reflection-000037](../../reflections/reflection-000037-fala-gavea-missing-analysis-pipeline.md) · planos [000001](../../plans/plan-000001-trl3-poc-tttc-local-ollama.md) / [000008](../../plans/plan-000008-gavealab-poc-scaffold.md) / [000016](../../plans/plan-000016-gavealab-poc-umap-visualization.md) / [000027](../../plans/plan-000027-fala-gavea-setup-streamlit.md)
