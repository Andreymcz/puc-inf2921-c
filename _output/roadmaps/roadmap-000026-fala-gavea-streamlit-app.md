# Roadmap 000026 | 2026-06-11 03:08 UTC | fala-gavea: Streamlit App de Participação Cidadã

source: research-000023 -- visão da plataforma Fala Gávea e modelo de dados da postagem cidadã

## Contexto

O app `fala-gavea/` é o **Subsistema A** da Plataforma Fala Gávea, conforme mapeado na research-000023. É um app Streamlit que:

1. **Mostra postagens** de cidadãos (texto + território)
2. **Permite likes** em postagens de outros usuários — máximo 1 like por usuário por postagem
3. **Coleta feedback humano sobre labels gerados pela IA** (tópico, cluster) por meio de thumbs up/down
4. **Dashboard** com métricas agregadas: posts com mais likes, filtros por território, sinais sobre acurácia dos labels da IA

A identidade do usuário é gerada automaticamente como UUID no início da sessão (sem cadastro ou login). O usuário não pode dar like na própria postagem.

O diretório `fala-gavea/` já existe com um `pyproject.toml` scaffoldado para FastAPI; este roadmap o reconverte para Streamlit.

---

## Source

- `fala-gavea/pyproject.toml` (read — scaffolded, será reescrito)
- `_output/research-logs/research-000023-plataforma-fala-gavea-roadmap.md` (read)
- `gavealab-poc/gavealab_poc/workspace.py` (read — padrão de workspace SQLite a replicar)
- `product-design/project/product-design-as-intended.md` (read)
- `product-design/project/conventions.md` (read)

---

## Modelo de Dados

```
Post {
  id           TEXT PRIMARY KEY   -- UUID
  user_id      TEXT NOT NULL      -- UUID anônimo (gerado na sessão)
  text         TEXT NOT NULL
  territory    TEXT               -- ex.: "Rocinha", "Gávea Asfalto"
  topic_label  TEXT               -- label gerado pela IA (pode ser NULL)
  cluster_id   TEXT               -- cluster da IA (pode ser NULL)
  created_at   TEXT NOT NULL      -- ISO-8601 UTC
}

Like {
  user_id      TEXT NOT NULL
  post_id      TEXT NOT NULL REFERENCES posts(id)
  created_at   TEXT NOT NULL
  PRIMARY KEY (user_id, post_id)  -- garante 1 like por user por post
}

LabelFeedback {
  id           INTEGER PRIMARY KEY AUTOINCREMENT
  user_id      TEXT NOT NULL
  post_id      TEXT NOT NULL REFERENCES posts(id)
  label_type   TEXT NOT NULL      -- 'topic_label' | 'cluster'
  signal       TEXT NOT NULL      -- 'like' | 'dislike'
  created_at   TEXT NOT NULL
  UNIQUE (user_id, post_id, label_type)  -- 1 sinal por user por post por tipo de label
}
```

---

## Wave Summary

### Wave 0 — Foundation (sequencial)

| # | ID | Título | Escopo | Tipo | Plan | Status |
|---|-----|--------|--------|------|------|--------|
| 1 | setup | Project setup: pyproject.toml Streamlit + estrutura de pacote | cross | chore | [plan-000027](./../plans/plan-000027-fala-gavea-setup-streamlit.md) | pending |
| 2 | workspace | FalaGaveaWorkspace: SQLite schema (Post, Like, LabelFeedback) | backend | feature | plan-TBD | pending |

### Wave 1 — Páginas principais (paralelo após Wave 0)

| # | ID | Título | Escopo | Tipo | Plan | Depends on | Status |
|---|-----|--------|--------|------|------|-----------|--------|
| 3 | page-posts | Página "Postagens": lista de posts + like button | frontend | feature | plan-TBD | workspace | pending |
| 4 | page-new-post | Página "Nova Postagem": formulário de submissão | frontend | feature | plan-TBD | workspace | pending |

