from backend.domain.exceptions.base import DomainError


class InvalidCardNumberError(DomainError):
    def __init__(self):
        super().__init__('Invalid card number')


class InvalidUsdtAddressError(DomainError):
    def __init__(self):
        super().__init__('Invalid USDT TRC20 address')
