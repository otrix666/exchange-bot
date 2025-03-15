from backend.domain.exceptions.base import DomainError


class BuyOrderNotFoundError(DomainError):
    def __init__(self):
        super().__init__('Buy Order not found')


class SellOrderNotFoundError(DomainError):
    def __init__(self):
        super().__init__('Sell Order not found')
