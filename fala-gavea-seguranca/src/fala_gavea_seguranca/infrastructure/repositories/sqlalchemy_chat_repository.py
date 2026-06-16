from __future__ import annotations

from sqlalchemy.orm import Session

from fala_gavea_seguranca.domain.entities.chat import ChatMessage, ChatSession
from fala_gavea_seguranca.domain.repositories.chat_repository import ChatMessageRepository, ChatSessionRepository
from fala_gavea_seguranca.infrastructure.database.models import ChatMessageModel, ChatSessionModel


def _session_to_entity(m: ChatSessionModel) -> ChatSession:
    return ChatSession(id=m.id, title=m.title, created_at=m.created_at)


def _message_to_entity(m: ChatMessageModel) -> ChatMessage:
    return ChatMessage(
        id=m.id,
        session_id=m.session_id,
        role=m.role,
        content=m.content,
        created_at=m.created_at,
        sources=m.sources or [],
    )


class SQLAlchemyChatSessionRepository(ChatSessionRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def save(self, session: ChatSession) -> ChatSession:
        model = ChatSessionModel(id=session.id, title=session.title, created_at=session.created_at)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _session_to_entity(model)

    def find_all(self) -> list[ChatSession]:
        models = self._db.query(ChatSessionModel).order_by(ChatSessionModel.created_at.desc()).all()
        return [_session_to_entity(m) for m in models]

    def find_by_id(self, session_id: str) -> ChatSession | None:
        m = self._db.query(ChatSessionModel).filter(ChatSessionModel.id == session_id).first()
        return _session_to_entity(m) if m else None

    def delete(self, session_id: str) -> None:
        self._db.query(ChatMessageModel).filter(ChatMessageModel.session_id == session_id).delete()
        self._db.query(ChatSessionModel).filter(ChatSessionModel.id == session_id).delete()
        self._db.commit()


class SQLAlchemyChatMessageRepository(ChatMessageRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def save(self, message: ChatMessage) -> ChatMessage:
        model = ChatMessageModel(
            id=message.id,
            session_id=message.session_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
            sources=message.sources,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _message_to_entity(model)

    def find_by_session(self, session_id: str) -> list[ChatMessage]:
        models = (
            self._db.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == session_id)
            .order_by(ChatMessageModel.created_at)
            .all()
        )
        return [_message_to_entity(m) for m in models]
