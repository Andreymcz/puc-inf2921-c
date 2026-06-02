from __future__ import annotations
import json
from gavealab_poc.llm import chat
from gavealab_poc.workspace import AnalysisSession
from gavealab_poc.pipeline.topics import _extract_json

SYSTEM_PROMPT = (
    "You are a JSON generator. You MUST respond with ONLY valid JSON. "
    "No text before or after the JSON."
)

USER_PROMPT_PREFIX = (
    "I'm going to give you a comment made by a participant and a list of topics and subtopics "
    "which have already been extracted.\n"
    "Extract a list of concise claims the participant may support, mapped to one of the given "
    "topics/subtopics. Each claim must be atomic and something others may disagree with. "
    "Also provide a short quote from the comment.\n\n"
    "Return ONLY valid JSON in this EXACT format:\n"
    '{"claims": [{"claim": "string", "quote": "string", '
    '"topicName": "string", "subtopicName": "string"}]}\n\n'
    "Topics/subtopics:\n"
)


def extract_claims(session: AnalysisSession) -> dict:
    """Extract claims from every comment using the session's topic_tree.

    Returns and persists a nested dict:
        {topicName: {subtopicName: [claim_dict, ...]}}

    Each claim_dict includes: claim, quote, topicName, subtopicName, commentId,
    and territory (if the column exists in session.df).
    Requires session.topic_tree to be populated first.
    """
    if not session.topic_tree:
        raise ValueError("Gere os temas primeiro ('Gerar temas com IA').")

    taxonomy_json = json.dumps(session.topic_tree)
    has_territory = "territory" in session.df.columns
    result: dict = {}

    for _, row in session.df.iterrows():
        text = str(row["text"])
        if len(text) < 10:
            continue
        raw = chat(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": USER_PROMPT_PREFIX + taxonomy_json + "\n\nComment:\n" + text,
                },
            ]
        )
        claims = _parse_claims(raw)
        for claim in claims:
            claim["commentId"] = str(row["id"])
            if has_territory:
                claim["territory"] = str(row["territory"])
            topic = claim.get("topicName", "Outros")
            subtopic = claim.get("subtopicName", "Geral")
            result.setdefault(topic, {}).setdefault(subtopic, []).append(claim)

    session.save_result("claims_tree", result)
    return result


def _parse_claims(raw: str) -> list[dict]:
    try:
        obj = _extract_json(raw)
        if isinstance(obj, list):
            return obj
        return obj.get("claims", []) if isinstance(obj, dict) else []
    except Exception:
        return []
