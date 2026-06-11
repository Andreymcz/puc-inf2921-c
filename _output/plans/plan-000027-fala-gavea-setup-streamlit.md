# Plan 000027 | CHORE-X | 2026-06-11 03:08 UTC | fala-gavea: Project setup — Streamlit + estrutura de pacote | Review: light
plan_format_version: 1

source: roadmap-000026 -- W0-1: converter fala-gavea para Streamlit

## User Brief

Converter o diretório `fala-gavea/` (atualmente scaffoldado com FastAPI) para um app Streamlit. Criar a estrutura de pacote `fala_gavea/` com o entry point `app.py` e os módulos necessários (workspace, pages).

## Agent Interpretation

O `fala-gavea/pyproject.toml` já existe com FastAPI/SQLAlchemy. Precisamos:
1. Reescrever o `pyproject.toml` com Streamlit + pandas (remover FastAPI/uvicorn/SQLAlchemy)
2. Criar `fala-gavea/app.py` — entry point Streamlit com geração de `user_id` e `st.navigation`
3. Criar a estrutura de pacote `fala_gavea/` com stubs de páginas
4. Criar `fala-gavea/.gitignore` se não existir (excluir `.venv`, `*.db`)

## Files

- `fala-gavea/pyproject.toml` — reescrever
- `fala-gavea/app.py` — criar
- `fala-gavea/fala_gavea/__init__.py` — criar
- `fala-gavea/fala_gavea/workspace.py` — criar stub (schema real no plan-TBD W0-2)
- `fala-gavea/fala_gavea/pages/__init__.py` — criar
- `fala-gavea/fala_gavea/pages/posts.py` — criar stub
- `fala-gavea/fala_gavea/pages/new_post.py` — criar stub
- `fala-gavea/fala_gavea/pages/label_feedback.py` — criar stub
- `fala-gavea/fala_gavea/pages/dashboard.py` — criar stub
- `fala-gavea/.gitignore` — criar ou atualizar

## Steps

### Step 1 — Reescrever pyproject.toml

Reescrever `fala-gavea/pyproject.toml` com as dependências Streamlit:

```toml
[project]
name = "fala-gavea"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "streamlit>=1.35",
    "pandas>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.4",
    "pyright>=1.1",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["fala_gavea"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py313"
```

**Validation:** `fala-gavea/pyproject.toml` não deve conter referências a fastapi, uvicorn, sqlalchemy.

---

### Step 2 — Criar app.py (entry point Streamlit)

Criar `fala-gavea/app.py`:

```python
import uuid
import streamlit as st
from pathlib import Path
from fala_gavea.workspace import FalaGaveaWorkspace
from fala_gavea.pages import posts, new_post, label_feedback, dashboard

st.set_page_config(page_title="Fala Gávea", page_icon="🗣️", layout="wide")

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

@st.cache_resource
def get_workspace() -> FalaGaveaWorkspace:
    db_path = Path(__file__).parent / "fala_gavea.db"
    return FalaGaveaWorkspace(db_path)

workspace = get_workspace()

pages = {
    "Postagens": posts,
    "Nova Postagem": new_post,
    "Validar Labels": label_feedback,
    "Dashboard": dashboard,
}

with st.sidebar:
    st.title("🗣️ Fala Gávea")
    st.caption(f"Sessão: `{st.session_state.user_id[:8]}...`")
    selection = st.radio("Navegação", list(pages.keys()))

pages[selection].render(workspace, st.session_state.user_id)
```

**Validation:** `app.py` importa os 4 módulos de página; executa sem erro com `streamlit run app.py` (mesmo que as páginas sejam stubs).

---

### Step 3 — Criar estrutura de pacote fala_gavea/

Criar os seguintes arquivos:

**`fala-gavea/fala_gavea/__init__.py`** — vazio

**`fala-gavea/fala_gavea/workspace.py`** — stub com schema SQLite e métodos placeholder:

```python
from pathlib import Path
import sqlite3


class FalaGaveaWorkspace:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS posts (
                    id          TEXT PRIMARY KEY,
                    user_id     TEXT NOT NULL,
                    text        TEXT NOT NULL,
                    territory   TEXT,
                    topic_label TEXT,
                    cluster_id  TEXT,
                    created_at  TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS likes (
                    user_id    TEXT NOT NULL,
                    post_id    TEXT NOT NULL REFERENCES posts(id),
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (user_id, post_id)
                );
                CREATE TABLE IF NOT EXISTS label_feedback (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id    TEXT NOT NULL,
                    post_id    TEXT NOT NULL REFERENCES posts(id),
                    label_type TEXT NOT NULL,
                    signal     TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE (user_id, post_id, label_type)
                );
            """)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn
```

Note: os métodos de negócio (create_post, toggle_like, etc.) são implementados no plan W0-2 (plan-TBD).

**`fala-gavea/fala_gavea/pages/__init__.py`** — vazio

**`fala-gavea/fala_gavea/pages/posts.py`** — stub:
```python
import streamlit as st
from fala_gavea.workspace import FalaGaveaWorkspace


def render(workspace: FalaGaveaWorkspace, user_id: str) -> None:
    st.header("Postagens")
    st.info("Em construção — implementado no plan W1-1")
```

**`fala-gavea/fala_gavea/pages/new_post.py`** — stub:
```python
import streamlit as st
from fala_gavea.workspace import FalaGaveaWorkspace


def render(workspace: FalaGaveaWorkspace, user_id: str) -> None:
    st.header("Nova Postagem")
    st.info("Em construção — implementado no plan W1-2")
```

**`fala-gavea/fala_gavea/pages/label_feedback.py`** — stub:
```python
import streamlit as st
from fala_gavea.workspace import FalaGaveaWorkspace


def render(workspace: FalaGaveaWorkspace, user_id: str) -> None:
    st.header("Validar Labels da IA")
    st.info("Em construção — implementado no plan W2-1")
```

**`fala-gavea/fala_gavea/pages/dashboard.py`** — stub:
```python
import streamlit as st
from fala_gavea.workspace import FalaGaveaWorkspace


def render(workspace: FalaGaveaWorkspace, user_id: str) -> None:
    st.header("Dashboard")
    st.info("Em construção — implementado no plan W2-2")
```

---

### Step 4 — Criar .gitignore

Criar `fala-gavea/.gitignore`:

```
.venv/
__pycache__/
*.db
*.pyc
.pytest_cache/
.ruff_cache/
```

---

### Step 5 — Instalar dependências e validar

Executar no diretório `fala-gavea/`:

```bash
uv sync
streamlit run app.py --server.headless true &
sleep 3
kill %1
```

O app deve iniciar sem erros de importação. Se `uv` não estiver disponível no diretório, verificar se o `.venv` existente precisa ser removido (foi criado com FastAPI).

**Validation:** `uv sync` completa sem erros; `streamlit run app.py` inicia sem `ImportError` ou `ModuleNotFoundError`.

---

## Acceptance Criteria

- [ ] `fala-gavea/pyproject.toml` contém `streamlit>=1.35` e não contém `fastapi`, `uvicorn`, `sqlalchemy`
- [ ] `fala-gavea/app.py` existe com geração de `user_id` e navegação por sidebar
- [ ] `fala-gavea/fala_gavea/workspace.py` existe com `FalaGaveaWorkspace._init_db()` criando as 3 tabelas
- [ ] Os 4 módulos de página existem com função `render(workspace, user_id)` stub
- [ ] `fala-gavea/.gitignore` exclui `.venv/` e `*.db`
- [ ] `uv sync` no diretório `fala-gavea/` completa sem erros
