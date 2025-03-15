from datetime import datetime
from decimal import Decimal
from uuid import UUID

from backend.domain.entities.settings import Settings


def admin_panel_menu_text() -> str:
    return '🖥 <b>Админ панель:</b>'


def settings_menu_text(settings: Settings) -> str:
    return (
        f'🇺🇸 Реквизиты [USDT]: <code>{settings.usdt_requisites}</code>\n\n'
        f'📈 Курс продажи: <b>{settings.sell_usdt_rate}₴</b>\n'
        f'📈 Курс покупки: <b>{settings.buy_usdt_rate}₴</b>\n\n'
        f'‍💻 Канал модерации: <code>{settings.tg_chat_id}</code>\n'
    )


def card_menu_text() -> str:
    return '📲 <b>Выберите действия:</b>'


def get_new_card_text() -> str:
    return '✍️ <b>Введите реквизиты карты:</b>'


def delete_card_menu_text() -> str:
    return '📲 <b>Нажмите на карту для удаления</b>'


def change_usdt_requisites_menu_text() -> str:
    return '✍️ <b>Введите новый адрес кошелька usdt(trc20):</b>'


def change_sell_usdt_rate_menu_text() -> str:
    return '✍️ <b>Введите новый курс продажи USDT:</b>'


def change_buy_usdt_rate_menu_text() -> str:
    return '✍️ <b>Введите новый курс покупки USDT:</b>'


def change_tg_chat_id_menu_text() -> str:
    return (
        '🆔 <b>Отправьте чат айди канала модерации.</b>\n\n'
        '⚠️ <u>Обязательно добавьте бот в канал и выдайте ему права администратора!</u>'
    )


def wallet_menu_text(
    address: str,
    trx_balance: Decimal,
    usdt_balance: Decimal,
) -> str:
    return (
        f'👛 Кошелек: <code>{address}</code>\n\n'
        f'▫️ <b>TRX:</b> <i>{trx_balance}</i>\n'
        f'▫️ <b>USDT:</b> <i>{usdt_balance}</i>\n'
    )


def no_wallet_menu_text() -> str:
    return '⚠️ <b>Для корректной работы бота, сгенерируйте приватный ключ для кошелька.</b>'


def private_key_text(private_key_hex: str) -> str:
    return f'🔑 Приватный ключ от вашего кошелька: <tg-spoiler>{private_key_hex}</tg-spoiler>'


def get_address_for_withdraw() -> str:
    return '✍️ <b>Введите адрес для перевода:</b>'


def get_withdraw_amount_text(balance: Decimal, currency: str) -> str:
    return f'✍️ <b>Введите сумму вывода, доступно: {balance} {currency} </b>'


def withdraw_details_text(to_address: str, amount: str, currency: str) -> str:
    return (
        f'💸 Сумма вывода: <b>{amount} {currency}</b>\n'
        f'📥 Адрес получателя: <code>{to_address}</code>\n\n'
        '📲 <b>Выберите действия</b>'
    )


def withdraw_transaction_details_text(tx_id: str) -> str:
    return f'📑 https://nile.tronscan.org/#/transaction/{tx_id}'


def withdraw_reject_text():
    return '❌ <b>Вывод отменен</b>'


def sell_exchange_order_details_notification_text(
    user_id: int | str,
    username: str | None,
    full_name: str,
    crypto_amount: Decimal,
    fiat_amount: Decimal,
    service_requisites: str,
    user_requisites: str,
) -> str:
    return (
        '🔻 <b>Новая заявка на продажу USDT</b>\n\n'
        f'👤 <b>Пользователь:</b>\n'
        f'🆔 ID: <code>{user_id}</code>\n'
        f'📛 Имя: {full_name}\n'
        f'💬 Username: {f"@{username}" if username else "—"}\n\n'
        f'📤 <b>Сумма к переводу:</b> {crypto_amount} USDT\n'
        f'💰 <b>Сумма к получению:</b> {fiat_amount} ₴\n\n'
        f'🏦 <b>Реквизиты для зачисления:</b>\n<code>{user_requisites}</code>\n\n'
        f'📥 <b>Реквизиты для перевода:</b>\n<code>{service_requisites}</code>\n'
    )


