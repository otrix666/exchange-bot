import binascii
import secrets
from decimal import Decimal

from tronpy import AsyncContract, AsyncTron
from tronpy.exceptions import AddressNotFound
from tronpy.keys import PrivateKey

from backend.application import exceptions, interfaces
from backend.application.dto.trc_wallet import AccountBalance, Transaction
from backend.domain.entities.wallet import PrivateKeyHex

FEE = 5_000_000
TOKEN_UNIT = 1_000_000


class PrivateKeyCreator(interfaces.PrivateKeyCreator):
    @staticmethod
    def create_key() -> PrivateKeyHex:
        private_key_bytes = secrets.token_bytes(32)
        private_key_hex = binascii.hexlify(private_key_bytes).decode('utf-8')
        return PrivateKeyHex(
            private_key=private_key_hex,
        )


class TrcClient(interfaces.TrcClient):
    def __init__(
        self,
        client: AsyncTron,
        contract_address: str,
    ):
        self._client = client
        self._contract_address = contract_address
        self._contract: AsyncContract | None = None
        self._private_key: PrivateKey | None = None

    async def get_account_balance(self, private_key_hex: str) -> AccountBalance:
        self._sync_private_key(private_key_hex=private_key_hex)
        await self._sync_contract()

        address = self._private_key.public_key.to_base58check_address()

        if not await self._check_account_exists(address=address):
            return AccountBalance(
                address=address,
                trx=Decimal(0),
                usdt=Decimal(0),
            )

        trx_balance = await self._client.get_account_balance(address)
        usdt_balance = await self._contract.functions.balanceOf(address)
        usdt_balance = usdt_balance // TOKEN_UNIT

        return AccountBalance(
            address=address,
            trx=trx_balance,
            usdt=usdt_balance,
        )

    async def transfer_trx(self, private_key_hex: str, to_address: str, amount: int) -> Transaction:
        account_balance = await self.get_account_balance(private_key_hex=private_key_hex)

        if account_balance.trx + FEE // TOKEN_UNIT < amount:
            raise exceptions.NotEnoughTrxForTransferError

        from_address = self._private_key.public_key.to_base58check_address()

        tx_builder = self._client.trx.transfer(from_=from_address, to=to_address, amount=amount * TOKEN_UNIT)
        tx_builder.fee_limit(FEE)
        tx = await tx_builder.build()
        tx.sign(self._private_key)
        tx = await tx.broadcast()

        if not tx.result:
            raise exceptions.TransactionError

        return Transaction(tx_id=tx.txid)

    async def transfer_usdt(self, private_key_hex: str, to_address: str, amount: int) -> Transaction:
        account_balance = await self.get_account_balance(private_key_hex)

        if account_balance.trx < FEE // TOKEN_UNIT:
            raise exceptions.NotEnoughTrxForCommissionError

        if account_balance.usdt < amount:
            raise exceptions.NotEnoughUsdtForTransferError

        from_address = self._private_key.public_key.to_base58check_address()

        tx_builder = await self._contract.functions.transfer(to_address, amount * TOKEN_UNIT)
        tx_builder.with_owner(from_address)
        tx_builder.fee_limit(FEE)
        tx = await tx_builder.build()
        tx = tx.sign(self._private_key)
        tx = await self._client.broadcast(tx)

        if not tx['result']:
            raise exceptions.TransactionError

        return Transaction(tx_id=tx['txid'])

    def _sync_private_key(self, private_key_hex) -> None:
        if not self._private_key:
            self._private_key = PrivateKey(private_key_bytes=binascii.unhexlify(private_key_hex))

    async def _sync_contract(self) -> None:
        if not self._contract:
            self._contract = await self._client.get_contract(self._contract_address)

    async def _check_account_exists(self, address) -> bool:
        try:
            account = await self._client.get_account(address)
            return bool(account)
        except AddressNotFound:
            return False
