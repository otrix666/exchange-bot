from abc import abstractmethod
from typing import Protocol

from backend.application.dto.trc_wallet import AccountBalance, Transaction
from backend.domain.entities.wallet import PrivateKeyHex


class PrivateKeyCreator(Protocol):
    @staticmethod
    @abstractmethod
    def create_key() -> PrivateKeyHex: ...


class TrcClient(Protocol):
    @abstractmethod
    async def _sync_contract(self) -> None: ...

    @abstractmethod
    def _sync_private_key(self, private_key_hex) -> None: ...

    @abstractmethod
    async def _check_account_exists(self, address: str) -> bool: ...

    @abstractmethod
    async def get_account_balance(self, private_key_hex: str) -> AccountBalance: ...

    @abstractmethod
    async def transfer_trx(self, private_key_hex: str, to_address: str, amount: int) -> Transaction: ...

    @abstractmethod
    async def transfer_usdt(self, private_key_hex: str, to_address: str, amount: int) -> Transaction: ...
