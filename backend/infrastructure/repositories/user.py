from collections.abc import Sequence

from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from backend.application import interfaces
from backend.domain import exceptions
from backend.domain.entities.user import User


class UserRepository(
    interfaces.UserReader,
    interfaces.UserSaver,
    interfaces.UserUpdater,
):
    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def get_by_id(self, user_id: int) -> User:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                query = 'SELECT id, username, full_name, is_banned, created_at FROM users WHERE id = %s'
                await cur.execute(query, (user_id,))
                result = await cur.fetchone()
                if not result:
                    raise exceptions.UserNotFoundByIdError(user_id=user_id)
                return result

    async def get_by_username(self, username: str) -> User:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                query = 'SELECT id, username, full_name, is_banned, created_at FROM users WHERE username = %s'
                await cur.execute(query, (username,))
                result = await cur.fetchone()
                if not result:
                    raise exceptions.UserNotFoundByUsernameError(username=username)
                return result

    async def get_all(self) -> Sequence[User]:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                query = 'SELECT id, username, full_name, is_banned, created_at FROM users'
                await cur.execute(query)
                result = await cur.fetchall()
                return result

    async def save_or_update(self, user: User) -> User:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                stmt = (
                    'INSERT INTO users(id, username, full_name, is_banned, created_at) VALUES(%s, %s, %s, %s, %s) '
                    'ON CONFLICT(id) DO UPDATE SET '
                    'username=EXCLUDED.username, '
                    'full_name=EXCLUDED.full_name '
                    'RETURNING id, username, full_name, is_banned, created_at '
                )
                await cur.execute(
                    stmt,
                    (user.id, user.username, user.full_name, user.is_banned, user.created_at),
                )
                await conn.commit()
                result = await cur.fetchone()
                return result

    async def update(self, user: User) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                stmt = 'UPDATE users set username = %s, full_name = %s, is_banned = %s WHERE id = %s'
                await cur.execute(stmt, (user.username, user.full_name, user.is_banned, user.id))
                await conn.commit()
