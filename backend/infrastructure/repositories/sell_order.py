from collections.abc import Sequence
from uuid import UUID

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from backend.application import interfaces
from backend.domain import exceptions
from backend.domain.entities.admin import FullSellOrder
from backend.domain.entities.order import SellOrder
from backend.infrastructure.mapper.sell_order import FullSellOrderMapper, SellOrderMapper


class SellOrderRepository(
    interfaces.SellOrderReader,
    interfaces.SellOrderSaver,
    interfaces.SellOrderUpdater,
):
    def __init__(
        self,
        pool: AsyncConnectionPool,
        mapper: SellOrderMapper,
        admin_mapper: FullSellOrderMapper,
    ) -> None:
        self._pool = pool
        self._mapper = mapper
        self._admin_mapper = admin_mapper

    async def get_by_id(self, order_id: UUID) -> SellOrder:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                query = (
                    'SELECT '
                    'id, '
                    'crypto_amount, '
                    'fiat_amount, '
                    'ticker, '
                    'status, '
                    'created_at, '
                    'completed_at, '
                    'note, '
                    'user_requisites, '
                    'service_requisites, '
                    'user_id, '
                    'cheque_id '
                    'FROM sell_exchange_orders WHERE id = %s'
                )
                await cur.execute(query, (order_id,))
                result = await cur.fetchone()
                if not result:
                    raise exceptions.SellOrderNotFoundError
                return self._mapper.result_to_entity(result=result)

    async def get_all_by_user_id(self, user_id: int) -> Sequence[SellOrder]:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                query = (
                    'SELECT '
                    'id, '
                    'crypto_amount, '
                    'fiat_amount, '
                    'ticker, '
                    'status, '
                    'created_at, '
                    'completed_at, '
                    'note, '
                    'user_requisites, '
                    'service_requisites, '
                    'user_id, '
                    'cheque_id '
                    'FROM sell_exchange_orders WHERE user_id = %s'
                )
                await cur.execute(query, (user_id,))
                result = await cur.fetchall()

                return [self._mapper.result_to_entity(result=result) for result in result]

    async def get_all(self) -> Sequence[SellOrder]:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                query = (
                    'SELECT '
                    'id, '
                    'crypto_amount, '
                    'fiat_amount, '
                    'ticker, '
                    'status, '
                    'created_at, '
                    'completed_at, '
                    'note, '
                    'user_requisites, '
                    'service_requisites, '
                    'user_id, '
                    'cheque_id '
                    'FROM sell_exchange_orders'
                )
                await cur.execute(query)
                result = await cur.fetchall()

                return [self._mapper.result_to_entity(result=result) for result in result]

    async def get_full_info(self, order_id: UUID) -> FullSellOrder:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                query = (
                    'SELECT '
                    'o.id as order_id, '
                    'o.crypto_amount, '
                    'o.fiat_amount, '
                    'o.ticker, '
                    'o.status, '
                    'o.created_at as order_created_at, '
                    'o.completed_at, '
                    'o.note, '
                    'o.user_requisites, '
                    'o.service_requisites, '
                    'o.user_id as order_user_id, '
                    'o.cheque_id, '
                    'u.id as user_id, '
                    'u.username, '
                    'u.full_name, '
                    'u.role, '
                    'u.is_banned, '
                    'u.created_at as user_created_at '
                    'FROM sell_exchange_orders o '
                    'JOIN users u ON o.user_id = u.id '
                    'WHERE o.id = %s'
                )
                await cur.execute(query, (order_id,))
                result = await cur.fetchone()
                if not result:
                    raise

                return self._admin_mapper.result_to_entity(result=result)

    async def save(self, order: SellOrder) -> SellOrder:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                stmt = (
                    'INSERT INTO sell_exchange_orders('
                    'id, '
                    'crypto_amount, '
                    'fiat_amount, '
                    'ticker, '
                    'status, '
                    'created_at, '
                    'completed_at, '
                    'note, '
                    'user_requisites, '
                    'service_requisites, '
                    'user_id, '
                    'cheque_id '
                    ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING '
                    'id, crypto_amount, fiat_amount, ticker, status, created_at, completed_at, note, '
                    'user_requisites, service_requisites, user_id, cheque_id'
                )
                await cur.execute(
                    stmt,
                    (
                        order.id,
                        order.crypto_amount,
                        order.fiat_amount,
                        order.ticker,
                        order.status,
                        order.created_at,
                        order.completed_at,
                        order.note,
                        order.user_requisites.card_number,
                        order.service_requisites.address,
                        order.user_id,
                        order.cheque_id,
                    ),
                )

                await conn.commit()
                result = await cur.fetchone()
                return self._mapper.result_to_entity(result=result)

    async def update(self, order: SellOrder) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                stmt = 'UPDATE sell_exchange_orders SET status = %s, completed_at = %s, note = %s WHERE id = %s'
                await cur.execute(stmt, (order.status, order.completed_at, order.note, order.id))
                await conn.commit()
