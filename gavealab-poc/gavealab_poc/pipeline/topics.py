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
