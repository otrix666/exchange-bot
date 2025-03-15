from abc import abstractmethod
from typing import Protocol

from backend.domain.entities.wallet import Wallet


class WalletReader(Protocol):
    @abstractmethod
    async def get_by_id(self, wallet_id: int) -> Wallet: ...

    @abstractmethod
    async def get_current(self) -> Wallet: ...


class WalletSaver(Protocol):
    @abstractmethod
    async def save(self, wallet: Wallet) -> None: ...


class WalletDeleter(Protocol):
    @abstractmethod
    async def delete_all(self) -> None: ...
