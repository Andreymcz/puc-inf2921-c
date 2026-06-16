from __future__ import annotations

from typing import Generator

from sqlalchemy.orm import Session

from ...infrastructure.database.session import SessionLocal
from ...infrastructure.repositories.sqlalchemy_chat_repository import (
    SQLAlchemyChatMessageRepository,
    SQLAlchemyChatSessionRepository,
)
from ...infrastructure.repositories.sqlalchemy_security_report_repository import (
    SQLAlchemySecurityReportRepository,
)


def get_security_report_repo() -> Generator[SQLAlchemySecurityReportRepository, None, None]:
    db: Session = SessionLocal()
    try:
        yield SQLAlchemySecurityReportRepository(db)
    finally:
        db.close()


def get_chat_session_repo() -> Generator[SQLAlchemyChatSessionRepository, None, None]:
    db: Session = SessionLocal()
    try:
        yield SQLAlchemyChatSessionRepository(db)
    finally:
        db.close()


def get_chat_message_repo() -> Generator[SQLAlchemyChatMessageRepository, None, None]:
    db: Session = SessionLocal()
    try:
        yield SQLAlchemyChatMessageRepository(db)
    finally:
        db.close()
