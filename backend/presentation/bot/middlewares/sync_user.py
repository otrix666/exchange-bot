from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from dishka import AsyncContainer

from backend.application.use_cases.user import SyncTelegramUserInteractor
from backend.config import Config


class SyncUserMiddleware(BaseMiddleware):
    def __init__(
        self,
        container: AsyncContainer,
    ) -> None:
        self._container = container

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        async with self._container() as container:
            interactor = await container.get(SyncTelegramUserInteractor)
            config = await container.get(Config)

        user = await interactor(
            user_id=event.from_user.id,
            username=event.from_user.username,
            full_name=event.from_user.full_name,
        )

        if user.id in config.bot.admins or user.id in config.bot.operators:
            data['user'] = user
            return await handler(event, data)
