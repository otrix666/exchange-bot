from collections.abc import Sequence
from uuid import UUID

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from backend.application import interfaces
from backend.application.interfaces import Keyboard
from backend.domain.entities.card import Card
from backend.domain.entities.contact import Contact


class AdminKeyboardBuilder(interfaces.AdminKeyboardBuilder):
    def __init__(self):
        self._kb_builder: InlineKeyboardBuilder | None = None

    def get_admin_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='⚙️ Настройки', callback_data='settings_menu')
        self._kb_builder.button(text='👛 Кошельки', callback_data='wallets_menu')
        self._kb_builder.button(text='👥 Юзеры', callback_data='users_menu')
        self._kb_builder.button(text='📊 Статистика', callback_data='statistics_menu')
        self._kb_builder.button(text='📲 Контакты', callback_data='admin_contacts_menu')
        self._kb_builder.button(text='❌ Закрыть', callback_data='close')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_settings_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.row(
            InlineKeyboardButton(text='💳 Карты', callback_data='cards_menu'),
            InlineKeyboardButton(text='🇺🇸 Реквизиты [USDT]', callback_data='set_usdt_requisites'),
        )

        self._kb_builder.row(
            InlineKeyboardButton(text='📉 Курс продажи', callback_data='set_sell_usdt_rate'),
            InlineKeyboardButton(text='📈 Курс покупки', callback_data='set_buy_usdt_rate'),
        )

        self._kb_builder.row(
            InlineKeyboardButton(text='🧑‍💻 Канал модерации', callback_data='set_tg_chat_id'),
        )

        self._kb_builder.row(
            InlineKeyboardButton(text='🔙 Назад', callback_data='admin_panel'),
        )

        return self._kb_builder

    def get_card_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='➕ Добавить', callback_data='add_card')
        self._kb_builder.button(text='➖ Удалить', callback_data='delete_card_menu')
        self._kb_builder.button(text='🔙 Назад', callback_data='admin_panel')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_delete_card_menu(self, cards: Sequence[Card]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for card in cards:
            self._kb_builder.button(text=f'{card.number.card_number}', callback_data=f'del_card:{card.id}')

        self._kb_builder.button(text='🔙 Назад', callback_data='cards_menu')
        self._kb_builder.adjust(1)

        return self._kb_builder

    def get_card_menu_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder

        self._kb_builder = InlineKeyboardBuilder()
        self._kb_builder.button(text='🔙 Назад', callback_data='cards_menu')

        return self._kb_builder

    def get_settings_menu_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🔙 Назад', callback_data='settings_menu')

        return self._kb_builder

    def get_wallet_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='⚙️ Create key', callback_data='create_wallet')
        self._kb_builder.button(text='🔑 Export key', callback_data='export_private_key')
        self._kb_builder.button(text='💸 Вывод [USDT]', callback_data='withdraw_usdt')
        self._kb_builder.button(text='💸 Вывод [TRX]', callback_data='withdraw_trx')
        self._kb_builder.button(text='🔙 Назад', callback_data='admin_panel')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_wallet_manu_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()
        self._kb_builder.button(text='🔙 Назад', callback_data='wallets_menu')
        return self._kb_builder

    def get_withdraw_confirmation_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()
        self._kb_builder.button(text='✅ Подтвердить', callback_data='confirm')
        self._kb_builder.button(text='❌ Отменить', callback_data='reject')
        return self._kb_builder

    def get_admin_menu_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🔙 Назад', callback_data='admin_panel')

        return self._kb_builder

    def get_users_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🔔 Рассылка', callback_data='mailing_menu')
        self._kb_builder.button(text='🕵️‍♂️ Найти юзера', callback_data='search_user_menu')
        self._kb_builder.button(text='🔙 Назад', callback_data='admin_panel')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_mailing_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='💬 Текстом', callback_data='mailing:text')
        self._kb_builder.button(text='🌌 Картинкой', callback_data='mailing:photo')
        self._kb_builder.button(text='📹 Видео', callback_data='mailing:video')
        self._kb_builder.button(text='🎑 Гиф', callback_data='mailing:animation')
        self._kb_builder.button(text='🔙 Назад', callback_data='users_menu')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_users_menu_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🔙 Назад', callback_data='users_menu')

        return self._kb_builder

    def get_search_user_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='▫️ [ID]', callback_data='search_by_id')
        self._kb_builder.button(text='▫️ [Username]', callback_data='search_by_username')
        self._kb_builder.button(text='🔙 Назад', callback_data='users_menu')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_user_details_menu_kb(self, user_id: int, is_banned: bool) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        if is_banned:
            self._kb_builder.button(text='🌕 Разбанить', callback_data=f'unban_user:{user_id}')
        else:
            self._kb_builder.button(text='🌑 Забанить', callback_data=f'ban_user:{user_id}')

        self._kb_builder.button(text='🔙 Назад', callback_data='users_menu')
        self._kb_builder.adjust(1)

        return self._kb_builder

    def get_admin_contacts_menu_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='➕ Добавить', callback_data='add_contact')
        self._kb_builder.button(text='➖ Удалить', callback_data='remove_contact_menu')
        self._kb_builder.button(text='🔙 Назад', callback_data='admin_panel')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_remove_contact_kb(self, contacts: Sequence[Contact]) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        for contact in contacts:
            self._kb_builder.button(text=f'🗑 [{contact.title}]', callback_data=f'remove_contact:{contact.id}')

        self._kb_builder.button(text='🔙 Назад', callback_data='admin_contacts_menu')
        self._kb_builder.adjust(1)

        return self._kb_builder

    def get_admin_contacts_menu_return_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🔙 Назад', callback_data='admin_contacts_menu')

        return self._kb_builder

    def get_order_confirm_kb(
        self,
        order_id: UUID,
        order_type: str,
        is_banned: bool,
    ):
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='✅ Подтвердить', callback_data=f'confirm_{order_type}_order:{order_id}')
        self._kb_builder.button(text='❌ Отменить', callback_data=f'reject_{order_type}_order:{order_id}')
        if is_banned:
            self._kb_builder.button(text='🌕 Разбанить', callback_data=f'unban_by_{order_type}_order:{order_id}')
        else:
            self._kb_builder.button(text='🌑 Забанить', callback_data=f'ban_by_{order_type}_order:{order_id}')
        self._kb_builder.adjust(2)

        return self._kb_builder

    def get_return_buy_order_kb(self, order_id: int) -> Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🔙 Назад', callback_data=f'buy_order:{order_id}')

        return self._kb_builder

    def get_return_sell_order_kb(self, order_id: int) -> Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='🔙 Назад', callback_data=f'sell_order:{order_id}')

        return self._kb_builder

    def get_close_kb(self) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(
            text='❌ Закрыть',
            callback_data='close',
        )
        return self._kb_builder

    def get_custom_kb(self, text: str, url: str) -> interfaces.Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()
        self._kb_builder.button(
            text=f'{text}',
            url=f'{url}',
        )

        self._kb_builder.button(
            text='Закрыть',
            callback_data='hide_message',
        )

        self._kb_builder.adjust(1)

        return self._kb_builder

    def get_operator_notifications_kb(self, chat_id: str, message_id: str) -> interfaces.Keyboard:
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='💸 Перейти', url=f'https://t.me/c/{chat_id}/{message_id}')

        return self._kb_builder
