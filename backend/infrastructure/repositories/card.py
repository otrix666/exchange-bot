from collections.abc import Sequence
from uuid import UUID

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from backend.application import exceptions, interfaces
from backend.domain.entities.card import Card
from backend.infrastructure.mapper.card import CardMapper


class CardRepository(
    interfaces.CardReader,
    interfaces.CardSaver,
    interfaces.CardDeleter,
):
    def __init__(
        self,
        pool: AsyncConnectionPool,
        mapper: CardMapper,
    ):
        self._pool = pool
        self._mapper = mapper

    async def get_by_id(self, card_id: UUID) -> Card:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                query = 'SELECT id, number, user_id, is_deleted FROM cards WHERE id = %s'
                await cur.execute(query, (card_id,))
                result = await cur.fetchone()
                if not result:
                    raise exceptions.CardNotFoundByIdError

                return self._mapper.result_to_entity(result)

    async def get_all_by_user_id(self, user_id: int) -> Sequence[Card]:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                query = 'SELECT id, number, user_id, is_deleted FROM cards WHERE user_id = %s AND is_deleted = FALSE'
                await cur.execute(query, (user_id,))
                results = await cur.fetchall()
                return [self._mapper.result_to_entity(result) for result in results]

    async def save(self, card: Card) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                stmt = 'INSERT INTO cards(id, number, user_id, is_deleted) VALUES(%s, %s, %s, %s)'
                await cur.execute(stmt, (card.id, card.number.card_number, card.user_id, card.is_deleted))
                await conn.commit()

    async def delete_by_id(self, card: Card) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                stmt = 'UPDATE cards SET is_deleted = %s WHERE id = %s'
                await cur.execute(stmt, (card.is_deleted, card.id))
                await conn.commit()
