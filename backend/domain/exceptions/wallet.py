from backend.domain.exceptions.base import DomainError


class WalletNotFoundError(DomainError):
    def __init__(self):
        super().__init__('Wallet not found')
