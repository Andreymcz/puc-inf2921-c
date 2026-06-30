# Research 000079 | DOC -X | 2026-06-27 02:12 UTC | Prompt p/ apresentação 077-style no resqml-expert (estudo kb-qa)

tags: prompt-engineering, presentation, rag, seja, kb-qa

## User Brief

> Quero usar este mesmo padrão de apresentação (communication-000077) em outro contexto: o **resqml-expert**. Crie um prompt para eu executar em outro repositório SEJA-seeded. Vou apresentar um estudo envolvendo a criação do **kb-qa** (usado neste repositório) — ferramenta que usei para avaliar o desempenho das LLMs com contexto RAG adicionado em **one-shot**, comparado a implementar a mesma intenção usando **LLMs + RAG + SEJA**.

## Agent Interpretation

O entregável é um **prompt autocontido**, para colar numa sessão Claude Code dentro do repo `resqml-expert` (que já tem o harness SEJA instalado). Ao ser executado, o prompt instrui o agente a **gerar uma apresentação no padrão do `communication-000077`** (documento único relatório+slides, formato Marp, links de 3 camadas de profundidade, documento vivo) sobre o **estudo do kb-qa**.

Decisões confirmadas pelo usuário (Q&A desta sessão):
- **Tarefa do resqml-expert:** assistente buscador de **corpus técnico de domínio + programação** para o formato **RESQML** (Energistics).
- **Contraste central do estudo:** **RAG one-shot × RAG + SEJA (workflow)** — Braço A = LLM + RAG em prompt único (contexto injetado de uma vez); Braço B = a mesma intenção construída via SEJA (RAG + ciclo `/research→/plan→/implement→/check`, com artefatos rastreáveis).
- **Eixos de avaliação:** qualidade/acurácia; fidelidade/aterramento (groundedness); esforço/tempo e manutenibilidade. *(Custo de tokens/infra ficou de fora.)*
- **Dados:** os resultados do experimento **já existem** no repo `resqml-expert` → o prompt deve instruir o agente a **localizá-los e citá-los**.

Como o `resqml-expert` não está acessível a partir deste repositório, o prompt é **autocontido**: carrega (1) uma ficha técnica do kb-qa, (2) o desenho do estudo, (3) a especificação do padrão 077, e (4) um checklist de descoberta para o agente puxar os artefatos do próprio repo.

## Files

- `_output/communication/2026-06-26/communication-000077-timeline-projeto.md` (padrão de referência)
- `.claude/skills/scripts/md_to_html.py` (conversor md→html, presente em repos SEJA-seeded)
- `src/kb_qa/` (ficha técnica do kb-qa)

---

## Q&A

### Q1: Qual prompt usar no resqml-expert para gerar a apresentação 077-style sobre o estudo do kb-qa?

**A1.** Cole o bloco abaixo numa sessão Claude Code **dentro do repo `resqml-expert`**. Ele é autocontido — não depende de acesso a este repositório.

> Dica: ajuste apenas os campos marcados com `«...»` (links públicos, nomes de pastas) se o agente não conseguir inferi-los. Se o `resqml-expert` tiver a skill `/communicate`, você pode rodar o prompt como corpo de um `/communicate academics` para ganhar o ciclo de lifecycle (id reservado, commit). Caso contrário, o prompt já instrui o agente a reservar id, gerar `.md`+`.html` e commitar.

````text
CONTEXTO E OBJETIVO
Você está no repositório `resqml-expert` (assistente de busca em corpus técnico de
domínio + programação para o formato RESQML/Energistics), que usa o harness SEJA.
Gere UM documento único que serve simultaneamente como RELATÓRIO e APRESENTAÇÃO
(formato de slides), apresentando um ESTUDO sobre a ferramenta `kb-qa` e a comparação
entre duas abordagens de construir a mesma intenção do resqml-expert:
  • Braço A — LLM + RAG "one-shot": recupera trechos e injeta tudo num prompt único.
  • Braço B — LLM + RAG + SEJA: a mesma intenção construída via o workflow SEJA
    (/research → /plan → /implement → /check), com artefatos numerados e rastreáveis.
