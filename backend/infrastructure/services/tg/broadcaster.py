import asyncio
import logging

from aiogram import Bot, exceptions

from backend.application import interfaces


class Broadcaster(interfaces.Broadcaster):
    def __init__(self, bot: Bot):
        self._bot = bot

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
        keyboard: interfaces.Keyboard | None = None,
    ) -> interfaces.Message | None:
        reply_markup = keyboard.as_markup() if keyboard else None
        try:
            if text:
                message = await self._bot.send_message(
                    chat_id=user_id,
                    text=text,
                    disable_notification=disable_notification,
                    reply_markup=reply_markup,
                )
            elif video_id:
                message = await self._bot.send_video(
                    chat_id=user_id,
                    video=video_id,
                    caption=caption,
                    reply_markup=reply_markup,
                )
            elif photo_id:
                message = await self._bot.send_photo(
                    chat_id=user_id,
                    photo=photo_id,
                    caption=caption,
                    reply_markup=reply_markup,
                )
            elif gif_id:
                message = await self._bot.send_animation(
                    chat_id=user_id,
                    animation=gif_id,
                    caption=caption,
                    reply_markup=reply_markup,
                )
            elif document_id:
                message = await self._bot.send_document(
                    chat_id=user_id,
                    document=document_id,
                    caption=caption,
                    reply_markup=reply_markup,
                )
            else:
                message = None
        except exceptions.TelegramBadRequest:
            logging.exception('Telegram server says - Bad Request: chat not found')
            message = None
        except exceptions.TelegramForbiddenError:
            logging.exception(f'Target [ID:{user_id}]: got TelegramForbiddenError')
            message = None
        except exceptions.TelegramRetryAfter as e:
            logging.exception(
                f'Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.',
            )
            await asyncio.sleep(e.retry_after)
            message = await self.send_message(
                user_id=user_id,
                text=text,
                video_id=video_id,
                photo_id=photo_id,
                gif_id=gif_id,
                document_id=document_id,
                caption=caption,
                disable_notification=disable_notification,
                keyboard=keyboard,
            )
        except exceptions.TelegramAPIError:
            logging.exception(f'Target [ID:{user_id}]: failed')
            message = None
        else:
            logging.info(f'Target [ID:{user_id}]: success')
        return message

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
        keyboard: interfaces.Keyboard | None = None,
    ) -> int:
        count = 0
        reply_markup = None
        try:
            for user_id in users:
                if reply_markup:
                    reply_markup = reply_markup.as_markup()

                if text:
                    sent = await self.send_message(
                        user_id=user_id,
                        text=text,
                        disable_notification=disable_notification,
                        keyboard=keyboard,
                    )

                elif video_id:
                    sent = await self.send_message(
                        user_id=user_id,
                        video_id=video_id,
                        caption=caption,
                        keyboard=keyboard,
                    )

                elif photo_id:
                    sent = await self.send_message(
                        user_id=user_id,
                        photo_id=photo_id,
                        caption=caption,
                        keyboard=keyboard,
                    )
                elif gif_id:
                    sent = await self.send_message(user_id=user_id, gif_id=gif_id, caption=caption, keyboard=keyboard)

                elif document_id:
                    sent = await self.send_message(
                        user_id=user_id,
                        document_id=gif_id,
                        caption=caption,
                        keyboard=keyboard,
                    )
                else:
                    sent = None

                if sent:
                    count += 1

                await asyncio.sleep(0.5)
        finally:
            logging.info(f'{count} messages successful sent.')

        return count
