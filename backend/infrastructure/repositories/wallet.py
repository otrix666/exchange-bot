from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from backend.application import interfaces
from backend.domain import exceptions
from backend.domain.entities.wallet import Wallet


class WalletRepository(
    interfaces.WalletReader,
    interfaces.WalletSaver,
    interfaces.WalletDeleter,
):
    def __init__(self, pool: AsyncConnectionPool):
        self._pool = pool

    async def get_by_id(self, wallet_id: int) -> Wallet:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Wallet)) as cur:
                query = 'SELECT id, private_key_hex, is_deleted FROM wallets WHERE id = %s'
                await cur.execute(query, (wallet_id,))
                result = await cur.fetchone()
                if not result:
                    raise exceptions.WalletNotFoundError
                return result

    async def get_current(self) -> Wallet:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Wallet)) as cur:
                query = 'SELECT id, private_key_hex, is_deleted FROM wallets WHERE is_deleted = FALSE'
                await cur.execute(query)
                result = await cur.fetchone()
                if not result:
                    raise exceptions.WalletNotFoundError
                return result

    async def save(self, wallet: Wallet) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                stmt = 'INSERT INTO wallets (private_key_hex, is_deleted) VALUES (%s, %s)'
                await cur.execute(stmt, (wallet.private_key_hex, wallet.is_deleted))
                await conn.commit()

    async def delete_all(self) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                stmt = 'UPDATE wallets SET is_deleted = TRUE'
                await cur.execute(stmt)
                await conn.commit()
