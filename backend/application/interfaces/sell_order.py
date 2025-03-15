from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from backend.domain.entities.admin import FullSellOrder
from backend.domain.entities.order import SellOrder


class SellOrderReader(Protocol):
    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> SellOrder: ...

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> Sequence[SellOrder]: ...

    @abstractmethod
    async def get_all(self) -> Sequence[SellOrder]: ...

    @abstractmethod
    async def get_full_info(self, order_id: UUID) -> FullSellOrder: ...


class SellOrderSaver(Protocol):
    @abstractmethod
    async def save(self, order: SellOrder) -> SellOrder: ...


class SellOrderUpdater(Protocol):
    @abstractmethod
    async def update(self, order: SellOrder) -> None: ...