O kb-qa foi o INSTRUMENTO de avaliação usado para comparar os dois braços.

PÚBLICO E IDIOMA
Público: avaliadores técnicos / acadêmicos. Idioma: pt-BR (ajuste se o público do
resqml-expert for outro). Tom: preciso, sem marketing.

EIXOS DE AVALIAÇÃO (destacar exatamente estes três)
1. Qualidade/acurácia das respostas.
2. Fidelidade/aterramento (groundedness): respostas ancoradas nas fontes, menos
   alucinação, citações verificáveis.
3. Esforço/tempo de desenvolvimento e manutenibilidade/reprodutibilidade/rastreabilidade.
(Não focar em custo de tokens/infra, salvo se houver dados claros no repo.)

FICHA TÉCNICA DO kb-qa (use como base; confirme detalhes se o repo tiver o código)
- Ferramenta de RAG local genérica. Ingere .md e .pdf num vetor store e expõe
  `query_knowledge` via MCP, além de um CLI `kb-qa` (ingest / status / ask).
- Stack: Python 3.13 + uv; ChromaDB (PersistentClient, local); sentence-transformers
  (embeddings, ex.: nomic-embed-text-v1, multilíngue); pymupdf (PDF); FastMCP (servidor
  MCP); click (CLI).
- Chunking endereçável por conteúdo (hash de caminho + início do texto) → ingestão
  incremental e idempotente. `n_results` limitado (ex.: 20) na fronteira MCP.
- Papel no estudo: adiciona contexto RAG a sessões de LLM (recuperação injetada via MCP).
  No Braço A isso é feito "one-shot" (chunks no prompt, resposta única); no Braço B a
  recuperação está embutida num processo SEJA com etapas e artefatos.

DESCOBERTA NO REPOSITÓRIO (faça ANTES de escrever — não invente dados)
Inventarie e cite os artefatos REAIS do resqml-expert:
- Artefatos SEJA: `_output/` (research-logs, plans, roadmaps, reflections, advisory-logs,
  check-logs, communication), `product-design/`, `CLAUDE.md`, decisões D-NNN.
- Resultados do experimento já existentes (o usuário confirmou que existem): procure
  por avaliações/benchmarks, saídas do kb-qa, planilhas/JSON/CSV de métricas, logs de
  comparação A×B, prompts de teste, perguntas RESQML de avaliação. Busque em pastas como
  `_output/`, `eval/`, `benchmarks/`, `data/`, `results/`, `tests/`, `docs/`.
- Código relevante do resqml-expert (pipeline de RAG, ingestão do corpus RESQML, MCP).
Use `git log`, busca por arquivos e leitura. Para CADA número/afirmação do estudo, aponte
o arquivo-fonte por link relativo. Onde faltar dado, marque "📌 lacuna — preencher".

PADRÃO DE APRESENTAÇÃO (replicar o estilo "communication-000077")
Formato: Markdown compatível com **Marp** (frontmatter `marp: true`, tema, paginate),
slides separados por `---`. O MESMO arquivo é relatório + slides.
- MODELO DE 3 CAMADAS DE PROFUNDIDADE, com ícones nos links — "quanto mais fundo, mais
  técnico": 🟢 slide (visão) → 🟡 relatório/artefato SEJA (médio) → 🔴 código/fonte (técnico).
- DOCUMENTO VIVO: todo artefato citado é um LINK RELATIVO que abre o arquivo original
  (.md/.pdf/código) a partir da localização do .html gerado.
- NOTAS DE ORADOR: sob cada slide, um comentário HTML `<!-- ... -->` com a narrativa do
  relatório (visível no modo apresentador do Marp; oculto no documento).
- SLIDE DE CAPA com: título, subtítulo, autor/equipe, data, e o LINK PÚBLICO do
  repositório («URL do resqml-expert no GitHub/GitLab»).
