# Plan 000075 | INF2921-Grupo-C | 2026-06-25 19:30 UTC | Relatório disciplina INF2921 — template colaborativo | Review: light
plan_format_version: 1

## Brief

Gerar um template Markdown para o relatório final da disciplina INF2921/CIS2114 (PUC-Rio 2026.1) que:
- Atenda às coordenadas do professor (processo de elaboração, desafios de confiabilidade/segurança/responsabilidade social, procedimentos e decisões tomadas)
- Pré-preencha as seções técnicas com informações já existentes no repositório (design intent, decisões, arquitetura, meetings)
- Deixe blocos colaborativos com perguntas orientadoras para cada membro da equipe inserir sua perspectiva
- Sirva de base para exportação em PDF

**Coordenadas do professor (literais):**
> "Cada grupo deve enviar também um relatório detalhando o processo de elaboração do seu projeto. A bibliografia acadêmica mobilizada deve constar ao término do relatório. O relatório deverá explicitar os desafios com que o grupo se deparou, em especial os relacionados aos requisitos para sistemas confiáveis, seguros e socialmente responsáveis, e como eles foram endereçados. Além disso, uma parte fundamental do relatório deverá descrever quais foram os procedimentos seguidos e as decisões tomadas na elaboração do projeto [...]. O relatório deve ser enviado em formato .pdf."

---

## Context

### Fontes disponíveis no repositório

| Fonte | Conteúdo relevante |
|-------|-------------------|
| `product-design/project/product-design-as-intended.md` | Design intent completo (§1 propósito, §2 entidades, §3 conceitos, §10 constantes, §12 metacomunicação, §13 user stories, §15 jornadas, Decisões D-001–D-005) |
| `product-design/project/constitution.md` | Princípios técnicos, de qualidade e segurança (T1-T8, Q1-Q3, S1-S4, C1-C2) |
| `knowledge/Reuniao-23-04-2026.md` | Notas da reunião de brainstorming inicial (temas: segurança pública, educação, atlas digital) |
| `knowledge/casos-de-uso.md` | Casos de uso preliminares (cidadão, gestor público, GaveaLab) |
| `knowledge/dump-grupo-wpp-24-05-2026.txt` | Histórico de comunicação do grupo (WhatsApp) — processo de formação e primeiras discussões |
| `knowledge/datasets.md` | Datasets considerados (SINESP, IPLAN Rio, DATAZOOM) |
| `knowledge/library/` | PDF de referências acadêmicas já coletadas (Weisz et al. 2024, EARTO 2014, 2203.05794v1) |
| `_output/plans/` | Histórico de planos executados (000006–000075) — trilha de decisões técnicas |

### Membros da equipe

Andrey, Mauro, Julia, Herbert, Natali (+ Sheila per constitution)

---

## Steps

### Step 1: Criar a estrutura base do template de relatório

Criar o arquivo `relatorio/relatorio-inf2921-grupo-c.md` com todas as seções exigidas pelo professor, pré-preenchidas com o conteúdo técnico já documentado no repositório e com blocos colaborativos marcados por `<!-- PREENCHER: ... -->` para os membros da equipe.

**Estrutura de seções:**

```
Capa (título, disciplina, equipe, data)
Resumo [placeholder coletivo — 1 parágrafo]
1. Introdução
   1.1 Contexto e Motivação [pré-preenchido do §1 design-as-intended]
   1.2 O que o grupo já conhecia [placeholder por membro]
2. Processo de Elaboração
   2.1 Formação da equipe e primeiras discussões [pré-preenchido do WhatsApp dump + Reunião 23/04]
   2.2 Definição do tema e escopo [pré-preenchido do brainstorming → GaveaLab]
   2.3 Pesquisas iniciais: ferramentas e perguntas [placeholder por membro + lista de fontes]
   2.4 Refinamento dos resultados iniciais [pré-preenchido da evolução de planos]
   2.5 Surpresas e tentativas que não deram certo [placeholder por membro]
   2.6 Organização da comunicação da equipe [pré-preenchido: WhatsApp + GitHub + Claude Code]
3. Arquitetura e Decisões Técnicas
   3.1 Visão geral da arquitetura [pré-preenchido do §2 entidades e conventions.md]
   3.2 Principais decisões técnicas [pré-preenchido de D-001–D-005]
   3.3 Stack e ferramentas [pré-preenchido do CLAUDE.md + pyproject.toml]
4. Requisitos para Sistemas Confiáveis, Seguros e Socialmente Responsáveis
   4.1 Desafios identificados [placeholder estruturado com categorias: privacidade, viés, transparência, acessibilidade]
   4.2 Como os desafios foram endereçados [mapeado dos princípios S1-S4, C1-C2 + placeholder complementar]
   4.3 Perspectiva de cada membro [placeholder por membro]
5. Resultados e Estado Atual
   5.1 Funcionalidades implementadas [pré-preenchido das US-GL-001–005 + planos executados]
   5.2 Limitações e trabalho futuro [pré-preenchido do §0 Planned Changes]
6. Conclusão [placeholder coletivo]
Referências [pré-preenchido dos PDFs em knowledge/library/ + datasets.md + citações do design-as-intended]
Apêndice: Jornadas de Usuário [pré-preenchido de JM-TB-001, JM-TB-002]
```

