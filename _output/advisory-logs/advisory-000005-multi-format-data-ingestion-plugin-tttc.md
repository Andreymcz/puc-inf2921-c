# Advisory 000005 | INF2921 Grupo C | 2026-05-24 01:10 UTC | Plugin de ingestão multi-formato para Talk to the City

tags: data-ingestion, llm-extraction, civic-tech, integration, plugin-architecture

**User brief:** Ideia para perguntar para o stakeholder: LLM especializada em transformar dados de pesquisas armazenados em formatos diversos para o formato de entrada do fork que vamos construir. Pode ser um plugin que permite o stakeholder enviar dados de diversos formatos (fontes) e ser um software que permite uma maior integração de dados de diversas fontes diferentes com diversas tecnologias.

**Agent interpretation:** O T3C espera um CSV simples (`id`, `comment`). Dados de participação cidadã chegam em dezenas de formatos (formulários, planilhas, PDFs, transcrições, APIs). A ideia é um componente intermediário — "adaptador universal" — que usa LLM para identificar campos relevantes e normalizar qualquer fonte para o formato T3C. Este advisory explora a viabilidade, arquitetura, escopo de stakeholder e perguntas a fazer ao GaveaLab.

**Files referenced:** Plan 000001 (Step 4b — embrião do adaptador), advisory-000004 (contexto T3C local).

---

## Q&A Log

### Q1 — Como estruturar um plugin de ingestão multi-formato para o T3C? Qual a viabilidade e o que perguntar ao stakeholder?

#### O problema central

O T3C recebe um CSV com duas colunas: `id` (identificador único) e `comment` (resposta qualitativa). Mas dados de participação cidadã existem em formatos radicalmente diferentes:

| Fonte | Formato | Dificuldade de normalização |
|-------|---------|----------------------------|
| Google Forms / Typeform | CSV/XLSX com colunas variáveis | Baixa — parser determinístico |
| SurveyMonkey / Qualtrics | JSON proprietário ou XLSX exportado | Média — estrutura semântica variável |
| Audiências públicas (atas PDF) | Texto não estruturado por blocos | Alta — requer segmentação semântica |
| WhatsApp / Telegram | JSON de exportação | Média — filtrar por remetente/contexto |
| Entrevistas gravadas | Áudio → transcrição automática | Alta — requer ASR + segmentação |
| APIs de dados abertos (Rio, IBGE) | JSON/GeoJSON | Média — mapeamento de campos |
| Planilhas internas do GaveaLab | XLSX com estrutura ad-hoc | Baixa-Média — depende da planilha |

#### Arquitetura proposta: Adaptador LLM em três camadas

```
[Fonte bruta]
    ↓
[Camada 1 — Parser de formato]
  CSV, XLSX, JSON, PDF, TXT, áudio
    ↓
[Camada 2 — Extrator LLM]
  Ollama local identifica campo de resposta qualitativa
  Prompt: "Qual coluna/campo contém respostas abertas de pesquisa?"
    ↓
[Camada 3 — Normalizador]
  Gera id,comment CSV → entrada T3C
```

**Vantagem chave:** A Camada 2 (LLM) elimina a necessidade de escrever um parser específico para cada variante de formulário/planilha. O mesmo adaptador funciona para um Google Forms de 2022 e um Typeform de 2026, mesmo que as colunas tenham nomes diferentes.

#### Comparação de abordagens de implementação

| Abordagem | Esforço | Flexibilidade | Adequação TRL |
|-----------|---------|---------------|---------------|
| Script CLI Python (adapt_to_tttc.py) | Baixo | Alta | TRL 3 (PoC) |
| Plugin Express (nova rota /ingest) | Médio | Alta | TRL 4-5 (protótipo) |
| Interface web de upload com preview | Alto | Muito alta | TRL 5-6 (demo) |
| Integração nativa no fork T3C | Muito alto | Máxima | TRL 6+ (produto) |