def buy_exchange_order_details_notification_text(
    user_id: int | str,
    username: str | None,
    full_name: str,
    crypto_amount: Decimal,
    fiat_amount: Decimal,
    service_requisites: str,
    user_requisites: str,
) -> str:
    return (
        '🔹 <b>Новая заявка на покупку USDT</b>\n\n'
        f'👤 <b>Пользователь:</b>\n'
        f'🆔 ID: <code>{user_id}</code>\n'
        f'📛 Имя: {full_name}\n'
        f'💬 Username: {f"@{username}" if username else "—"}\n\n'
        f'💰 <b>Сумма к переводу:</b> {fiat_amount} ₴\n'
        f'📥 <b>Сумма к получению:</b> {crypto_amount} USDT\n\n'
        f'🏦 <b>Реквизиты для зачисления:</b>\n<code>{user_requisites}</code>\n\n'
        f'📤 <b>Реквизиты для перевода:</b>\n<code>{service_requisites}</code>\n'
    )


def statistic_menu_text(
    buy_order_count: int,
    sell_order_count: int,
    total_bought_amount: Decimal,
    total_sold_amount: Decimal,
) -> str:
    return (
        f'📈 <b>{buy_order_count}</b> покупок на сумму: <b>{total_bought_amount} USDT</b>\n'
        f'📉 <b>{sell_order_count}</b> продаж на сумму: <b>{total_sold_amount} USDT</b>\n\n'
    )


def mailing_menu_text():
    return '📲 <b>Выберите тип рассылки:</b>'


def get_mailing_content_text(content_type: str):
    mailing_text_mapping = {
        'text': '✍️ <b>Введите текст для рассылки.</b>',
        'photo': '📥 <b>Отправьте картинку для рассылки.</b>',
        'video': '📥 <b>Отправьте видео для рассылки.</b>',
        'animation': '📥 <b>Отправьте гиф для рассылки.</b>',
    }

    return mailing_text_mapping[content_type]


def get_mailing_button_text():
    return '🖇 <b>Введите данные для кнопки под текстом. Формат ввода (текст|ссылка) если хотите отправить без кнопки введите просто 0.</b>'


def get_mailing_caption_text(content_type: str):
    content_mapping = {'photo': 'фото', 'video': 'видео', 'animation': 'гиф'}

    return f'✍️ <b>Введите текст который будет находится под {content_mapping[content_type]}</b>'


def example_mailing_text(mailing_text: str):
    return f'🔍 <b>Проверьте данные для рассылки!</b>\n\n{mailing_text}\n\nℹ️ <i>Отправить/отменить рассылку ➕ | ➖</i>'


def search_user_menu_text() -> str:
    return '🕵️‍♂️ <b>Как будем искать пользователя?</b>'


def get_user_id_for_search_text() -> str:
    return '✍️ <b>Введите <i>id</i> пользователя для поиска:</b>'


def get_username_for_search_text() -> str:
    return '✍️ <b>Введите <i>username</i> пользователя для поиска:</b>'


def user_details_menu_text(
    user_id: int,
    username: str | None,
    created_at: datetime,
    buy_order_count: int,
    sell_order_count: int,
    total_bought_amount: Decimal,
    total_sold_amount: Decimal,
) -> str:
    return (
        f'🆔 - [<code>{user_id}</code>]\n'
        f'👤 <b>Юзер:</b> {username}\n\n'
        f'📈 <b>{buy_order_count}</b> покупок на сумму: <b>{total_bought_amount} USDT</b>\n'
        f'📉 <b>{sell_order_count}</b> продаж на сумму: <b>{total_sold_amount} USDT</b>\n\n'
        f'📆 Дата регистрации: <b>{created_at.strftime("%Y-%M-%d")}</b>'
    )


def contacts_admin_menu_text() -> str:
    return '📲 <b>Выберите действия</b>'


def get_new_contact_text():
    return '✍️ <b>Введите информацию о контакте в формате <code>[название|ссылка]</code></b>'


def remove_contact_menu_text() -> str:
    return '📲 <b>Для удаления контакта просто нажмите на него</b>'


def get_reject_note_text() -> str:
    return '✍️ <b>Введите причину отмены данной заявки:</b>'


def operator_norification_text(order_id: UUID) -> str:
    return f'📩 <b>У вас новая заявка на обмен ID {order_id}</b>'