- SLIDE "Como ler" (explica as 3 camadas) e SLIDE "Reprodução e navegação":
    git clone --recurse-submodules «URL do repo»
    # ou: git submodule update --init «submódulo se houver»
  + como abrir o .html (links relativos) + como exportar slides (Marp for VS Code →
  Export slide deck → PDF/PPTX).
- ANEXOS ao final = a camada técnica (🟡/🔴): detalhamento, tabelas e um índice de fontes
  originais (todos por link relativo). Funcionam como "slides de backup".

SEQUÊNCIA DE SLIDES SUGERIDA (adapte ao que existir no repo)
1. Capa (com link público do repo).
2. Como ler (modelo de profundidade).
3. Reprodução e navegação (clone + submódulos + Marp).
4. Problema/contexto: por que um assistente de corpus técnico para RESQML?
5. Objetivo do estudo: o que se quer descobrir (A×B).
6. Desenho do experimento: os dois braços (RAG one-shot × RAG+SEJA), variáveis controladas.
7. O instrumento: o que é o kb-qa e como mede (recuperação via MCP, perguntas de avaliação).
8. Eixos de avaliação: qualidade, groundedness, esforço/manutenibilidade.
9. Resultados (PUXAR do repo): tabelas/figuras com link à fonte de cada número.
10. Análise por eixo: o que A×B revelou em cada dimensão.
11. Ameaças à validade / limitações (tamanho de amostra, juiz, vazamento de contexto).
12. Conclusão: quando RAG one-shot basta e quando RAG+SEJA compensa.
13. Próximos passos.
14. Anexos: detalhe técnico + índice de fontes (links).

ARGUMENTO/TESE (fio condutor; confirme com os dados reais antes de afirmar)
RAG one-shot entrega respostas rápidas e boas para perguntas diretas; RAG + SEJA troca
imediatismo por **groundedness, rastreabilidade e manutenibilidade** — cada resposta/feature
vira um artefato auditável (pesquisa→decisão→plano→implementação→verificação). O kb-qa foi
o instrumento que tornou essa comparação mensurável.

SAÍDA E LIFECYCLE
- Se existir a skill `/communicate`: rode este conteúdo como corpo dela (público academics)
  para reservar id e commitar pelo lifecycle. Senão:
  • Reserve um id: `python .claude/skills/scripts/reserve_id.py --type communication --title 'estudo-kbqa-rag-vs-seja'`.
  • Grave o `.md` em `_output/communication/«AAAA-MM-DD»/communication-«id»-estudo-kbqa.md`.
  • Gere o `.html`: `python .claude/skills/scripts/md_to_html.py «caminho do .md» --lang pt-BR`.
- Verifique que os links relativos resolvem (os alvos existem) e que o frontmatter Marp
  não vaza no .html.
- Commit + push (mensagem: "communicate: estudo kb-qa RAG one-shot vs RAG+SEJA").

REGRAS
- NÃO invente resultados: todo número vem de um arquivo do repo, com link. Lacunas → "📌".
- Mantenha os slides concisos; ponha o detalhe nas notas de orador e nos anexos.
- Cite o kb-qa como ferramenta de OUTRO repositório (origem), deixando claro o que foi
  reaproveitado aqui.
````

---

## Recommendations Summary

| # | Prioridade | Recomendação |
|---|-----------|-------------|
| R1 | ALTA | Rodar o prompt acima no `resqml-expert`; preencher os campos `«...»` (URL pública do repo, submódulos) se o agente não inferir. |
| R2 | ALTA | Antes de escrever, exigir o **inventário de resultados reais** no repo (o usuário confirmou que existem) — cada número com link à fonte; lacunas marcadas. |
| R3 | MÉDIA | Se houver `/communicate` no `resqml-expert`, executar o prompt como corpo dela (ganha id + commit pelo lifecycle); senão, usar `reserve_id.py` + `md_to_html.py`. |
| R4 | MÉDIA | Reusar a checklist de qualidade do 077: âncoras resolvem, frontmatter Marp não vaza, links relativos válidos, slide de reprodução + link público na capa. |
| R5 | BAIXA | Considerar uma versão em inglês se o público do RESQML for internacional (o padrão é Energistics/EN). |
