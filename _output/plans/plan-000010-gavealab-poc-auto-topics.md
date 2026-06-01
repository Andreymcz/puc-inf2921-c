# Plan 000010 | FEATURE-X | 2026-06-01 22:44 | GaveaLab PoC -- Auto topic tree generation | Review: light
plan_format_version: 1

## Revision note
Revised 2026-06-01 23:10 UTC: render() receives workspace; result persisted via
session.save_result("topic_tree", ...); uses df["text"] canonical column.

## Brief (verbatim)
Implement automatic topic/subtopic generation from CSV comments (LLM pipeline step 1).
Renders results in the "Temas automaticos" page.
(Wave 1, step 2 of roadmap-000007. Depends on plan-000009.)

## Files
- `gavealab-poc/gavealab_poc/pipeline/topics.py` (create)
- `gavealab-poc/gavealab_poc/pages/auto_topics.py` (replace stub)

## Steps

### Step 1 -- pipeline/topics.py

```python
from __future__ import annotations
import json
from gavealab_poc.llm import chat
from gavealab_poc.workspace import AnalysisSession

SYSTEM_PROMPT = (
    "You are a JSON generator. You MUST respond with ONLY valid JSON. "
    "No text before or after the JSON. Each topic MUST have at least one subtopic."
)

USER_PROMPT_PREFIX = (
    "I will give you a list of comments. "
    "Please propose a way to organize the information contained in these comments "
    "into topics and subtopics of interest. "
    "Keep the topic and subtopic names very concise and use the short description "
    "to explain what the topic is about.\n\n"
    "Return a JSON object in this EXACT structure:\n"
    '{"taxonomy": [{"topicName": "string", "topicShortDescription": "string", '
    '"subtopics": [{"subtopicName": "string", "subtopicShortDescription": "string"}]}]}\n\n'
    "Comments:\n"
)


def generate_topic_tree(session: AnalysisSession) -> list[dict]:
    """Call Ollama to generate a topic/subtopic taxonomy from all comments.

    Persists the result via session.save_result and returns the topic list.
    """
    comment_block = "\n".join(
        row["text"] for _, row in session.df.iterrows() if len(row["text"]) >= 10
    )
    raw = chat(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_PREFIX + comment_block},
        ]
    )
    tree = _parse_taxonomy(raw)
    session.save_result("topic_tree", tree)
    return tree


def _parse_taxonomy(raw: str) -> list[dict]:
    try:
        obj = _extract_json(raw)
        taxonomy = obj.get("taxonomy", []) if isinstance(obj, dict) else []
    except Exception:
        taxonomy = []
    for topic in taxonomy:
        if not isinstance(topic.get("subtopics"), list) or len(topic["subtopics"]) == 0:
            topic["subtopics"] = [
                {"subtopicName": "Geral", "subtopicShortDescription": "Aspectos gerais"}
            ]
    return taxonomy


def _extract_json(text: str) -> dict:
    """Best-effort JSON extraction: try full text, then first {...} block."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(text[start:end])
    raise ValueError("No JSON object found in response")
```

### Step 2 -- pages/auto_topics.py

```python
from __future__ import annotations
import streamlit as st
from gavealab_poc.workspace import GaveaLabWorkspace


def render(workspace: GaveaLabWorkspace) -> None:
    st.header("2. Temas automaticos")
    session = st.session_state.get("session")
    if session is None:
        st.warning("Crie ou carregue uma sessao na pagina 'Upload CSV'.")
        return

    if st.button("Gerar temas com IA"):
        with st.spinner("Analisando relatos com Ollama..."):
            try:
                from gavealab_poc.pipeline.topics import generate_topic_tree
                generate_topic_tree(session)
                st.session_state.session = session
            except Exception as exc:
                st.error(f"Erro ao chamar Ollama: {exc}")
                return

    if not session.topic_tree:
        st.info("Clique em 'Gerar temas' para iniciar a analise.")
        return

    st.success(f"{len(session.topic_tree)} temas identificados. Resultado salvo.")
    for topic in session.topic_tree:
        with st.expander(
            f"**{topic['topicName']}** -- {topic.get('topicShortDescription', '')}"
        ):
            for sub in topic.get("subtopics", []):
                st.markdown(
                    f"- **{sub['subtopicName']}**: {sub.get('subtopicShortDescription', '')}"
                )
```

### Step 3 -- Verify
Upload `tttc-poc/data/sample-gavealab.csv`, click "Gerar temas".
Confirm topics render as expandable sections. Reload the page -- topics must still be shown
(loaded from SQLite via session.topic_tree, which was set by save_result).

## Commit
```
feat(gavealab-poc): auto topic tree generation via Ollama, persisted to SQLite
```

## Review log
| Perspective | Status | Notes |
|-------------|--------|-------|
| ARCH | Adopted | Pipeline function is pure Python; no Streamlit dependency |
| DATA | Adopted | Uses df["text"] canonical column set by workspace._parse_csv |
| DX | Adopted | Type annotations on all public functions |
