from dataclasses import dataclass

from backend.domain import exceptions


@dataclass(frozen=True)
class CardRequisites:
    card_number: str

    def __post_init__(self):
        if not self.card_number.isdigit() or len(self.card_number) not in (13, 16, 19):
            raise exceptions.InvalidCardNumberError


@dataclass(frozen=True)
class UsdtRequisites:
    address: str

    def __post_init__(self):
        if not self.address.startswith('T') or len(self.address) != 34:
            raise exceptions.InvalidUsdtAddressError
