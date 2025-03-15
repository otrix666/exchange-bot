from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class Settings:
    usdt_requisites: str
    sell_usdt_rate: Decimal
    buy_usdt_rate: Decimal
    tg_chat_id: str
