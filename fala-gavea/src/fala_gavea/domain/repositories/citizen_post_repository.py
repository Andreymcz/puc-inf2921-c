from __future__ import annotations

from abc import ABC, abstractmethod

from ..entities.citizen_post import CitizenPost


class CitizenPostRepository(ABC):
    @abstractmethod
    def save(self, entity: CitizenPost) -> CitizenPost: ...

    @abstractmethod
    def find_by_id(self, id: str) -> CitizenPost | None: ...

    @abstractmethod
    def find_all(self, limit: int = 50, offset: int = 0) -> list[CitizenPost]: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...
