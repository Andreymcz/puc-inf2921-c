# Como preencher o relatório — INF2921 Grupo C

O relatório principal está em `relatorio/relatorio-inf2921-grupo-c.tex` (LaTeX).
A bibliografia está em `relatorio/referencias.bib` (BibTeX).

## 1. Localizar seu bloco

Abra `relatorio-inf2921-grupo-c.tex` e pesquise por `\todo` ou pelo seu nome:

```
\todo[inline]{PREENCHER — SeuNome
```

Cada bloco tem perguntas orientadoras. Substitua o bloco `\todo{}` pelos seus parágrafos em texto LaTeX:

```latex
% antes
\todo[inline]{PREENCHER — Andrey: ... (3--4 parágrafos)}

% depois
Minha perspectiva sobre este tema é ...

Em segundo lugar, ...
```

## 2. Formatação LaTeX básica

- Parágrafos: separe por uma linha em branco
- **Negrito**: `\textbf{texto}`
- *Itálico*: `\textit{texto}` ou `\emph{texto}`
- Aspas: use `\enquote{texto}` ou `''texto''`
- Cite planos/decisões por ID: `\texttt{plan-000001}`, `\texttt{D-004}`
- Não use `\section` ou `\subsection` dentro dos seus blocos — mantenha só parágrafos

## 3. Blocos coletivos

Seções marcadas com `PREENCHER — Todos` ou `PREENCHER — Andrey (rascunho) + todos (revisão)` devem ser redigidas em conjunto. Sugestão: Andrey faz um rascunho; todos revisam pelo WhatsApp e editam diretamente no `.tex`.

## 4. Seção que aguarda geração automática

A seção 3.1 (diagrama de arquitetura) tem um placeholder:

```
\todo[inline]{SEÇÃO AGUARDA diagrama de arquitetura ...}
```

Quando o diagrama for gerado (Step 4 do plan-000075), substituir por um bloco Mermaid ou figura.

## 5. Compilar para PDF

### Opção 1: pdflatex + biber (recomendado)

```bash
cd relatorio/
pdflatex relatorio-inf2921-grupo-c.tex
biber relatorio-inf2921-grupo-c
pdflatex relatorio-inf2921-grupo-c.tex
pdflatex relatorio-inf2921-grupo-c.tex
```

### Opção 2: latexmk (automatiza os múltiplos passes)

```bash
cd relatorio/
latexmk -pdf relatorio-inf2921-grupo-c.tex
```

### Opção 3: Overleaf

1. Compacte `relatorio/` em zip
2. Importe no Overleaf (overleaf.com)
3. Compile diretamente no browser (já reconhece biber)
4. Baixe o PDF gerado

### Opção 4: Docker (sem instalar nada localmente)

```bash
docker run --rm -v "$(pwd)/relatorio:/data" texlive/texlive:latest \
  bash -c "cd /data && latexmk -pdf relatorio-inf2921-grupo-c.tex"
```

## 6. Status das seções

| Seção | Status | Responsável |
|-------|--------|-------------|
| Resumo | `\todo` — aguarda contribuições individuais | Andrey (rascunho) + todos |
| 1.1 Contexto e Motivação | Pré-preenchido | — |
| 1.2 O que o grupo já conhecia | `\todo` por membro | Cada membro |
| 2.1 Formação da equipe | Pré-preenchido + `\todo` coletivo | Todos |
| 2.2 Definição do tema | Pré-preenchido + `\todo` stakeholder | Andrey + Natali |
| 2.3 Pesquisas iniciais | Pré-preenchido + `\todo` por membro | Cada membro |
| 2.4 Refinamento | Pré-preenchido + `\todo` por membro | Cada membro |
| 2.5 Surpresas | `\todo` por membro | Cada membro |
| 2.6 Comunicação | Pré-preenchido + `\todo` coletivo | Todos |
| 3.1 Arquitetura | `\todo` aguardando diagrama | Step 4 do plan-000075 |
| 3.2 Decisões D-001–D-005 | Pré-preenchido | — |
| 3.3 Stack | Pré-preenchido | — |
| 4.1 Desafios | Pré-preenchido | — |
| 4.2 Como endereçados | Pré-preenchido | — |
| 4.3 Perspectivas individuais | `\todo` por membro | Cada membro |
| 5.1 Funcionalidades | Pré-preenchido | — |
| 5.2 Limitações | Pré-preenchido | — |
| 6. Conclusão | `\todo` coletivo | Andrey (rascunho) + todos |
| Referências | `referencias.bib` pré-preenchido | Todos adicionam suas refs |
| Apêndice A: Linha do tempo | Pré-preenchido (de evolution-000076) | — |
| Apêndice B: Jornadas | Pré-preenchido | — |

## 7. Prazo e entrega

> **[A definir pelo grupo — data-limite para contribuições individuais e data de envio ao professor]**

Formato de entrega ao professor: `.pdf`
