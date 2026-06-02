# Plan 000011 | FEATURE-X | 2026-06-01 22:44 | GaveaLab PoC -- Claims extraction | Review: light
# DONE | 2026-06-02 00:41 UTC |
plan_format_version: 1

## Revision note
Revised 2026-06-01 23:10 UTC: render() receives workspace; result persisted via
session.save_result("claims_tree", ...); uses df["text"] canonical column;
territory kept as metadata in claim dict when present.

## Brief (verbatim)
Implement claims extraction: for each comment, extract one or more concise claims placed under
the topic/subtopic tree (LLM pipeline step 2). Results shown inline under each subtopic.
(Wave 1, step 3 of roadmap-000007. Depends on plan-000010.)

## Files
- `gavealab-poc/gavealab_poc/pipeline/claims.py` (create)
- `gavealab-poc/gavealab_poc/pages/auto_topics.py` (extend -- add claims section below topics)

## Steps

### Step 1 -- pipeline/claims.py

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
```

### Step 2 -- Extend pages/auto_topics.py
Append a "Claims por subtema" section below the existing topic expanders.

```python
# Add at the end of render(), after the topic tree section:

    st.divider()
    st.subheader("Claims por subtema")

    if st.button("Extrair claims (pode demorar)"):
        with st.spinner("Extraindo claims comentario por comentario..."):
            try:
                from gavealab_poc.pipeline.claims import extract_claims
                extract_claims(session)
                st.session_state.session = session
            except Exception as exc:
                st.error(f"Erro: {exc}")
                return

    if not session.claims_tree:
        st.info("Gere os temas e depois clique em 'Extrair claims'.")
        return

    import pandas as pd
    for topic, subtopics in session.claims_tree.items():
        st.markdown(f"### {topic}")
        for subtopic, claims in subtopics.items():
            with st.expander(f"{subtopic} ({len(claims)} claims)"):
                cols = ["claim", "quote", "territory"] if claims and "territory" in claims[0] else ["claim", "quote"]
                st.dataframe(pd.DataFrame(claims)[cols], use_container_width=True)
```

### Step 3 -- Verify
Upload `tttc-poc/data/sample-gavealab.csv`, generate topics, then extract claims.
- Confirm claims appear under subtopics with territory column (asfalto/favela).
- Reload the app; confirm claims_tree is restored from SQLite (button shows result without re-running).

## Commit
```
feat(gavealab-poc): claims extraction per comment, persisted to SQLite
```

## Review log
| Perspective | Status | Notes |
|-------------|--------|-------|
| DATA | Adopted | territory column propagated to claim dict when present |
| PERF | Adopted | One LLM call per comment -- warn user via button label |
| UX | Adopted | Territory column shown in claims table only when present |
