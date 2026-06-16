from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from fala_gavea_seguranca.domain.entities.chat import ChatMessage, ChatSession
from fala_gavea_seguranca.domain.repositories.chat_repository import ChatMessageRepository, ChatSessionRepository


@dataclass
class CreateChatSessionInput:
    title: str


class CreateChatSession:
    def __init__(self, repo: ChatSessionRepository) -> None:
        self._repo = repo

    def execute(self, inp: CreateChatSessionInput) -> ChatSession:
        session = ChatSession(
            id=str(uuid.uuid4()),
            title=inp.title,
            created_at=datetime.now(tz=timezone.utc),
        )
        return self._repo.save(session)


class ListChatSessions:
    def __init__(self, repo: ChatSessionRepository) -> None:
        self._repo = repo

    def execute(self) -> list[ChatSession]:
        return self._repo.find_all()


class GetChatSession:
    def __init__(self, repo: ChatSessionRepository) -> None:
        self._repo = repo

    def execute(self, session_id: str) -> ChatSession | None:
        return self._repo.find_by_id(session_id)


class GetChatMessages:
    def __init__(self, repo: ChatMessageRepository) -> None:
        self._repo = repo

    def execute(self, session_id: str) -> list[ChatMessage]:
        return self._repo.find_by_session(session_id)
