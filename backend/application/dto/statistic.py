from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class ExchangeStat:
    total_sold_amount: Decimal
    total_bought_amount: Decimal
    sell_order_count: int
    buy_order_count: int


@dataclass(slots=True)
class MailingStat:
    success: int
    un_success: int
