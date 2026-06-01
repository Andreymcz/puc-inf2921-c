from __future__ import annotations
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


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

    def create_session(self, name: str, csv_file: Any) -> "AnalysisSession":
        """Create a new AnalysisSession from an uploaded CSV file object."""
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


@dataclass
class AnalysisSession:
    """In-memory representation of one analysis session."""
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
