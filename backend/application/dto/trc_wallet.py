from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class AccountBalance:
    address: str
    usdt: Decimal
    trx: Decimal


@dataclass(slots=True)
class Transaction:
    tx_id: str
