# Runbook — Purga do dump do WhatsApp do histórico do git

> **Status:** PENDENTE — executar **somente após consultar o time** (todos cientes e prontos).
> O arquivo já foi removido do tree e gitignored (commit `bce7ea4`). Falta **purgar o histórico antigo**.
>
> **Alvo:** `knowledge/dump-grupo-wpp-24-05-2026.txt` — adicionado em `047cc9c`, presente em ~200 commits.
> **Remoto:** `github.com/Andreymcz/puc-inf2921-c` (branch `main`).

## ⚠️ Antes de começar (checklist do time)
- [ ] Todos os 6 membros fizeram **push** do que tinham (nada de trabalho local não salvo).
- [ ] Ninguém com rebase/merge em andamento; sem PRs abertos dependendo do histórico atual.
- [ ] Combinar uma janela: após o force-push, **todos re-clonam** (ou resetam) `main`.
- [ ] Cópia segura do conteúdo guardada fora do git (já existe em `private/`; idealmente mover para o Dropbox).

## Passos

```bash
# 0) Backup completo recuperável (bundle de TODO o repo, fora do git)
git bundle create ../inf2921-backup-pre-purge-$(date +%Y%m%d).bundle --all

# 1a) Opção A — git-filter-repo (recomendado; instalar se necessário)
#     pip install git-filter-repo   (ou: uv pip install git-filter-repo)
git filter-repo --path knowledge/dump-grupo-wpp-24-05-2026.txt --invert-paths --force

# 1b) Opção B — git filter-branch (built-in, sem instalar)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch knowledge/dump-grupo-wpp-24-05-2026.txt' \
  --prune-empty --tag-name-filter cat -- --all

# 2) Limpeza de refs/objetos (após filter-branch)
rm -rf .git/refs/original/ && git reflog expire --expire=now --all && git gc --prune=now --aggressive

# 3) Conferir que sumiu do histórico (deve não retornar nada)
git log --oneline --all -- knowledge/dump-grupo-wpp-24-05-2026.txt

# 4) Force-push do histórico reescrito (TODAS as branches/tags)
git push --force --all
git push --force --tags
```

## Depois (cada membro do time)
```bash
# Mais simples e seguro: re-clonar
git clone https://github.com/Andreymcz/puc-inf2921-c
# OU resetar o clone existente ao novo main
git fetch origin && git reset --hard origin/main
```

## Parte 2 — Limpar os vector stores locais (KB) ⚠️ não esquecer

A purga do git **não** limpa a base vetorial. Se alguma máquina rodou `kb-qa ingest` enquanto o
arquivo estava em `knowledge/`, o conteúdo do dump pode estar em `knowledge/vectorstore/`
(ChromaDB, gitignored) como chunks + embeddings.

> **Resolução (26/06): falso alarme.** A suspeita de que o dump estaria no vector store local
> (notebook do Tecgraf) não se confirmou como problema. O passo abaixo fica como **precaução**:
> rodar de qualquer forma é barato e garante consistência.

**Em CADA máquina que rodou `kb-qa ingest`:**
```bash
rm -rf knowledge/vectorstore/     # apaga o índice ChromaDB local
uv run kb-qa ingest               # reconstrói SEM o dump (ja removido de knowledge/)
uv run kb-qa status               # conferir contagem de chunks
```

> O `fala-gavea` tem ChromaDB próprio (`chroma_data/`, `local-data/chromadb`) que indexa
> **relatos**, não o dump — não precisa ser limpo por causa disto.

> Cópia de segurança do dump: `private/` (gitignored). Mover para o Dropbox/local seguro.

## Achado: impacto no projeto ≈ zero

O dump **não foi fonte de nenhum artefato**: o nome do arquivo nunca foi citado em planos,
researches, reflexões, advisories ou product-design (toda a história do git), e seu conteúdo
distintivo não aparece reproduzido em lugar nenhum. As personas/casos de uso vieram de outras
fontes (diagnóstico FAPERJ, `Casos_de_uso_*`, `Reunioes-stakeholders-1-2.pdf`, conversa de 15/06
colada na reflection-000052). Ou seja: remover o dump (git + vector store) **não quebra nada**.

## ⚠️ Limites importantes
- A reescrita **não desfaz** o fato de o dado já ter sido publicado. Se o repo é/foi público ou alguém já clonou, **trate o conteúdo como já divulgado** e avise o grupo.
- O GitHub pode reter o blob em caches/PRs/forks. Para remoção real do lado deles, **abrir ticket no GitHub Support** pedindo purga do objeto.
- Submódulo `fala-gavea` é separado — este arquivo não está lá; nada a fazer no submódulo.
- Princípio do projeto: soberania de dados / LGPD — só publicar o que for consentido por todos.
