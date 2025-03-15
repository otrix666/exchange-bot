from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka

from backend.application import exceptions, interfaces
from backend.application.use_cases.admin import (
    BanUserByBuyOrderInteractor,
    BanUserBySellOrderInteractor,
    ConfirmBuyOrderInteractor,
    ConfirmSellOrderInteractor,
    GetExchangeStatInteractor,
    GetFullBuyOrderInteractor,
    GetFullSellOrderInteractor,
    UserBanInteractor,
)
from backend.application.use_cases.buy_order import GetBuyOrderInteractor
from backend.application.use_cases.card import DeleteCardInteractor, GetCardsInteractor
from backend.application.use_cases.contact import DeleteContactInteractor, GetContactsInteractor
from backend.application.use_cases.sell_order import GetSellOrderInteractor
from backend.application.use_cases.settings import GetSettingsInteractor
from backend.application.use_cases.user import OperatorAccessInteractor
from backend.application.use_cases.wallet import (
    CreateTrxWithdrawInteractor,
    CreateUsdtWithdrawInteractor,
    CreateWalletInteractor,
    GetAccountBalanceInteractor,
    GetWalletInteractor,
)
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.order import OrderStatus
from backend.domain.entities.user import User
from backend.domain.templates.admin_texts import (
    admin_panel_menu_text,
    buy_exchange_order_details_notification_text,
    card_menu_text,
    change_buy_usdt_rate_menu_text,
    change_sell_usdt_rate_menu_text,
    change_tg_chat_id_menu_text,
    change_usdt_requisites_menu_text,
    contacts_admin_menu_text,
    delete_card_menu_text,
    get_mailing_content_text,
    get_new_card_text,
    get_new_contact_text,
    get_reject_note_text,
    get_user_id_for_search_text,
    get_username_for_search_text,
    get_withdraw_amount_text,
    mailing_menu_text,
    no_wallet_menu_text,
    private_key_text,
    remove_contact_menu_text,
    search_user_menu_text,
    sell_exchange_order_details_notification_text,
    settings_menu_text,
    statistic_menu_text,
    user_details_menu_text,
    wallet_menu_text,
    withdraw_reject_text,
    withdraw_transaction_details_text,
)
from backend.domain.templates.exception_texts import (
    incorrect_order_status_for_confirm_error_text,
    incorrect_order_status_for_reject_error_text,
    incorrect_withdraw_value_error_text,
    no_cards_error_text,
    no_contacts_for_remove_error_text,
    no_permission_error_text,
    not_enough_trx_for_commission_error_text,
    not_enough_trx_for_withdraw_error_text,
    not_enough_usdt_for_withdraw_error_text,
    only_admin_error_text,
    only_operator_error_text,
    transaction_error_text,
)
from backend.presentation.bot.states.admin import (
    AddCard,
    AddContact,
    CancelBuyOrder,
    CancelSellOrder,
    CreateMailing,
    CreateTrxWithdraw,
    CreateUsdtWithdraw,
    SearchUser,
    UpdateSettings,
)

router = Router()


@router.callback_query(F.data == 'admin_panel')
async def display_admin_panel(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    await state.clear()
    await call.message.edit_text(text=admin_panel_menu_text(), reply_markup=kb_builder.get_admin_menu_kb().as_markup())


@router.callback_query(F.data == 'settings_menu')
async def display_settings_menu(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetSettingsInteractor],
):
    await call.answer()
    settings = interactor()
    await call.message.edit_text(
        text=settings_menu_text(settings=settings),
        reply_markup=kb_builder.get_settings_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'cards_menu')
