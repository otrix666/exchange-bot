from collections.abc import Sequence

from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from backend.application import interfaces
from backend.domain import exceptions
from backend.domain.entities.contact import Contact


class ContactRepository(
    interfaces.ContactReader,
    interfaces.ContactSaver,
    interfaces.ContactDeleter,
):
    def __init__(self, pool: AsyncConnectionPool):
        self._pool = pool

    async def get_by_id(self, contact_id: int) -> Contact:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Contact)) as cur:
                query = 'SELECT id, title, url FROM contacts WHERE id = %s'
                await cur.execute(query, (contact_id,))
                result = await cur.fetchone()
                if not result:
                    raise exceptions.ContactNotFoundError
                return result

    async def get_all(self) -> Sequence[Contact]:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Contact)) as cur:
                query = 'SELECT id, title, url FROM contacts'
                await cur.execute(query)
                results = await cur.fetchall()
                return results

    async def save(self, contact: Contact) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                stmt = 'INSERT INTO contacts (title, url) VALUES ( %s, %s)'
                await cur.execute(stmt, (contact.title, contact.url))
                await conn.commit()

    async def delete_by_id(self, contact: Contact) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                stmt = 'DELETE FROM contacts WHERE id = %s'
                await cur.execute(stmt, (contact.id,))
                await conn.commit()
