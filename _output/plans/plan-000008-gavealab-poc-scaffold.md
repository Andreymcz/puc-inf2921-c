# Plan 000008 | FEATURE-X | 2026-06-01 22:44 | GaveaLab PoC -- Scaffold, Streamlit skeleton, Ollama client | Review: light
# DONE | 2026-06-01 23:45 UTC |
plan_format_version: 1

## Revision note
Revised after initial generation (2026-06-01 23:10 UTC): switched from requirements.txt to uv/pyproject.toml;
updated CSV schema to match sample-gavealab.csv (columns: id, comment, territory);
introduced GaveaLabWorkspace with SQLite persistence for sessions and analysis results.

## Brief (verbatim)
Scaffold the gavealab-poc Streamlit PoC: project structure, uv pyproject.toml, Streamlit entry point,
Ollama client wrapper, GaveaLabWorkspace (SQLite-backed), and AnalysisSession data model.
(Wave 0 of roadmap-000007)

## Agent Interpretation
Create the directory layout, `pyproject.toml` (uv), `app.py` (multi-page Streamlit shell),
`gavealab_poc/llm.py` (Ollama OpenAI-compatible wrapper), `gavealab_poc/workspace.py`
(GaveaLabWorkspace + AnalysisSession with SQLite persistence), and stub page modules.

Reference CSV: `tttc-poc/data/sample-gavealab.csv` (columns: id, comment, territory).
The `comment` column maps to the text to analyse; `territory` is metadata (asfalto / favela).

## Files
- `gavealab-poc/pyproject.toml` (create)
- `gavealab-poc/app.py` (create)
- `gavealab-poc/gavealab_poc/__init__.py` (create)
- `gavealab-poc/gavealab_poc/llm.py` (create)
- `gavealab-poc/gavealab_poc/workspace.py` (create)
- `gavealab-poc/gavealab_poc/pipeline/__init__.py` (create)
- `gavealab-poc/gavealab_poc/pages/__init__.py` (create)
- `gavealab-poc/gavealab_poc/pages/upload.py` (create -- stub)
- `gavealab-poc/gavealab_poc/pages/auto_topics.py` (create -- stub)
- `gavealab-poc/gavealab_poc/pages/manual_topics.py` (create -- stub)
- `gavealab-poc/gavealab_poc/pages/cruxes.py` (create -- stub)

## Steps

### Step 1 -- Create directory skeleton
Create directories:
```
gavealab-poc/
gavealab-poc/gavealab_poc/
gavealab-poc/gavealab_poc/pipeline/
gavealab-poc/gavealab_poc/pages/
```

### Step 2 -- pyproject.toml
Use uv as the package manager. No requirements.txt.

```toml
[project]
name = "gavealab-poc"
version = "0.1.0"
description = "GaveaLab citizen claims analysis PoC -- Streamlit + Ollama"
requires-python = ">=3.11"
dependencies = [
    "streamlit>=1.35",
    "pandas>=2.2",
    "openai>=1.30",
]

[project.optional-dependencies]
dev = []

[tool.uv]
dev-dependencies = []
```

Install with: `uv sync` (from `gavealab-poc/` directory).
Run with: `uv run streamlit run app.py`

### Step 3 -- gavealab_poc/llm.py
Thin Ollama wrapper. Connects to the same Ollama instance used by tttc-poc.

```python
from __future__ import annotations
import os
from openai import OpenAI

OLLAMA_BASE_URL: str = os.getenv("GAVEALAB_OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL: str = os.getenv("GAVEALAB_OLLAMA_MODEL", "qwen3:8b")


def get_client() -> OpenAI:
    """Return an OpenAI-compatible client pointed at the local Ollama instance."""
    return OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


def chat(messages: list[dict], model: str = OLLAMA_MODEL, temperature: float = 0.0) -> str:
    """Send messages to Ollama and return the text content of the first choice.

    Sets think=False to disable thinking mode for speed (matches tttc-poc behavior).
    """
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        extra_body={"think": False},
    )
    return response.choices[0].message.content
```

### Step 4 -- gavealab_poc/workspace.py
Central access point. `GaveaLabWorkspace` manages SQLite persistence; `AnalysisSession`
is a thin domain object that delegates persistence to the workspace.

