def incorrect_exchange_amount_error_text(amount: str) -> str:
    return f'☹️ <b>Некорректное {amount} значения для просчета суммы обмена!</b>'


def incorrect_card_requisites_error_text(card_number: str) -> str:
    return f'☹️ <b>Некорректная банковская карта: {card_number}!</b>'


def incorrect_usdt_address_error_text(address: str) -> str:
    return f'☹️ <b>Некорректный адрес USDT(TRC20) кошелька: {address}!</b>'


def incorrect_order_status_for_reject_error_text() -> str:
    return 'ℹ️ Заявка находится в статусе, не допускающем отмену'


def incorrect_order_status_for_confirm_error_text() -> str:
    return 'ℹ️ Заявка находится в статусе, не допускающем подтверждения'


def no_contacts_for_remove_error_text() -> str:
    return '⚠️ Нет контактов для удаления'


def incorrect_withdraw_value_error_text() -> str:
    return '⚠️ Не корректное значения для вывода!'


def not_enough_trx_for_withdraw_error_text() -> str:
    return '⚠️ На балансе не достаточно trx для вывода!'


def not_enough_usdt_for_withdraw_error_text() -> str:
    return '⚠️ На балансе не достаточно usdt для вывода!'


def not_enough_trx_for_commission_error_text() -> str:
    return '⚠️ На балансе не достаточно trx для комиссии!'


def transaction_error_text() -> str:
    return '⚠️ Произошла ошибка во время создания транзакции, попробуйте позже!'


def only_operator_error_text() -> str:
    return '⚠️ Данное меню только для операторов'


def only_admin_error_text() -> str:
    return '⚠️ Данное меню только для админа'


def no_cards_error_text():
    return '⚠️ Вы не добавили ни одной карты'


def no_cards_for_order_error_text():
    return '⚠️ <b>Сервис обмена временно не работает, попробуйте позже</b>'


def no_permission_error_text() -> str:
    return '⚠️ Данный ордер был создан не на вашу карту'
