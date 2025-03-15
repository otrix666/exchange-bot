from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from backend.domain.entities.admin import FullBuyOrder
from backend.domain.entities.order import BuyOrder


class BuyOrderReader(Protocol):
    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> BuyOrder: ...

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> Sequence[FullBuyOrder]: ...

    @abstractmethod
    async def get_all(self) -> Sequence[BuyOrder]: ...

    @abstractmethod
    async def get_full_info(self, order_id: UUID) -> FullBuyOrder: ...


class BuyOrderSaver(Protocol):
    @abstractmethod
    async def save(self, order: BuyOrder) -> BuyOrder: ...


class BuyOrderUpdater(Protocol):
    @abstractmethod
    async def update(self, order: BuyOrder) -> None: ...
