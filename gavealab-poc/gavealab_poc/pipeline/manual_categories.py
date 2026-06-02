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
