from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from backend.domain.entities.card import Card


class CardReader(Protocol):
    @abstractmethod
    async def get_by_id(self, card_id: UUID) -> Card: ...

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> Sequence[Card]: ...


class CardSaver(Protocol):
    @abstractmethod
    async def save(self, card: Card) -> None: ...


class CardDeleter(Protocol):
    @abstractmethod
    async def delete_by_id(self, card: Card) -> None: ...