Para o TRL 3 atual, o Step 4b do plano 000001 (script CLI) é o caminho certo. A arquitetura foi desenhada para escalar para as camadas superiores sem reescrever.

#### Fontes específicas do GaveaLab

Com base no contexto do projeto (pesquisa participativa, urbanismo, Amazônia, dados públicos do Rio), as fontes mais prováveis são:

1. **Formulários de consulta pública** — Google Forms ou equivalente (mais simples)
2. **Atas de audiências públicas** — PDFs ou DOCXs (mais complexo)
3. **Dados do Data.Rio** — APIs REST com JSON estruturado
4. **Entrevistas com moradores** — transcrições em texto ou áudio
5. **Questionários de pesquisa acadêmica** — XLSX com estrutura variável

#### Perguntas para o stakeholder (GaveaLab)

**Sobre fontes de dados:**
1. "Em quais formatos vocês coletam dados de participação cidadã hoje? (formulários online, planilhas, atas em PDF, WhatsApp, entrevistas...)"
2. "Qual é a frequência dessas coletas? São eventos pontuais (audiências) ou contínuos (formulários abertos)?"
3. "Existe alguma fonte de dados que vocês já têm mas nunca conseguiram analisar por falta de ferramenta?"

**Sobre dificuldades atuais:**
4. "Qual é o maior problema com os dados que vocês têm: volume, diversidade de formatos, ou qualidade/padronização das respostas?"
5. "Vocês já tentaram cruzar dados de diferentes fontes? Quais foram os obstáculos?"

**Sobre o que seria mais valioso:**
6. "Se uma ferramenta pudesse resolver UMA coisa para vocês hoje, o que seria: (a) analisar mais rapidamente dados que já têm, (b) integrar dados de fontes diferentes, ou (c) visualizar padrões que hoje são invisíveis?"

#### Análise por perspectivas

**Arquitetura:** A separação em 3 camadas (parser → extrator LLM → normalizador) é sólida. Cada camada é substituível independentemente — ex: trocar Ollama por um modelo mais especializado na Camada 2 sem reescrever os parsers. O risco principal é a qualidade da extração LLM para fontes muito heterogêneas (PDFs de atas com formatação irregular).

**Dados/ética:** Dados de participação cidadã podem conter informações pessoais (nome, endereço, contato). O adaptador deve ter uma etapa de anonimização antes de enviar ao T3C — especialmente relevante para o GaveaLab que trabalha com comunidades vulneráveis. Isso alinha com os princípios CARE/OCAP identificados no advisory-000002.

**Extensibilidade:** O mesmo adaptador pode alimentar não só o T3C, mas também o kb-qa (RAG) — transformando respostas de pesquisa em chunks indexáveis. Isso cria uma sinergia direta entre os dois projetos do grupo.

**Complexidade técnica:** Para TRL 3, o risco maior é a extração LLM de PDFs não estruturados (atas de reunião com múltiplos falantes, formatação irregular). Recomendado começar com CSV/XLSX e adicionar PDF como extensão posterior.

---

## Recomendações

| Prioridade | Recomendação |
|-----------|-------------|
| HIGH | Perguntar ao stakeholder as 6 questões acima antes de definir escopo — a escolha dos formatos suportados deve vir da realidade deles |
| HIGH | Implementar o adaptador CLI (Step 4b do plano 000001) como PoC: suportar CSV, XLSX, JSON, TXT na primeira versão |
| MEDIUM | Adicionar etapa de anonimização básica no adaptador antes de gerar o CSV de saída (remover campos com PII identificáveis) |
| MEDIUM | Explorar sinergia kb-qa + adaptador: as mesmas respostas normalizadas podem ser ingeridas tanto no T3C quanto no ChromaDB (RAG) |
| LOW | Planejar extensão para PDF/áudio como TRL 4+ — requer bibliotecas adicionais (pymupdf já está no kb-qa, whisper para áudio) |
| LOW | Avaliar interface web de upload com preview apenas após validar o CLI com dados reais do GaveaLab |