**Convenções para blocos colaborativos:**

Cada bloco placeholder usará o formato:

```markdown
> **[PREENCHER — NomeMembro]**
> *Perguntas orientadoras:*
> - Pergunta 1?
> - Pergunta 2?
> *(Apague este bloco e insira sua contribuição aqui — 2 a 5 parágrafos)*
```

- **Files**: `relatorio/relatorio-inf2921-grupo-c.tex` (create — LaTeX a pedido do usuário), `relatorio/referencias.bib` (create), `relatorio/relatorio-inf2921-grupo-c.md` (create — Markdown intermediário, supersedido pelo .tex)
- **References**: `product-design/project/product-design-as-intended.md`, `product-design/project/constitution.md`, `knowledge/Reuniao-23-04-2026.md`, `knowledge/casos-de-uso.md`, `knowledge/datasets.md`
- **Interface**: N/A
- **Verify**: `.tex` criado; seções 1–6 + Referências + Apêndices presentes; `\todo{}` identificáveis para cada membro; conteúdo técnico de D-001–D-005 presente em `\subsection{Principais Decisões Técnicas}`
- **Tests**: N/A
- **Docs**: O próprio documento é o artefato final
- **Traces**: US-GL-001, US-GL-002, US-GL-003, US-GL-004, US-GL-005
- [x] Done — `relatorio-inf2921-grupo-c.tex` + `referencias.bib` criados; formato LaTeX (pdflatex/xelatex + biber)

---

### Step 2: Adicionar guia de instruções para preenchimento colaborativo

Criar `relatorio/COMO-PREENCHER.md` com instruções práticas para os membros da equipe: como localizar os blocos de preenchimento, convenções de formatação, prazo, e instrução de exportação para PDF via Pandoc ou VS Code.

```markdown
# Como preencher o relatório

## Localizar seu bloco
Pesquise `[PREENCHER — SeuNome]` no arquivo `relatorio-inf2921-grupo-c.md`.

## Formatação
- Use parágrafos corridos (sem bullets desnecessários)
- Máximo 5 parágrafos por bloco individual
- Mantenha o português do Brasil

## Exportar para PDF
# opção 1: Pandoc
pandoc relatorio-inf2921-grupo-c.md -o relatorio-inf2921-grupo-c.pdf --pdf-engine=xelatex

# opção 2: VS Code
Instale a extensão "Markdown PDF" → botão direito → "Markdown PDF: Export (pdf)"

## Prazo
[A preencher pelo grupo]
```

- **Files**: `relatorio/COMO-PREENCHER.md` (create — guia de preenchimento Markdown; mantido como referência de processo)
- **Depends on**: Step 1
- **Interface**: N/A
- **Verify**: Arquivo criado; contém instrução de exportação PDF
- **Tests**: N/A
- [x] Done — `COMO-PREENCHER.md` criado; seção 6 cobre pdflatex + biber para o .tex

---

### Step 3: Gerar relatório de evolução do projeto com `/explain behavior-evolution`

Executar o skill `/explain behavior-evolution` para minerar o histórico de planos em `_output/plans/` e gerar uma linha do tempo narrativa da evolução do projeto desde os primeiros planos (kb-qa genérico, TRL1) até o GaveaLab atual (TRL2+). O relatório gerado em `_output/behavior-evolution/` será usado como fonte primária para a seção 2.4 "Refinamento dos resultados iniciais" e como anexo de evidência de processo.

Perguntas orientadoras para o skill:
- "Como o projeto evoluiu desde o plano 000001 até o estado atual?"
- "Quais decisões de produto foram tomadas e como mudaram o escopo?"
- "Como a arquitetura evoluiu de kb-qa para GaveaLab?"

