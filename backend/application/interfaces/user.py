from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from backend.domain.entities.user import User


class UserReader(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User: ...

    @abstractmethod
    async def get_all(self) -> Sequence[User]: ...


class UserSaver(Protocol):
    @abstractmethod
    async def save_or_update(self, user: User) -> User: ...


class UserUpdater(Protocol):
    @abstractmethod
    async def update(self, user: User) -> None: ...


class AccessManager(Protocol):
    @staticmethod
    @abstractmethod
    def is_admin(user_id: int, admin_ids: list[int]) -> bool: ...

    @staticmethod
    @abstractmethod
    def is_operator(user_id: int, operator_ids: list[int]) -> bool: ...