async def display_cards_menu(
    call: CallbackQuery,
    user: User,
    interactor: FromDishka[OperatorAccessInteractor],
):
    try:
        keyboard = interactor(user_id=user.id)
    except domain_exceptions.UserPermissionError:
        return await call.answer(only_operator_error_text(), show_alert=True)

    await call.answer()
    await call.message.edit_text(
        text=card_menu_text(),
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(F.data == 'add_card')
async def get_new_card(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_text(
        text=get_new_card_text(),
        reply_markup=kb_builder.get_card_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(AddCard.card)


@router.callback_query(F.data == 'delete_card_menu')
async def display_delete_card_menu(
    call: CallbackQuery,
    user: User,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetCardsInteractor],
):
    try:
        cards = await interactor(user_id=user.id)
    except exceptions.NoCardsError:
        return await call.answer(no_cards_error_text(), show_alert=True)

    await call.answer()
    await call.message.edit_text(
        text=delete_card_menu_text(),
        reply_markup=kb_builder.get_delete_card_menu(cards=cards).as_markup(),
    )


@router.callback_query(F.data.startswith('del_card'))
async def process_card_delete(
    call: CallbackQuery,
    user: User,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[DeleteCardInteractor],
):
    await call.answer()
    _, card_id = call.data.split(':')

    try:
        cards = await interactor(card_id=card_id, user_id=user.id)
        text = delete_card_menu_text()
        keyboard = kb_builder.get_delete_card_menu(cards=cards)
    except exceptions.NoCardsError:
        text = card_menu_text()
        keyboard = kb_builder.get_card_menu_kb()

    await call.message.edit_text(text=text, reply_markup=keyboard.as_markup())


@router.callback_query(F.data == 'set_usdt_requisites')
async def get_new_usdt_requisites(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_text(
        text=change_usdt_requisites_menu_text(),
        reply_markup=kb_builder.get_settings_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(UpdateSettings.usdt_requisites)


@router.callback_query(F.data == 'set_sell_usdt_rate')
async def get_new_sell_usdt_rate(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_text(
        text=change_sell_usdt_rate_menu_text(),
        reply_markup=kb_builder.get_settings_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(UpdateSettings.sell_usdt_rate)


@router.callback_query(F.data == 'set_buy_usdt_rate')
async def get_new_buy_usdt_rate(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_text(
        text=change_buy_usdt_rate_menu_text(),
        reply_markup=kb_builder.get_settings_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(UpdateSettings.buy_usdt_rate)


@router.callback_query(F.data == 'set_tg_chat_id')
async def get_new_moderation_channel_id(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_text(
        text=change_tg_chat_id_menu_text(),
        reply_markup=kb_builder.get_settings_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(UpdateSettings.tg_chat_id)


@router.callback_query(F.data == 'statistics_menu')
async def display_statistics_menu(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetExchangeStatInteractor],
):
    await call.answer()
    stats = await interactor()

    await call.message.edit_text(
        text=statistic_menu_text(
            buy_order_count=stats.buy_order_count,
            sell_order_count=stats.sell_order_count,
            total_sold_amount=stats.total_sold_amount,
            total_bought_amount=stats.total_bought_amount,
        ),
        reply_markup=kb_builder.get_admin_menu_return_kb().as_markup(),
    )


@router.callback_query(F.data == 'wallets_menu')
async def display_wallets_menu(
    call: CallbackQuery,
    user: User,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetAccountBalanceInteractor],
):
    keyboard = kb_builder.get_wallet_menu_kb().as_markup()
    try:
        account_balance = await interactor(user_id=user.id)
        text = wallet_menu_text(
            address=account_balance.address,
            usdt_balance=account_balance.usdt,
            trx_balance=account_balance.trx,
        )
    except domain_exceptions.WalletNotFoundError:
        text = no_wallet_menu_text()
    except domain_exceptions.UserPermissionError:
        return await call.answer(only_admin_error_text(), show_alert=True)

    await call.answer()
    await call.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(F.data == 'create_wallet')
async def process_create_wallet(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[CreateWalletInteractor],
):
    account_balance = await interactor()
    await call.message.edit_text(
        text=wallet_menu_text(
            address=account_balance.address,
            usdt_balance=account_balance.usdt,
            trx_balance=account_balance.trx,
        ),
        reply_markup=kb_builder.get_wallet_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'export_private_key')
async def process_export_private_key(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetWalletInteractor],
):
    await call.answer()
    wallet = await interactor()

    await call.message.answer(
        text=private_key_text(private_key_hex=wallet.private_key_hex),
        reply_markup=kb_builder.get_close_kb().as_markup(),
    )


@router.callback_query(F.data == 'withdraw_usdt')
async def get_usdt_withdraw_amount(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetAccountBalanceInteractor],
):
    account_balance = await interactor()
    if account_balance.usdt == 0:
        return await call.answer(not_enough_usdt_for_withdraw_error_text(), show_alert=True)

    await call.answer()
    msg = await call.message.edit_text(
        text=get_withdraw_amount_text(balance=account_balance.usdt, currency='USDT'),
        reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
    )
    await state.update_data(msg=msg)
    await state.set_state(CreateUsdtWithdraw.amount)


@router.callback_query(F.data == 'withdraw_trx')
async def get_trx_withdraw_amount(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetAccountBalanceInteractor],
):
    account_balance = await interactor()
    if account_balance.trx == 0:
        return await call.answer(not_enough_trx_for_commission_error_text(), show_alert=True)

    await call.answer()
    msg = await call.message.edit_text(
        text=get_withdraw_amount_text(balance=account_balance.trx, currency='TRX'),
        reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
    )
    await state.update_data(msg=msg)
    await state.set_state(CreateTrxWithdraw.amount)


@router.callback_query(F.data == 'confirm', CreateUsdtWithdraw.confirm)
async def process_withdraw_usdt(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[CreateUsdtWithdrawInteractor],
):
    try:
        state_data = await state.get_data()
        await state.clear()
        tx = await interactor(to_address=state_data['address'], amount=state_data['amount'])

        await call.message.edit_text(
            text=withdraw_transaction_details_text(tx_id=tx.tx_id),
            reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
        )

    except exceptions.IncorrectWithdrawAmountError:
        await call.message.edit_text(
            text=incorrect_withdraw_value_error_text(),
            reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
        )

    except exceptions.NotEnoughUsdtForTransferError:
        await call.message.edit_text(
            text=not_enough_usdt_for_withdraw_error_text(),
            reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
        )

    except exceptions.NotEnoughTrxForCommissionError:
        await call.message.edit_text(
            text=not_enough_trx_for_commission_error_text(),
            reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
        )

    except exceptions.TransactionError:
        await call.message.edit_text(
            text=transaction_error_text(),
            reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
        )


@router.callback_query(F.data == 'reject', CreateUsdtWithdraw.confirm)
async def reject_withdraw_usdt(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    await state.clear()

    await call.message.edit_text(
        text=withdraw_reject_text(),
        reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
    )


@router.callback_query(F.data == 'confirm', CreateTrxWithdraw.confirm)
async def process_withdraw_trx(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[CreateTrxWithdrawInteractor],
):
    try:
        await call.answer()

        state_data = await state.get_data()
        tx = await interactor(to_address=state_data['address'], amount=state_data['amount'])
        await call.message.edit_text(
            text=withdraw_transaction_details_text(tx_id=tx.tx_id),
            reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
        )
    except exceptions.IncorrectWithdrawAmountError:
        await call.message.edit_text(
            text=incorrect_withdraw_value_error_text(),
            reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
        )

    except exceptions.NotEnoughTrxForTransferError:
        await call.message.edit_text(
            text=not_enough_trx_for_withdraw_error_text(),
            reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
        )

    except exceptions.TransactionError:
        await call.message.edit_text(
            text=transaction_error_text(),
            reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
        )


@router.callback_query(F.data == 'reject', CreateTrxWithdraw.confirm)
async def reject_withdraw_trx(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    await state.clear()

    await call.message.edit_text(
        text=withdraw_reject_text(),
        reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
    )


@router.callback_query(F.data == 'users_menu')
async def display_users_menu(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    await state.clear()

    await call.message.edit_text(text=admin_panel_menu_text(), reply_markup=kb_builder.get_users_menu_kb().as_markup())


@router.callback_query(F.data == 'mailing_menu')
async def show_mailing_menu(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    await call.message.edit_text(text=mailing_menu_text(), reply_markup=kb_builder.get_mailing_menu_kb().as_markup())


@router.callback_query(F.data.split(':')[0] == 'mailing')
async def get_type_of_mailing(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    content_type = call.data.split(':')[1]

    msg = await call.message.edit_text(
        text=get_mailing_content_text(content_type=content_type),
        reply_markup=kb_builder.get_users_menu_return_kb().as_markup(),
    )
    await state.update_data(msg=msg, content_type=content_type)

    if content_type == 'text':
        await state.set_state(CreateMailing.text)
    else:
        await state.set_state(CreateMailing.media)


@router.callback_query(F.data == 'search_user_menu')
async def display_search_user_menu(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    await call.message.edit_text(
        text=search_user_menu_text(),
        reply_markup=kb_builder.get_search_user_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'search_by_id')
async def get_user_id_for_search(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_text(
        text=get_user_id_for_search_text(),
        reply_markup=kb_builder.get_users_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(SearchUser.user_id)


@router.callback_query(F.data == 'search_by_username')
async def get_username_for_search(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_text(
        text=get_username_for_search_text(),
        reply_markup=kb_builder.get_users_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(SearchUser.username)


@router.callback_query(F.data.startswith('ban_user') | F.data.startswith('unban_user'))
async def process_user_ban(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[UserBanInteractor],
):
    await call.answer()
    _, user_id = call.data.split(':')

    ban = True
    if 'unban_user' in call.data:
        ban = False

    details = await interactor(user_id=user_id, ban_status=ban)
    await call.message.edit_text(
        text=user_details_menu_text(
            user_id=details.user.id,
            username=details.user.username,
            created_at=details.user.created_at,
            buy_order_count=details.statistic.buy_order_count,
            sell_order_count=details.statistic.sell_order_count,
            total_bought_amount=details.statistic.total_bought_amount,
            total_sold_amount=details.statistic.total_sold_amount,
        ),
        reply_markup=kb_builder.get_user_details_menu_kb(
            user_id=details.user.id,
            is_banned=details.user.is_banned,
        ).as_markup(),
    )


@router.callback_query(F.data == 'admin_contacts_menu')
async def display_admin_contacts_menu(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    await state.clear()

    await call.message.edit_text(
        text=contacts_admin_menu_text(),
        reply_markup=kb_builder.get_admin_contacts_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'add_contact')
async def get_new_contact(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await call.answer()
    msg = await call.message.edit_text(
        text=get_new_contact_text(),
        reply_markup=kb_builder.get_admin_contacts_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(AddContact.contact)


@router.callback_query(F.data == 'remove_contact_menu')
async def display_contacts_for_remove(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetContactsInteractor],
):
    contacts = await interactor()
    if len(contacts) == 0:
        return await call.answer(no_contacts_for_remove_error_text(), show_alert=True)

    await call.answer()
    await call.message.edit_text(
        text=remove_contact_menu_text(),
        reply_markup=kb_builder.get_remove_contact_kb(contacts=contacts).as_markup(),
    )


@router.callback_query(F.data.startswith('remove_contact'))
async def remove_contact(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[DeleteContactInteractor],
):
    await call.answer()
    _, contact_id = call.data.split(':')
    contact_id = int(contact_id)

    contacts = await interactor(contact_id=contact_id)

    if len(contacts) == 0:
        return await call.message.edit_text(
            text=contacts_admin_menu_text(),
            reply_markup=kb_builder.get_admin_contacts_menu_kb().as_markup(),
        )

    await call.message.edit_text(
        text=remove_contact_menu_text(),
        reply_markup=kb_builder.get_remove_contact_kb(contacts=contacts).as_markup(),
    )


@router.callback_query(F.data.startswith('buy_order'))
async def display_buy_order(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetFullBuyOrderInteractor],
):
    await call.answer()
    await state.clear()

    _, order_id = call.data.split(':')

    order = await interactor(order_id=order_id)

    await call.message.edit_caption(
        caption=buy_exchange_order_details_notification_text(
            user_id=order.order.user_id,
            username=order.user.username,
            full_name=order.user.full_name,
            crypto_amount=order.order.crypto_amount,
            fiat_amount=order.order.fiat_amount,
            service_requisites=order.card.number.card_number,
            user_requisites=order.order.user_requisites.address,
        ),
        reply_markup=kb_builder.get_order_confirm_kb(
            order_id=order_id,
            order_type='buy',
            is_banned=order.user.is_banned,
        ).as_markup(),
    )


@router.callback_query(F.data.startswith('sell_order'))
async def display_sell_order(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetFullSellOrderInteractor],
):
    await call.answer()
    await state.clear()

    _, order_id = call.data.split(':')

    order = await interactor(order_id=order_id)

    await call.message.edit_caption(
        caption=sell_exchange_order_details_notification_text(
            user_id=order.order.user_id,
            username=order.user.username,
            full_name=order.user.full_name,
            crypto_amount=order.order.crypto_amount,
            fiat_amount=order.order.fiat_amount,
            service_requisites=order.order.service_requisites.address,
            user_requisites=order.order.user_requisites.card_number,
        ),
        reply_markup=kb_builder.get_order_confirm_kb(
            order_id=order_id,
            order_type='sell',
            is_banned=order.user.is_banned,
        ).as_markup(),
    )


@router.callback_query(F.data.startswith('ban_by_sell_order') | F.data.startswith('unban_by_sell_order'))
async def process_user_ban_by_sell(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[BanUserBySellOrderInteractor],
):
    await call.answer()
    await state.clear()

    _, order_id = call.data.split(':')

    ban = True
    if 'unban_by_sell_order' in call.data:
        ban = False

    order = await interactor(order_id=order_id, ban_status=ban)

    await call.message.edit_caption(
        caption=sell_exchange_order_details_notification_text(
            user_id=order.order.user_id,
            username=order.user.username,
            full_name=order.user.full_name,
            crypto_amount=order.order.crypto_amount,
            fiat_amount=order.order.fiat_amount,
            service_requisites=order.order.service_requisites.address,
            user_requisites=order.order.user_requisites.card_number,
        ),
        reply_markup=kb_builder.get_order_confirm_kb(
            order_id=order_id,
            order_type='sell',
            is_banned=order.user.is_banned,
        ).as_markup(),
    )


@router.callback_query(F.data.startswith('ban_by_buy_order') | F.data.startswith('unban_by_buy_order'))
async def process_user_ban_by_sell(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[BanUserByBuyOrderInteractor],
):
    await call.answer()
    await state.clear()

    _, order_id = call.data.split(':')

    ban = True
    if 'unban_by_buy_order' in call.data:
        ban = False

    order = await interactor(order_id=order_id, ban_status=ban)

    await call.message.edit_caption(
        caption=buy_exchange_order_details_notification_text(
            user_id=order.order.user_id,
            username=order.user.username,
            full_name=order.user.full_name,
            crypto_amount=order.order.crypto_amount,
            fiat_amount=order.order.fiat_amount,
            service_requisites=order.card.number.card_number,
            user_requisites=order.order.user_requisites.address,
        ),
        reply_markup=kb_builder.get_order_confirm_kb(
            order_id=order_id,
            order_type='buy',
            is_banned=order.user.is_banned,
        ).as_markup(),
    )


@router.callback_query(F.data.startswith('confirm_sell_order'))
async def process_confirm_sell_order(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[ConfirmSellOrderInteractor],
):
    _, order_id = call.data.split(':')

    try:
        order = await interactor(order_id=order_id)
        await call.answer()

        await call.message.edit_caption(
            caption=sell_exchange_order_details_notification_text(
                user_id=order.order.user_id,
                username=order.user.username,
                full_name=order.user.full_name,
                crypto_amount=order.order.crypto_amount,
                fiat_amount=order.order.fiat_amount,
                service_requisites=order.order.service_requisites.address,
                user_requisites=order.order.user_requisites.card_number,
            )
            + '\n\n✅ <b>Ордер подтвержден</b>',
            reply_markup=kb_builder.get_order_confirm_kb(
                order_id=order_id,
                order_type='buy',
                is_banned=order.user.is_banned,
            ).as_markup(),
        )

    except exceptions.InvalidOrderStatusForConfirmationError:
        await call.answer(incorrect_order_status_for_confirm_error_text(), show_alert=True)


@router.callback_query(F.data.startswith('confirm_buy_order'))
async def process_confirm_sell_order(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[ConfirmBuyOrderInteractor],
):
    _, order_id = call.data.split(':')

    try:
        order = await interactor(order_id=order_id)
        await call.answer()

        await call.message.edit_caption(
            caption=sell_exchange_order_details_notification_text(
                user_id=order.order.user_id,
                username=order.user.username,
                full_name=order.user.full_name,
                crypto_amount=order.order.crypto_amount,
                fiat_amount=order.order.fiat_amount,
                service_requisites=order.card.number.card_number,
                user_requisites=order.order.user_requisites.address,
            )
            + '\n\n✅ <b>Ордер подтвержден</b>',
            reply_markup=kb_builder.get_order_confirm_kb(
                order_id=order_id,
                order_type='buy',
                is_banned=order.user.is_banned,
            ).as_markup(),
        )

    except exceptions.InvalidOrderStatusForConfirmationError:
        await call.answer(incorrect_order_status_for_confirm_error_text(), show_alert=True)

    except exceptions.IncorrectWithdrawAmountError:
        await call.answer(incorrect_withdraw_value_error_text(), show_alert=True)

    except exceptions.NotEnoughUsdtForTransferError:
        await call.answer(not_enough_usdt_for_withdraw_error_text(), show_alert=True)

    except exceptions.NotEnoughTrxForCommissionError:
        await call.answer(not_enough_trx_for_commission_error_text(), show_alert=True)

    except exceptions.TransactionError:
        await call.answer(transaction_error_text(), show_alert=True)
    except domain_exceptions.UserPermissionError:
        await call.answer(no_permission_error_text(), show_alert=True)


@router.callback_query(F.data.startswith('reject_sell_order'))
async def get_sell_reject_note(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetSellOrderInteractor],
):
    _, order_id = call.data.split(':')

    order = await interactor(order_id=order_id)

    if order.status != OrderStatus.PAID:
        return await call.answer(incorrect_order_status_for_reject_error_text(), show_alert=True)

    await call.answer()
    msg = await call.message.edit_caption(
        caption=get_reject_note_text(),
        reply_markup=kb_builder.get_return_sell_order_kb(order_id=order_id).as_markup(),
    )

    await state.update_data(msg=msg, order_id=order_id)
    await state.set_state(CancelSellOrder.note)


@router.callback_query(F.data.startswith('reject_buy_order'))
async def get_buy_reject_note(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[GetBuyOrderInteractor],
):
    _, order_id = call.data.split(':')

    order = await interactor(order_id=order_id)

    if order.status != OrderStatus.PAID:
        return await call.answer(incorrect_order_status_for_reject_error_text(), show_alert=True)

    await call.answer()
    msg = await call.message.edit_caption(
        caption=get_reject_note_text(),
        reply_markup=kb_builder.get_return_buy_order_kb(order_id=order_id).as_markup(),
    )

    await state.update_data(msg=msg, order_id=order_id)
    await state.set_state(CancelBuyOrder.note)
