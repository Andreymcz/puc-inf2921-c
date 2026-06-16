from __future__ import annotations

from dataclasses import dataclass

from fala_gavea_seguranca.domain.repositories.chat_repository import ChatMessageRepository
from fala_gavea_seguranca.infrastructure.vector_store.chroma_client import embed_text


@dataclass
class InsightPoint:
    session_id: str
    text: str
    x: float
    y: float


class GetChatInsights:
    def __init__(self, msg_repo: ChatMessageRepository) -> None:
        self._msg_repo = msg_repo

    def execute(self, session_ids: list[str] | None = None) -> list[InsightPoint]:
        try:
            import numpy as np
            from umap import UMAP
        except ImportError as e:
            raise RuntimeError("umap-learn e numpy são necessários para insights") from e

        # Collect all user messages across sessions
        messages = []
        if session_ids:
            for sid in session_ids:
                for m in self._msg_repo.find_by_session(sid):
                    if m.role == "user":
                        messages.append(m)
        else:
            # No filter — caller should pass aggregated repo or limit
            return []

        if len(messages) < 2:
            # UMAP needs at least 2 points
            return [
                InsightPoint(session_id=m.session_id, text=m.content, x=float(i), y=0.0)
                for i, m in enumerate(messages)
            ]

        embeddings = [embed_text(m.content) for m in messages]
        arr = np.array(embeddings)

        n_neighbors = min(15, len(messages) - 1)
        reducer = UMAP(n_components=2, n_neighbors=n_neighbors, random_state=42)
        coords = reducer.fit_transform(arr)

        return [
            InsightPoint(session_id=m.session_id, text=m.content, x=float(coords[i, 0]), y=float(coords[i, 1]))
            for i, m in enumerate(messages)
        ]
