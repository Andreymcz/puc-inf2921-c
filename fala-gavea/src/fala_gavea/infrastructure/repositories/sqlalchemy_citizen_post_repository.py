from __future__ import annotations

from datetime import UTC, datetime
from typing import cast

from sqlalchemy.orm import Session

from ...domain.entities.citizen_post import CitizenPost, LikeRecord, TerritoryLevel
from ...domain.repositories.citizen_post_repository import CitizenPostRepository
from ..database.models import CitizenPostModel, LikeModel


class SQLAlchemyCitizenPostRepository(CitizenPostRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, entity: CitizenPost) -> CitizenPost:
        model = self._to_model(entity)
        self._session.merge(model)
        self._session.commit()
        return entity

    def find_by_id(self, id: str) -> CitizenPost | None:
        model = self._session.get(CitizenPostModel, id)
        return self._to_entity(model) if model else None

    def find_all(self, limit: int = 50, offset: int = 0) -> list[CitizenPost]:
        models = (
            self._session.query(CitizenPostModel)
            .order_by(CitizenPostModel.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]

    def delete(self, id: str) -> bool:
        model = self._session.get(CitizenPostModel, id)
        if model is None:
            return False
        self._session.delete(model)
        self._session.commit()
        return True

    def add_like(self, post_id: str, user_id: str) -> CitizenPost:
        post = self._session.get(CitizenPostModel, post_id)
        if post is None:
            raise ValueError(f"Post {post_id} not found")
        existing = self._session.get(LikeModel, (user_id, post_id))
        if existing:
            return self._to_entity(post)
        like = LikeModel(user_id=user_id, post_id=post_id, created_at=datetime.now(UTC))
        post.likes_count = (post.likes_count or 0) + 1
        self._session.add(like)
        self._session.commit()
        self._session.refresh(post)
        return self._to_entity(post)

    def remove_like(self, post_id: str, user_id: str) -> CitizenPost:
        post = self._session.get(CitizenPostModel, post_id)
        if post is None:
            raise ValueError(f"Post {post_id} not found")
        like = self._session.get(LikeModel, (user_id, post_id))
        if like:
            self._session.delete(like)
            post.likes_count = max(0, (post.likes_count or 0) - 1)
            self._session.commit()
            self._session.refresh(post)
        return self._to_entity(post)

    def has_liked(self, post_id: str, user_id: str) -> bool:
        return self._session.get(LikeModel, (user_id, post_id)) is not None

    def get_likes(self, post_id: str) -> list[LikeRecord]:
        likes = (
            self._session.query(LikeModel)
            .filter(LikeModel.post_id == post_id)
            .all()
        )
        return [
            LikeRecord(user_id=cast(str, like.user_id), created_at=cast(datetime, like.created_at))
            for like in likes
        ]

    def set_label_feedback(self, post_id: str, label: str, approved: bool, user_id: str) -> CitizenPost:
        post = self._session.get(CitizenPostModel, post_id)
        if post is None:
            raise ValueError(f"Post {post_id} not found")
        feedback = dict(post.label_feedback or {})
        feedback[label] = {"approved": approved, "user_id": user_id}
        post.label_feedback = feedback
        self._session.commit()
        self._session.refresh(post)
        return self._to_entity(post)

    @staticmethod
    def _to_entity(model: CitizenPostModel) -> CitizenPost:
        return CitizenPost(
            id=model.id,
            text=model.text,
            territory_level=TerritoryLevel(model.territory_level),
            territory_name=model.territory_name,
            author_id=model.author_id,
            created_at=model.created_at,
            ai_labels=model.ai_labels or [],
            label_feedback=model.label_feedback or {},
            likes_count=model.likes_count or 0,
        )

    @staticmethod
    def _to_model(entity: CitizenPost) -> CitizenPostModel:
        return CitizenPostModel(
            id=entity.id,
            text=entity.text,
            territory_level=entity.territory_level,
            territory_name=entity.territory_name,
            author_id=entity.author_id,
            created_at=entity.created_at,
            ai_labels=entity.ai_labels,
            label_feedback=entity.label_feedback,
            likes_count=entity.likes_count,
        )
