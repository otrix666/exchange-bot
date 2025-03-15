from datetime import datetime
from decimal import Decimal
from uuid import UUID

from backend.domain.entities.order import Ticker


def main_menu_text() -> str:
    return 'Главное меню'


def profile_menu_text(
    user_id: int,
    created_at: datetime,
    buy_order_count: int,
    sell_order_count: int,
    total_bought_amount: Decimal,
    total_sold_amount: Decimal,
) -> str:
    return (
        f'🪪 Профиль - [<code>{user_id}</code>]\n\n'
        f'📈 <b>{buy_order_count}</b> покупок на сумму: <b>{total_bought_amount} USDT</b>\n'
        f'📉 <b>{sell_order_count}</b> продаж на сумму: <b>{total_sold_amount} USDT</b>\n\n'
        f'📆 Дата регистрации: <b>{created_at.strftime("%Y-%M-%d")}</b>'
    )


def exchange_menu_text() -> str:
    return '🔄 <b>Выберите действие:</b>'


def contacts_menu_text() -> str:
    return '📲 <b>Наши контакты:</b>'


def get_buy_usdt_amount_text() -> str:
    return '✍️ <b>Введите количество USDT для покупки:</b>'


def get_sell_usdt_amount_text() -> str:
    return '✍️ <b>Введите количество USDT для продажи:</b>'


def get_card_requisites_text(order_amount: Decimal) -> str:
    return f'💱 <i>Сумма к получению: {order_amount}₴</i>\n\n✍️ <b>Введите реквизиты банковской карты:</b>'


def get_usdt_requisites_text(order_amount: Decimal) -> str:
    return f'💱 <i>Сумма к оплате: {order_amount}₴</i>\n\n✍️ <b>Введите адрес USDT(TRC20) кошелька:</b>'


def sell_exchange_order_details_text(
    crypto_amount: str,
    fiat_amount: str,
    service_requisites: str,
    user_requisites: str,
) -> str:
    return (
        '🔻 <b>Заявка на продажу USDT</b>\n\n'
        f'📤 <b>Сумма к переводу:</b> {crypto_amount} USDT\n'
        f'💰 <b>Сумма к получению:</b> {fiat_amount} ₴\n\n'
        f'🏦 <b>Реквизиты для зачисления:</b>\n<code>{user_requisites}</code>\n\n'
        f'📥 <b>Реквизиты для перевода:</b>\n<code>{service_requisites}</code>\n\n'
        '✅ <b>Как подтвердить заявку?</b>\n'
        'Переведите указанную сумму по указанным реквизитам и отправьте скриншот или фото чека в этот чат! 📸'
    )


def buy_exchange_order_details_text(
    crypto_amount: str,
    fiat_amount: str,
    service_requisites: str,
    user_requisites: str,
) -> str:
    return (
        '🔹 <b>Заявка на покупку USDT</b>\n\n'
        f'💰 <b>Сумма к переводу:</b> {fiat_amount} ₴\n'
        f'📥 <b>Сумма к получению:</b> {crypto_amount} USDT\n\n'
        f'🏦 <b>Реквизиты для зачисления:</b>\n<code>{user_requisites}</code>\n\n'
        f'📤 <b>Реквизиты для перевода:</b>\n<code>{service_requisites}</code>\n\n'
        '✅ <b>Как подтвердить заявку?</b>\n'
        'Переведите указанную сумму по реквизитам и отправьте скриншот или фото чека в этот чат! 📸'
    )


def success_order_creat_text(order_id: UUID, ticker: Ticker) -> str:
    return f'📑 <b>Заявка: #{order_id} {ticker.upper()} успешно создана, ожидайте подтверждения от модерации</b>'


def reject_buy_order_notification_text(order_id: UUID, note: str) -> str:
    return f'❌ <b>Ваш ордер #{order_id} на покупку usdt был отменен по причине: {note}</b>'


def reject_sell_order_notification_text(order_id: UUID, note: str) -> str:
    return f'❌ <b>Ваш ордер #{order_id} на продажу usdt был отменен по причине: {note}</b>'


def confirm_buy_order_notification_text(order_id: UUID, tx_id: str) -> str:
    return (
        f'✅ <b>Ваш ордер #{order_id} на покупку usdt был успешно выполнен</b>\n'
        f'https://nile.tronscan.org/#/transaction/{tx_id}'
    )


def confirm_sell_order_notification_text(order_id: UUID) -> str:
    return f'✅ <b>Ваш ордер #{order_id} на продажу usdt был успешно выполнен</b>\n'