- **Files**: `_output/behavior-evolution/<gerado-pelo-skill>.md` (create via skill)
- **Depends on**: Step 1
- **Interface**: N/A
- **Verify**: Arquivo de behavior-evolution gerado; contém linha do tempo com referências a pelo menos 5 planos distintos; cobre a transição kb-qa → GaveaLab
- **Tests**: N/A
- [x] Done — evolution-000076 gerado e corrigido (tttc-poc TRL3 alcançado); commit 7cfbdad

---

### Step 4: Gerar relatório de arquitetura com `/explain architecture`

Executar o skill `/explain architecture` para gerar um relatório de arquitetura atual do GaveaLab com diagramas e analogias. O relatório gerado em `_output/explained-architecture/` será usado para pré-preencher a seção 3.1 do template com um diagrama de componentes e uma descrição estruturada da arquitetura.

Perguntas orientadoras para o skill:
- "Explique a arquitetura do GaveaLab: quais são os componentes principais e como eles interagem?"
- "Como o pipeline LLM (topics → claims → cruxes) se conecta à camada de persistência e à UI Streamlit?"

- **Files**: `_output/explained-architecture/<gerado-pelo-skill>.md` (create via skill)
- **Depends on**: Step 1
- **Interface**: N/A
- **Verify**: Arquivo de architecture explanation gerado; contém pelo menos um diagrama (Mermaid ou ASCII) da arquitetura GaveaLab + kb-qa; descreve os 5 módulos principais (app.py, llm.py, workspace.py, pipeline/, pages/)
- **Tests**: N/A
- [ ] Done

---

### Step 5: Integrar artefatos de conhecimento no template do relatório

Com os relatórios dos Steps 3 e 4 em mãos, atualizar `relatorio/relatorio-inf2921-grupo-c.md` para:

1. **Seção 2.4**: Inserir resumo da linha do tempo de evolução extraída do behavior-evolution report (Steps de TRL: kb-qa genérico → GaveaLab PoC → GaveaLab com UMAP)
2. **Seção 3.1**: Inserir diagrama de arquitetura do architecture explanation report
3. **Seção 3.2**: Formatar as decisões D-001–D-005 de `product-design/project/product-design-as-intended.md` como itens de discussão acadêmica com contexto, decisão e consequências
4. **Referências**: Adicionar entradas bibliográficas formatadas para os PDFs em `knowledge/library/`:
   - Weisz et al. (2024) — Design Principles for Generative AI Applications
   - EARTO (2014) — The TRL Scale as a Research & Innovation Policy Tool
   - Paper 2203.05794v1 (verificar autoria e título na leitura do PDF)

- **Files**: `relatorio/relatorio-inf2921-grupo-c.md` (modify)
- **Depends on**: Step 1, Step 3, Step 4
- **Interface**: N/A
- **Verify**: Seção 3.2 contém D-001–D-005 formatadas; seção 3.1 tem diagrama; seção 2.4 tem linha do tempo; Referências tem ≥3 entradas bibliográficas com autores/anos
- **Tests**: N/A
- [ ] Done

---

## Artifact Index

| Artifact | Path | Status |
|----------|------|--------|
| Relatório LaTeX | `relatorio/relatorio-inf2921-grupo-c.tex` | Done |
| Bibliografia BibTeX | `relatorio/referencias.bib` | Done |
| Guia de preenchimento | `relatorio/COMO-PREENCHER.md` | Done |
| Behavior evolution report | `_output/behavior-evolution/evolution-000076-evolucao-projeto-inf2921-gavealab-fala-gavea.md` | Done |
| Architecture explanation | `_output/explained-architecture/<gerado-pelo-skill>.md` | Pending (Step 4) |

---

## Notes

- O conteúdo técnico (arquitetura, decisões D-001–D-005, user stories, jornadas) está integralmente documentado no `product-design/` — o Step 1 deve copiar/adaptar essas seções diretamente, não reescrever do zero.
- Os blocos `[PREENCHER]` para seção 4.3 (perspectiva individual sobre sistemas confiáveis) são os mais importantes: cobrem o requisito central das coordenadas do professor.
- As referências bibliográficas devem incluir os PDFs em `knowledge/library/` (Weisz et al. 2024, EARTO 2014) e o paper 2203.05794v1 recém-adicionado.
- O dump do WhatsApp (`knowledge/dump-grupo-wpp-24-05-2026.txt`) é rico em processo de formação da equipe e primeiras decisões — deve informar a seção 2.1 e 2.6 sem citar mensagens privadas diretamente.
