from __future__ import annotations

from abc import ABC, abstractmethod

from fala_gavea_seguranca.domain.entities.chat import ChatMessage, ChatSession


class ChatSessionRepository(ABC):
    @abstractmethod
    def save(self, session: ChatSession) -> ChatSession: ...

    @abstractmethod
    def find_all(self) -> list[ChatSession]: ...

    @abstractmethod
    def find_by_id(self, session_id: str) -> ChatSession | None: ...

    @abstractmethod
    def delete(self, session_id: str) -> None: ...


class ChatMessageRepository(ABC):
    @abstractmethod
    def save(self, message: ChatMessage) -> ChatMessage: ...

    @abstractmethod
    def find_by_session(self, session_id: str) -> list[ChatMessage]: ...
