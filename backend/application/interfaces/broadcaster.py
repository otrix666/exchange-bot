from abc import abstractmethod
from typing import Protocol

from backend.application.interfaces.keyboard import Keyboard
from backend.application.interfaces.tg_message import Message


class Broadcaster(Protocol):
    @abstractmethod
    async def send_message(
        self,
        user_id: int | str,
        text: str | None = None,
        video_id: str | None = None,
        photo_id: str | None = None,
        gif_id: str | None = None,
        document_id: str | None = None,
        caption: str | None = None,
        disable_notification: bool = False,
        keyboard: Keyboard | None = None,
    ) -> Message: ...

    @abstractmethod
    async def broadcast(
        self,
        users: list[str | int],
        text: str | None = None,
        video_id: str | None = None,
        photo_id: str | None = None,
        gif_id: str | None = None,
        document_id: str | None = None,
        caption: str | None = None,
        disable_notification: bool = False,
        keyboard: Keyboard | None = None,
    ) -> int: ...
