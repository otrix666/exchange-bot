from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from backend.domain.entities.order import BuyOrder, SellOrder


class CsvCreator(Protocol):
    @staticmethod
    @abstractmethod
    def _generate_order_row(order: [SellOrder, BuyOrder]) -> list: ...

    @abstractmethod
    def create_report(self, orders: Sequence[SellOrder | BuyOrder]) -> bytes: ...
