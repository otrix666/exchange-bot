from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from backend.domain.vo.requisites import CardRequisites, UsdtRequisites


class OrderStatus(StrEnum):
    CREATED = 'created'
    PAID = 'paid'
    CANCELED = 'canceled'
    COMPLETED = 'completed'


@dataclass
class Ticker(StrEnum):
    USDT_RUB = 'usdt/rub'
    RUB_USDT = 'rub/usdt'


@dataclass
class BuyOrder:
    id: UUID
    crypto_amount: Decimal
    fiat_amount: Decimal
    ticker: Ticker
    status: OrderStatus
    created_at: datetime
    completed_at: datetime | None
    note: str | None
    user_requisites: UsdtRequisites
    card_id: UUID
    user_id: int
    cheque_id: int | None


@dataclass
class SellOrder:
    id: UUID
    crypto_amount: Decimal
    fiat_amount: Decimal
    ticker: Ticker
    status: OrderStatus
    created_at: datetime
    completed_at: datetime | None
    note: str | None
    user_requisites: CardRequisites
    service_requisites: UsdtRequisites
    user_id: int
    cheque_id: int | None
