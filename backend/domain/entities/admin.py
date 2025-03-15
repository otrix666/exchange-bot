from dataclasses import dataclass

from backend.domain.entities.card import Card
from backend.domain.entities.order import BuyOrder, SellOrder
from backend.domain.entities.user import User


@dataclass(slots=True)
class FullSellOrder:
    order: SellOrder
    user: User


@dataclass(slots=True)
class FullBuyOrder:
    order: BuyOrder
    user: User
    card: Card
