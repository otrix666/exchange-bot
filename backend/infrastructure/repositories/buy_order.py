from collections.abc import Sequence
from uuid import UUID

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from backend.application import interfaces
from backend.domain import exceptions
from backend.domain.entities.admin import FullBuyOrder
from backend.domain.entities.order import BuyOrder
from backend.infrastructure.mapper.buy_order import BuyOrderMapper, FullBuyOrderMapper


class BuyOrderRepository(
    interfaces.BuyOrderReader,
    interfaces.BuyOrderSaver,
    interfaces.BuyOrderUpdater,
):
    def __init__(
        self,
        pool: AsyncConnectionPool,
        mapper: BuyOrderMapper,
        admin_mapper: FullBuyOrderMapper,
    ) -> None:
        self._pool = pool
        self._mapper = mapper
        self._admin_mapper = admin_mapper

    async def get_by_id(self, order_id: UUID) -> BuyOrder:
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
                    'card_id, '
                    'user_id, '
                    'cheque_id '
                    'FROM buy_exchange_orders WHERE id = %s'
                )
                await cur.execute(query, (order_id,))
                result = await cur.fetchone()
                if not result:
                    raise exceptions.BuyOrderNotFoundError
                return self._mapper.result_to_entity(result=result)

    async def get_all_by_user_id(self, user_id: int) -> Sequence[FullBuyOrder]:
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
                    'o.card_id, '
                    'o.user_id as order_user_id, '
                    'o.cheque_id, '
                    'u.id as user_id, '
                    'u.username, '
                    'u.full_name, '
                    'u.is_banned, '
                    'u.created_at as user_created_at, '
                    'c.id as order_card_id, '
                    'c.number, '
                    'c.user_id as operator_id, '
                    'c.is_deleted '
                    'FROM buy_exchange_orders o '
                    'JOIN users u ON o.user_id = u.id '
                    'JOIN cards c ON o.card_id = c.id '
                    'WHERE o.user_id = %s'
                )
                await cur.execute(query, (user_id,))
                results = await cur.fetchall()

                return [self._admin_mapper.result_to_entity(result=result) for result in results]

    async def get_all(self) -> Sequence[BuyOrder]:
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
                    'card_id, '
                    'user_id, '
                    'cheque_id '
                    'FROM buy_exchange_orders'
                )
                await cur.execute(query)
                results = await cur.fetchall()
                return [self._mapper.result_to_entity(result=result) for result in results]

    async def get_full_info(self, order_id: UUID) -> FullBuyOrder:
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
                    'o.card_id, '
                    'o.user_id as order_user_id, '
                    'o.cheque_id, '
                    'u.id as user_id, '
                    'u.username, '
                    'u.full_name, '
                    'u.is_banned, '
                    'u.created_at as user_created_at, '
                    'c.id as order_card_id, '
                    'c.number, '
                    'c.user_id as operator_id, '
                    'c.is_deleted '
                    'FROM buy_exchange_orders o '
                    'JOIN users u ON o.user_id = u.id '
                    'JOIN cards c ON o.card_id = c.id '
                    'WHERE o.id = %s'
                )
                await cur.execute(query, (order_id,))
                result = await cur.fetchone()
                if not result:
                    raise exceptions.BuyOrderNotFoundError

                return self._admin_mapper.result_to_entity(result=result)

    async def save(self, order: BuyOrder) -> BuyOrder:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                stmt = (
                    'INSERT INTO buy_exchange_orders('
                    'id, '
                    'crypto_amount, '
                    'fiat_amount, '
                    'ticker, '
                    'status, '
                    'created_at, '
                    'completed_at, '
                    'note, '
                    'user_requisites, '
                    'card_id, '
                    'user_id, '
                    'cheque_id '
                    ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING '
                    'id, crypto_amount, fiat_amount, ticker, status, created_at, '
                    'completed_at, note, user_requisites, card_id, user_id, cheque_id'
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
                        order.user_requisites.address,
                        order.card_id,
                        order.user_id,
                        order.cheque_id,
                    ),
                )

                await conn.commit()
                result = await cur.fetchone()
                return self._mapper.result_to_entity(result=result)

    async def update(self, order: BuyOrder) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                stmt = 'UPDATE buy_exchange_orders SET status = %s, completed_at = %s, note = %s WHERE id = %s'
                await cur.execute(stmt, (order.status, order.completed_at, order.note, order.id))
                await conn.commit()
