from __future__ import annotations

from typing import Generator

from sqlalchemy.orm import Session

from ...infrastructure.database.session import SessionLocal
from ...infrastructure.repositories.sqlalchemy_citizen_post_repository import (
    SQLAlchemyCitizenPostRepository,
)


def get_citizen_post_repo() -> Generator[SQLAlchemyCitizenPostRepository, None, None]:
    db: Session = SessionLocal()
    try:
        yield SQLAlchemyCitizenPostRepository(db)
    finally:
        db.close()
