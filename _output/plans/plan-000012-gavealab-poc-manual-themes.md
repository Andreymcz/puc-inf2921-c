# Plan 000012 | FEATURE-X | 2026-06-01 22:44 | GaveaLab PoC -- Manual theme categorization | Review: light
plan_format_version: 1

## Revision note
Revised 2026-06-01 23:10 UTC: render() receives workspace; result persisted via
session.save_result("manual_categories", ...); territory included in result rows.

## Brief (verbatim)
Implement the "Categorizar por temas" tool: user types theme names; LLM categorizes each
comment against those themes and returns the matching comments per theme.
(Wave 2, parallel with plan-000013. Depends on plan-000011.)

## Files
- `gavealab-poc/gavealab_poc/pipeline/manual_categories.py` (create)
- `gavealab-poc/gavealab_poc/pages/manual_topics.py` (replace stub)

## Steps

### Step 1 -- pipeline/manual_categories.py

```python
from __future__ import annotations
import json
from gavealab_poc.llm import chat
from gavealab_poc.workspace import AnalysisSession
from gavealab_poc.pipeline.topics import _extract_json

SYSTEM_PROMPT = (
    "You are a JSON generator. You MUST respond with ONLY valid JSON. "
    "No text before or after the JSON."
)


def categorize_by_themes(session: AnalysisSession, themes: list[str]) -> dict[str, list[dict]]:
    """Classify each comment into one or more user-provided themes via LLM.

    Returns and persists {theme_name: [{id, text, territory, reason}, ...]}
    Territory is included when the column exists in session.df.
    """
    themes_str = ", ".join(themes)
    has_territory = "territory" in session.df.columns
    result: dict[str, list[dict]] = {t: [] for t in themes}

    for _, row in session.df.iterrows():
        text = str(row["text"])
        if len(text) < 10:
            continue
        prompt = (
            f"The following themes are available: {themes_str}.\n"
            f"Given this comment, identify which themes it belongs to (may be multiple or none).\n"
            "Return ONLY valid JSON: "
            '{"themes": [{"theme": "string", "reason": "string"}]}\n\n'
            f"Comment: {text}"
        )
        raw = chat(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]
        )
        matched = _parse_theme_matches(raw, themes)
        entry: dict = {"id": str(row["id"]), "text": text}
        if has_territory:
            entry["territory"] = str(row["territory"])
        for match in matched:
            theme = match["theme"]
            if theme in result:
                result[theme].append({**entry, "reason": match.get("reason", "")})

    session.save_result("manual_categories", result)
    return result


def _parse_theme_matches(raw: str, valid_themes: list[str]) -> list[dict]:
    try:
        obj = _extract_json(raw)
        matches = obj.get("themes", []) if isinstance(obj, dict) else []
        return [m for m in matches if isinstance(m, dict) and m.get("theme") in valid_themes]
    except Exception:
        return []
```

### Step 2 -- pages/manual_topics.py

```python
from __future__ import annotations
import streamlit as st
import pandas as pd
from gavealab_poc.workspace import GaveaLabWorkspace


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("3. Categorizar por temas")
    session = st.session_state.get("session")
    if session is None:
        st.warning("Crie ou carregue uma sessao na pagina 'Upload CSV'.")
        return

    st.markdown(
        "Digite os temas que deseja usar para categorizar os relatos. "
        "O sistema classificara cada relato nos temas correspondentes."
    )

    themes_input = st.text_area(
        "Temas (um por linha)",
        placeholder="Mobilidade urbana\nSaude publica\nSeguranca\nEducacao",
        height=150,
    )
    themes = [t.strip() for t in themes_input.splitlines() if t.strip()]

    if not themes:
        st.info("Digite ao menos um tema acima.")
        return

    if st.button("Categorizar relatos"):
        with st.spinner("Categorizando com Ollama..."):
            try:
                from gavealab_poc.pipeline.manual_categories import categorize_by_themes
                categorize_by_themes(session, themes)
                st.session_state.session = session
            except Exception as exc:
                st.error(f"Erro: {exc}")
                return

    if not session.manual_categories:
        return

    st.success("Categorias salvas.")
    for theme, items in session.manual_categories.items():
        with st.expander(f"**{theme}** -- {len(items)} relatos"):
            if items:
                cols = ["territory", "text", "reason"] if items and "territory" in items[0] else ["text", "reason"]
                st.dataframe(pd.DataFrame(items)[cols], use_container_width=True)
            else:
                st.write("Nenhum relato classificado neste tema.")
```

### Step 3 -- Verify
Upload `tttc-poc/data/sample-gavealab.csv`, navigate to "Categorizar por temas",
enter themes: `Seguranca, Saude, Infraestrutura, Meio ambiente`. Click button.
Confirm territory (asfalto/favela) appears in each theme's table.
Reload app -- confirm categories reload from SQLite.

## Commit
```
feat(gavealab-poc): manual theme categorization tool, persisted to SQLite
```

## Review log
| Perspective | Status | Notes |
|-------------|--------|-------|
| UX | Adopted | Territory column shown when present; reason column shows LLM rationale |
| DATA | Adopted | territory propagated to result rows when present in df |