### Wave 2 — Feedback de labels + Dashboard (paralelo após Wave 1)

| # | ID | Título | Escopo | Tipo | Plan | Depends on | Status |
|---|-----|--------|--------|------|------|-----------|--------|
| 5 | page-label-feedback | Feedback de labels da IA (thumbs up/down em topic_label e cluster) | frontend | feature | plan-TBD | page-posts | pending |
| 6 | page-dashboard | Dashboard: top posts, métricas de likes, filtros, feedback de labels | frontend | feature | plan-TBD | page-posts | pending |

> O `Plan` começa como `plan-TBD` para todos os itens pendentes. Preencher com o ID real (ex.: `plan-000028`) somente após `/plan` ser invocado para aquele item e retornar o ID reservado.

---

## Detalhamento dos Itens

### W0-1: setup — Project setup

**Objetivo:** Converter `fala-gavea/pyproject.toml` para Streamlit + criar a estrutura de pacote `fala_gavea/`.

**Estrutura de diretórios resultante:**
```
fala-gavea/
  app.py                        # Entry point: st.navigation + page dispatch
  pyproject.toml                # streamlit, pandas (sem fastapi/uvicorn)
  fala_gavea/
    __init__.py
    workspace.py                # FalaGaveaWorkspace (SQLite)
    pages/
      posts.py                  # render() — lista de postagens + likes
      new_post.py               # render() — formulário de nova postagem
      label_feedback.py         # render() — feedback de labels da IA
      dashboard.py              # render() — dashboard de métricas
```

**Dependências Streamlit:**
```toml
dependencies = [
  "streamlit>=1.35",
  "pandas>=2.0",
]
```

**Identidade de usuário:** UUID gerado em `app.py` via `st.session_state.user_id = str(uuid.uuid4())` se ausente. Exibido na sidebar como "Sua ID de sessão: `{uuid[:8]}...`".

---

### W0-2: workspace — FalaGaveaWorkspace

**Objetivo:** Criar `fala_gavea/workspace.py` com `FalaGaveaWorkspace` — o único ponto de acesso ao SQLite.

**Contrato público:**
```python
class FalaGaveaWorkspace:
    def __init__(self, db_path: Path) -> None: ...

    # Posts
    def create_post(self, user_id: str, text: str, territory: str | None) -> str: ...  # retorna post_id
    def list_posts(self, territory: str | None = None) -> list[dict]: ...
    def get_post(self, post_id: str) -> dict | None: ...

    # Likes
    def toggle_like(self, user_id: str, post_id: str) -> bool: ...  # True = liked, False = unliked
    def get_like_count(self, post_id: str) -> int: ...
    def user_liked(self, user_id: str, post_id: str) -> bool: ...
    def top_posts(self, limit: int = 10, territory: str | None = None) -> list[dict]: ...

    # Label feedback
    def set_label_feedback(self, user_id: str, post_id: str, label_type: str, signal: str) -> None: ...
    def get_label_feedback(self, post_id: str) -> dict: ...  # {label_type: {likes: int, dislikes: int}}
    def get_label_accuracy_summary(self) -> list[dict]: ...  # por topic_label: {label, likes, dislikes, accuracy_pct}
```

**Restrição de negócio implementada em SQL:** a PRIMARY KEY `(user_id, post_id)` na tabela `likes` garante a regra "1 like por usuário por postagem" no banco — sem validação extra no Python.

---

### W1-1: page-posts — Página "Postagens"

**Layout:**
- Sidebar: seletor de território (All + lista de territórios distintos)
- Body: lista de postagens filtradas, mais recentes primeiro
- Cada postagem exibe: texto, território, data, contador de likes, botão Like/Unlike
- O botão fica desabilitado se `post.user_id == session.user_id` (não pode dar like no próprio post)
- Clicar em Like chama `workspace.toggle_like()`; a página faz rerun via `st.rerun()`

---

### W1-2: page-new-post — Página "Nova Postagem"