#### SQLite schema

Three tables:

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    csv_raw TEXT NOT NULL,          -- full CSV file contents (UTF-8)
    created_at TEXT NOT NULL        -- ISO-8601
);

CREATE TABLE IF NOT EXISTS results (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL REFERENCES sessions(id),
    result_type TEXT NOT NULL,      -- 'topic_tree' | 'claims_tree' | 'cruxes' | 'manual_categories'
    result_json TEXT NOT NULL,      -- JSON-serialized result
    created_at  TEXT NOT NULL
);
```

#### Implementation

```python
from __future__ import annotations
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


# ------------------------------------------------------------------
# Workspace
# ------------------------------------------------------------------

class GaveaLabWorkspace:
    """Central access point for GaveaLab PoC persistence.

    Manages a SQLite database at `db_path`. All sessions and their
    analysis results are stored here.

    Usage:
        ws = GaveaLabWorkspace("gavealab.db")
        session = ws.create_session("Gavea 2026", csv_file)
        session.save_result("topic_tree", tree_list)
    """

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = Path(db_path)
        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._migrate()

    # ------------------------------------------------------------------
    # Schema migration
    # ------------------------------------------------------------------

    def _migrate(self) -> None:
        cur = self._conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL,
                csv_raw    TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS results (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  INTEGER NOT NULL REFERENCES sessions(id),
                result_type TEXT NOT NULL,
                result_json TEXT NOT NULL,
                created_at  TEXT NOT NULL
            );
        """)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def create_session(self, name: str, csv_file) -> "AnalysisSession":
        """Create a new AnalysisSession from an uploaded CSV file object.

        Persists the raw CSV content immediately. Returns the session.
        """
        csv_raw = csv_file.read()
        if isinstance(csv_raw, bytes):
            csv_raw = csv_raw.decode("utf-8")
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO sessions (name, csv_raw, created_at) VALUES (?, ?, ?)",
            (name, csv_raw, _now()),
        )
        self._conn.commit()
        session_id = cur.lastrowid
        df = _parse_csv(csv_raw)
        return AnalysisSession(session_id=session_id, name=name, df=df, _workspace=self)

    def load_session(self, session_id: int) -> "AnalysisSession":
        """Reload a previously created session including all saved results."""
        row = self._conn.execute(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()
        if row is None:
            raise ValueError(f"Session {session_id} not found.")
        df = _parse_csv(row["csv_raw"])
        session = AnalysisSession(
            session_id=session_id, name=row["name"], df=df, _workspace=self
        )
        for res in self._conn.execute(
            "SELECT result_type, result_json FROM results WHERE session_id = ? ORDER BY id",
            (session_id,),
        ):
            setattr(session, res["result_type"], json.loads(res["result_json"]))
        return session

    def list_sessions(self) -> list[dict]:
        """Return a list of {id, name, created_at} dicts for all sessions."""
        rows = self._conn.execute(
            "SELECT id, name, created_at FROM sessions ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    def save_result(self, session_id: int, result_type: str, value: Any) -> None:
        """Persist an analysis result for a session. Overwrites if same type exists."""
        self._conn.execute(
            "DELETE FROM results WHERE session_id = ? AND result_type = ?",
            (session_id, result_type),
        )
        self._conn.execute(
            "INSERT INTO results (session_id, result_type, result_json, created_at) VALUES (?, ?, ?, ?)",
            (session_id, result_type, json.dumps(value, ensure_ascii=False), _now()),
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


# ------------------------------------------------------------------
# AnalysisSession
# ------------------------------------------------------------------

@dataclass
class AnalysisSession:
    """In-memory representation of one analysis session.

    Persists results to SQLite via its parent GaveaLabWorkspace whenever
    save_result() is called.
    """
    session_id: int
    name: str
    df: pd.DataFrame
    _workspace: GaveaLabWorkspace
    topic_tree: list[dict] = field(default_factory=list)
    claims_tree: dict[str, Any] = field(default_factory=dict)
    cruxes: list[dict] = field(default_factory=list)
    manual_categories: dict[str, list[dict]] = field(default_factory=dict)

    def save_result(self, result_type: str, value: Any) -> None:
        """Persist a result and update the in-memory field atomically."""
        setattr(self, result_type, value)
        self._workspace.save_result(self.session_id, result_type, value)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_csv(csv_raw: str) -> pd.DataFrame:
    """Parse raw CSV text into a normalized DataFrame.

    Normalizes column names: 'comment' -> 'text' (internal canonical name).
    Required: at least one of 'text' or 'comment' columns must be present.
    Optional columns: 'id', 'territory' (any extra columns are kept as metadata).
    """
    import io
    df = pd.read_csv(io.StringIO(csv_raw))

    # normalize text column
    if "comment" in df.columns and "text" not in df.columns:
        df = df.rename(columns={"comment": "text"})
    if "text" not in df.columns:
        raise ValueError("CSV must contain a 'comment' or 'text' column.")

    if "id" not in df.columns:
        df.insert(0, "id", [f"c{i+1}" for i in range(len(df))])
    df["id"] = df["id"].astype(str)
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"].str.len() >= 10].reset_index(drop=True)
    return df
```

### Step 5 -- app.py (Streamlit entry point)
Multi-page shell. Initializes `GaveaLabWorkspace` once per process using `st.cache_resource`.

```python
from __future__ import annotations
import streamlit as st
from gavealab_poc.workspace import GaveaLabWorkspace

st.set_page_config(page_title="GaveaLab -- Analise de Relatos", layout="wide")
st.title("GaveaLab -- Analise de Relatos de Cidadaos")


@st.cache_resource
def get_workspace() -> GaveaLabWorkspace:
    return GaveaLabWorkspace("gavealab.db")


workspace = get_workspace()

if "session" not in st.session_state:
    st.session_state.session = None

page = st.sidebar.radio(
    "Navegacao",
    ["Upload CSV", "Temas automaticos", "Categorizar por temas", "Opinioes divergentes"],
)

if page == "Upload CSV":
    from gavealab_poc.pages.upload import render
elif page == "Temas automaticos":
    from gavealab_poc.pages.auto_topics import render
elif page == "Categorizar por temas":
    from gavealab_poc.pages.manual_topics import render
else:
    from gavealab_poc.pages.cruxes import render

render(workspace)
```

Each `render(workspace)` receives the workspace so pages can create/load sessions.

### Step 6 -- Stub page modules
Each stub accepts `workspace: GaveaLabWorkspace` and shows a placeholder.

`gavealab_poc/pages/upload.py`:
```python
import streamlit as st
from gavealab_poc.workspace import GaveaLabWorkspace

def render(workspace: GaveaLabWorkspace) -> None:
    st.info("Upload page -- to be implemented in plan-000009")
```

Same pattern for `auto_topics.py`, `manual_topics.py`, `cruxes.py`.

### Step 7 -- Smoke test
```
cd gavealab-poc
uv sync
uv run streamlit run app.py --server.headless true &
```
Wait 3 seconds, then `curl -s http://localhost:8501/` -- confirm HTTP 200.
Kill the background process. Confirm `gavealab.db` was created (workspace constructor
creates it on first connect).

### Step 8 -- Note for downstream plans
All downstream plans (000009--000013) must:
- Accept `workspace: GaveaLabWorkspace` in `render()` signature
- Call `session.save_result(result_type, value)` after each LLM analysis completes
- Use `df["text"]` as the canonical comment column (after CSV normalization in step 4)
- The sample CSV at `tttc-poc/data/sample-gavealab.csv` is the reference input for manual testing

## Commit
```
feat(gavealab-poc): scaffold Streamlit app with GaveaLabWorkspace, SQLite persistence, Ollama client
```

## Review log
| Perspective | Status | Notes |
|-------------|--------|-------|
| ARCH | Adopted | Workspace owns all SQLite access; AnalysisSession is a thin domain object |
| DATA | Adopted | CSV normalization maps 'comment' -> 'text'; 'territory' kept as metadata |
| DX | Adopted | uv for dependency management; type annotations on all public functions |
| SEC | Adopted | No secrets in code; Ollama API key is the literal string "ollama" (local only) |
| TEST | Deferred | No unit tests in scaffold; smoke test confirms app starts and db is created |
