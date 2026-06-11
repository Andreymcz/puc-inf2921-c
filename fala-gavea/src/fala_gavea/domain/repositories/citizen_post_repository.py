from __future__ import annotations

from abc import ABC, abstractmethod

from ..entities.citizen_post import CitizenPost, LikeRecord


class CitizenPostRepository(ABC):
    @abstractmethod
    def save(self, entity: CitizenPost) -> CitizenPost: ...

    @abstractmethod
    def find_by_id(self, id: str) -> CitizenPost | None: ...

    @abstractmethod
    def find_all(self, limit: int = 50, offset: int = 0) -> list[CitizenPost]: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...

    @abstractmethod
    def add_like(self, post_id: str, user_id: str) -> CitizenPost: ...

    @abstractmethod
    def remove_like(self, post_id: str, user_id: str) -> CitizenPost: ...

    @abstractmethod
    def has_liked(self, post_id: str, user_id: str) -> bool: ...

    @abstractmethod
    def get_likes(self, post_id: str) -> list[LikeRecord]: ...

    @abstractmethod
    def set_label_feedback(self, post_id: str, label: str, approved: bool, user_id: str) -> CitizenPost: ...
