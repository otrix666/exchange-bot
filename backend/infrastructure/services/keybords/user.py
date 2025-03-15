from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from backend.application import interfaces
from backend.domain.entities.contact import Contact


class UserKeyboardBuilder(interfaces.UserKeyboardBuilder):
    def __init__(self):
        self._kb_builder: InlineKeyboardBuilder | None = None

    def get_main_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder = InlineKeyboardBuilder()
        self._kb_builder.row(
            InlineKeyboardButton(text='🪪 Мой профиль', callback_data='profile_menu'),
        )
        self._kb_builder.row(
            InlineKeyboardButton(text='💱 Обмен', callback_data='exchange_menu'),
            InlineKeyboardButton(text='👥 Контакты', callback_data='contacts_menu'),
        )

        return self._kb_builder

    def get_main_menu_return_kb(self):
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🔙 Назад', callback_data='main_menu')

        return self._kb_builder

    def get_profile_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='📑 История сделок', callback_data='order_history')
        self._kb_builder.button(text='🔙 Назад', callback_data='main_menu')
        self._kb_builder.adjust(1)

        return self._kb_builder

    def get_exchange_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='📈 Купить USDT', callback_data='buy')
        self._kb_builder.button(text='📉 Продать USDT', callback_data='sell')
        self._kb_builder.button(text='🔙 Назад', callback_data='main_menu')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_exchange_menu_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🔙 Назад', callback_data='exchange_menu')
        return self._kb_builder

    def get_contact_menu_kb(self, contacts: Sequence[Contact]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for contact in contacts:
            self._kb_builder.button(text=f'{contact.title}', url=f'{contact.url}')

        self._kb_builder.button(text='🔙 Назад', callback_data='main_menu')
        self._kb_builder.adjust(1)

        return self._kb_builder
