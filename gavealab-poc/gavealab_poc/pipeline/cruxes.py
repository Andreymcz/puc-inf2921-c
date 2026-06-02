from __future__ import annotations
import json
import numpy as np
from gavealab_poc.embeddings import embed
from gavealab_poc.llm import chat
from gavealab_poc.workspace import AnalysisSession
from gavealab_poc.pipeline.topics import _extract_json

# Cosine distance threshold above which a subtopic is considered divergent.
# (distance = 1 - cosine_similarity; 0.25 ~= moderate divergence)
DIVERGENCE_THRESHOLD = 0.10

SYSTEM_PROMPT = (
    "You are a JSON generator. You MUST respond with ONLY valid JSON. "
    "No text before or after the JSON."
)

LABEL_PROMPT_TMPL = (
    "Two groups of citizens disagree about the topic '{topic} / {subtopic}'.\n\n"
    "Group A ({group_a}) says:\n{claims_a}\n\n"
    "Group B ({group_b}) says:\n{claims_b}\n\n"
    "Write ONE sentence that captures the core point of disagreement between these groups. "
    "Be specific and controversial — this is the crux.\n\n"
    'Return ONLY valid JSON: {{"cruxClaim": "string", "explanation": "string"}}'
)


def detect_cruxes(session: AnalysisSession) -> tuple[list[dict], list[dict]]:
    """Detect crux claims using embedding-based divergence detection.

    Algorithm:
    1. Embed all claims with multilingual-e5-large.
    2. Per subtopic: compute centroid per territory group.
    3. If cosine distance between centroids > DIVERGENCE_THRESHOLD, flag as divergent.
    4. For divergent subtopics only, ask Ollama for a one-sentence crux label.

    Returns (cruxes, diagnostics). Persists cruxes via session.save_result.
    Each crux dict: {topic, subtopic, cruxClaim, explanation, agree, disagree, cosine_distance}
    Each diagnostics dict: {topic, subtopic, cosine_distance, groups, divergent}
    """
    if not session.claims_tree:
        raise ValueError("Extraia os claims primeiro ('Extrair claims').")

    cruxes: list[dict] = []
    diagnostics: list[dict] = []

    for topic, subtopics in session.claims_tree.items():
        for subtopic, claims in subtopics.items():
            groups = _build_groups(claims)
            if len(groups) < 2:
                diagnostics.append({
                    "topic": topic, "subtopic": subtopic,
                    "cosine_distance": None, "groups": list(groups.keys()),
                    "divergent": False, "reason": "single group",
                })
                continue

            group_names = list(groups.keys())
            # Only handle binary divergence (two groups) for simplicity
            g_a, g_b = group_names[0], group_names[1]
            claims_a = [c["claim"] for c in groups[g_a]]
            claims_b = [c["claim"] for c in groups[g_b]]

            dist = _group_cosine_distance(claims_a, claims_b)
            divergent = dist >= DIVERGENCE_THRESHOLD
            diagnostics.append({
                "topic": topic, "subtopic": subtopic,
                "cosine_distance": round(dist, 4), "groups": [g_a, g_b],
                "divergent": divergent, "reason": f"dist={dist:.4f} threshold={DIVERGENCE_THRESHOLD}",
            })

            if not divergent:
                continue

            crux = _label_crux(topic, subtopic, g_a, claims_a, g_b, claims_b)
            if crux:
                crux.update({
                    "topic": topic,
                    "subtopic": subtopic,
                    "agree": [g_a],
                    "disagree": [g_b],
                    "cosine_distance": round(dist, 3),
                })
                cruxes.append(crux)

    session.save_result("cruxes", cruxes)
    return cruxes, diagnostics


def _build_groups(claims: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for c in claims:
        key = c.get("territory") or c.get("commentId", "?")
        groups.setdefault(key, []).append(c)
    return groups


def _group_cosine_distance(claims_a: list[str], claims_b: list[str]) -> float:
    """Cosine distance (1 - similarity) between the centroids of two claim sets."""
    emb_a = embed(claims_a).mean(axis=0)
    emb_b = embed(claims_b).mean(axis=0)
    # Embeddings are already L2-normalised; dot product == cosine similarity
    similarity = float(np.dot(emb_a, emb_b))
    return 1.0 - similarity


def _label_crux(
    topic: str, subtopic: str,
    g_a: str, claims_a: list[str],
    g_b: str, claims_b: list[str],
) -> dict | None:
    """Ask Ollama to produce a one-sentence crux label for the divergent pair."""
    prompt = LABEL_PROMPT_TMPL.format(
        topic=topic, subtopic=subtopic,
        group_a=g_a, claims_a="\n".join(f"- {c}" for c in claims_a),
        group_b=g_b, claims_b="\n".join(f"- {c}" for c in claims_b),
    )
    for _ in range(3):  # up to 3 retries for JSON parse failures
        raw = chat(messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ])
        try:
            obj = _extract_json(raw)
            if isinstance(obj, dict) and "cruxClaim" in obj:
                return obj
        except Exception:
            pass
    return None
