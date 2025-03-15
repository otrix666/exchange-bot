from typing import Protocol

from backend.application import interfaces
from backend.application.dto.trc_wallet import AccountBalance, Transaction
from backend.config import Config
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.wallet import Wallet


class SaveWalletManager(interfaces.WalletSaver, interfaces.WalletDeleter, Protocol): ...


class CreateWalletInteractor:
    def __init__(
        self,
        save_manager: SaveWalletManager,
        trc_client: interfaces.TrcClient,
        key_creator: interfaces.PrivateKeyCreator,
    ):
        self._save_manager = save_manager
        self._trc_client = trc_client
        self._key_creator = key_creator

    async def __call__(self) -> AccountBalance:
        private_key_hex = self._key_creator.create_key()

        wallet = Wallet(
            id=None,
            private_key_hex=private_key_hex.private_key,
            is_deleted=False,
        )

        await self._save_manager.delete_all()
        await self._save_manager.save(wallet=wallet)

        account_balance = await self._trc_client.get_account_balance(private_key_hex=wallet.private_key_hex)
        return account_balance


class GetAccountBalanceInteractor:
    def __init__(
        self,
        config: Config,
        access_manager: interfaces.AccessManager,
        reader: interfaces.WalletReader,
        trc_client: interfaces.TrcClient,
    ):
        self._config = config
        self._access_manager = access_manager
        self._reader = reader
        self._trc_client = trc_client

    async def __call__(self, user_id: int) -> AccountBalance:
        if not self._access_manager.is_admin(user_id=user_id, admin_ids=self._config.bot.admins):
            raise domain_exceptions.UserPermissionError

        wallet = await self._reader.get_current()
        account_balance = await self._trc_client.get_account_balance(private_key_hex=wallet.private_key_hex)
        return account_balance


class GetWalletInteractor:
    def __init__(
        self,
        reader: interfaces.WalletReader,
    ):
        self._reader = reader

    async def __call__(self) -> Wallet:
        wallet = await self._reader.get_current()
        return wallet


class CreateTrxWithdrawInteractor:
    def __init__(
        self,
        reader: interfaces.WalletReader,
        trc_client: interfaces.TrcClient,
    ):
        self._reader = reader
        self._trc_client = trc_client

    async def __call__(self, to_address: str, amount: str) -> Transaction:
        try:
            amount = int(amount)
        except ValueError:
            raise exceptions.IncorrectWithdrawAmountError

        wallet = await self._reader.get_current()

        tx = await self._trc_client.transfer_trx(
            private_key_hex=wallet.private_key_hex,
            to_address=to_address,
            amount=amount,
        )
        return tx


class CreateUsdtWithdrawInteractor:
    def __init__(
        self,
        reader: interfaces.WalletReader,
        trc_client: interfaces.TrcClient,
    ):
        self._reader = reader
        self._trc_client = trc_client

    async def __call__(self, to_address: str, amount: str) -> Transaction:
        try:
            amount = int(amount)
        except ValueError:
            raise exceptions.IncorrectWithdrawAmountError

        wallet = await self._reader.get_current()

        tx = await self._trc_client.transfer_usdt(
            private_key_hex=wallet.private_key_hex,
            to_address=to_address,
            amount=amount,
        )
        return tx