**Layout:**
- Formulário: `st.text_area("Seu relato")` + `st.selectbox("Território", ["Gávea Asfalto", "Rocinha", "Outros"])` + botão Enviar
- Validação: texto não vazio, mínimo 10 chars
- Após envio: `workspace.create_post(user_id, text, territory)` + `st.success("Postagem enviada!")`

---

### W2-1: page-label-feedback — Feedback de labels da IA

**Contexto:** Posts com `topic_label != NULL` podem ter feedback de acurácia.

**Layout (na página Postagens, como expansão de cada card):**
- Se `post.topic_label` existe: exibe "Tema: {topic_label}" + 👍 👎 buttons
- Se `post.cluster_id` existe: exibe "Cluster: {cluster_id}" + 👍 👎 buttons
- Ao clicar: `workspace.set_label_feedback(user_id, post_id, label_type, signal)`
- O botão selecionado fica highlighted; clicar de novo substitui (upsert via UNIQUE constraint)

**Alternativa de implementação:** pode ser uma página separada "Validar Labels" com lista só de posts que têm labels da IA.

---

### W2-2: page-dashboard — Dashboard

**Seções:**

1. **Top Posts por Likes**
   - `st.bar_chart` ou `st.dataframe` dos N posts mais curtidos
   - Filtro por território (sidebar)

2. **Métricas Gerais**
   - Total de postagens, total de likes, usuários únicos (estimativa por user_id distintos)
   - `st.metric()` tiles

3. **Distribuição por Território**
   - `st.bar_chart` de postagens por território

4. **Feedback de Labels da IA**
   - Tabela: por `topic_label` → {likes, dislikes, acurácia %}
   - Ordena por volume de feedback
   - Indica labels com baixa acurácia (< 50%) em vermelho via `st.dataframe` com estilo

---

## Execution Instructions

### Wave 0 (sequencial)

Execute um por vez, em ordem:

1. `/plan` "W0-1: converter fala-gavea para Streamlit — pyproject.toml + estrutura de pacote" → `/implement <id>`
2. `/plan` "W0-2: FalaGaveaWorkspace — SQLite schema Post/Like/LabelFeedback + métodos públicos" → `/implement <id>`

### Wave 1 (paralelo — 2 plans)

Ambos dependem de Wave 0. Podem ser executados em paralelo após Wave 0 completa:

- `/plan` "W1-1: Página Postagens — lista de posts + like button com restrição de negócio" → `/implement <id>`
- `/plan` "W1-2: Página Nova Postagem — formulário de submissão + validação" → `/implement <id>`

### Wave 2 (paralelo — 2 plans)

Ambos dependem de Wave 1. Podem ser executados em paralelo após Wave 1 completa:

- `/plan` "W2-1: Feedback de labels da IA — thumbs up/down em topic_label e cluster" → `/implement <id>`
- `/plan` "W2-2: Dashboard — top posts, métricas de likes, filtros por território, resumo de feedback de labels" → `/implement <id>`

---

## Notas de Implementação

- **Identidade anônima:** user_id é gerado por sessão Streamlit (`st.session_state`). Não persiste entre sessões diferentes do mesmo usuário — isso é intencional para o PoC.
- **Sem auth real:** a restrição "não dar like no próprio post" é enforçada comparando `post.user_id == session.user_id` — confiável apenas dentro da mesma sessão Streamlit.
- **SQLite é suficiente** para o PoC single-user; para multiusuário real, migrar para PostgreSQL (Fase 2 do roadmap da research-000023).
- **Labels da IA:** nesta versão, os campos `topic_label` e `cluster_id` nos posts são preenchidos manualmente (fixture/seed) ou importados via CSV. A integração com o pipeline do gavealab-poc é escopo da Fase 2.
- **Padrão de workspace:** seguir o padrão de `gavealab-poc/gavealab_poc/workspace.py` — `@st.cache_resource` no `app.py` para criar o singleton `FalaGaveaWorkspace`.
