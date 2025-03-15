from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dishka import FromDishka

from backend.application import interfaces
from backend.application.services.tg_helpers import get_file_id_by_content_type, get_spam_keyboard
from backend.application.use_cases.admin import (
    MailingInteractor,
    RejectBuyOrderInteractor,
    RejectSellOrderInteractor,
    SearchUserByIdInteractor,
    SearchUserByUsernameInteractor,
)
from backend.application.use_cases.card import SaveCardInteractor
from backend.application.use_cases.contact import SaveContactInteractor
from backend.application.use_cases.settings import (
    UpdateBuyUsdtRateInteractor,
    UpdateSellUsdtRateInteractor,
    UpdateTgChatIdInteractor,
    UpdateUsdtRequisitesInteractor,
)
from backend.application.use_cases.user import PanelAccessInteractor
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.user import User
from backend.domain.templates.admin_texts import (
    admin_panel_menu_text,
    buy_exchange_order_details_notification_text,
    card_menu_text,
    contacts_admin_menu_text,
    example_mailing_text,
    get_address_for_withdraw,
    get_mailing_button_text,
    get_mailing_caption_text,
    sell_exchange_order_details_notification_text,
    settings_menu_text,
    user_details_menu_text,
    withdraw_details_text,
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


@router.message(Command('admin'))
async def display_admin_panel(
    message: Message,
    user: User,
    interactor: FromDishka[PanelAccessInteractor],
) -> None:
    try:
        keyboard = interactor(user_id=user.id)
        await message.answer(text=admin_panel_menu_text(), reply_markup=keyboard.as_markup())
    except domain_exceptions.UserPermissionError:
        pass


@router.message(AddCard.card)
async def process_update_card_requisites(
    message: Message,
    user: User,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[SaveCardInteractor],
):
    try:
        await message.delete()
        state_data = await state.get_data()
        await state.clear()

        await interactor(user_id=user.id, card_number=message.text)
        await state_data['msg'].edit_text(
            text=card_menu_text(),
            reply_markup=kb_builder.get_card_menu_kb().as_markup(),
        )
    except domain_exceptions.InvalidCardNumberError:
        pass


@router.message(UpdateSettings.usdt_requisites)
async def process_update_usdt_requisites(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[UpdateUsdtRequisitesInteractor],
):
    try:
        await message.delete()
        state_data = await state.get_data()
        await state.clear()

        settings = interactor(usdt_requisites=message.text)
        await state_data['msg'].edit_text(
            text=settings_menu_text(settings=settings),
            reply_markup=kb_builder.get_settings_menu_kb().as_markup(),
        )
    except domain_exceptions.UserPermissionError:
        pass


@router.message(UpdateSettings.sell_usdt_rate)
async def process_update_sell_usdt_rate(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[UpdateSellUsdtRateInteractor],
):
    try:
        await message.delete()
        state_data = await state.get_data()
        await state.clear()

        settings = interactor(sell_usdt_rate=message.text)
        await state_data['msg'].edit_text(
            text=settings_menu_text(settings=settings),
            reply_markup=kb_builder.get_settings_menu_kb().as_markup(),
        )
    except domain_exceptions.UserPermissionError:
        pass


@router.message(UpdateSettings.buy_usdt_rate)
async def process_update_buy_usdt_rate(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[UpdateBuyUsdtRateInteractor],
):
    try:
        await message.delete()
        state_data = await state.get_data()
        await state.clear()

        settings = interactor(buy_usdt_rate=message.text)
        await state_data['msg'].edit_text(
            text=settings_menu_text(settings=settings),
            reply_markup=kb_builder.get_settings_menu_kb().as_markup(),
        )
    except domain_exceptions.UserPermissionError:
        pass


@router.message(UpdateSettings.tg_chat_id)
async def process_update_tg_chat_id(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[UpdateTgChatIdInteractor],
):
    try:
        await message.delete()
        state_data = await state.get_data()
        await state.clear()

        settings = interactor(tg_chat_id=message.text)
        await state_data['msg'].edit_text(
            text=settings_menu_text(settings=settings),
            reply_markup=kb_builder.get_settings_menu_kb().as_markup(),
        )
    except domain_exceptions.UserPermissionError:
        pass


@router.message(CreateUsdtWithdraw.amount)
async def get_withdraw_usdt_address(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await message.delete()
    state_data = await state.get_data()

    await state_data['msg'].edit_text(
        text=get_address_for_withdraw(),
        reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
    )
    await state.update_data(amount=message.text)
    await state.set_state(CreateUsdtWithdraw.address)


@router.message(CreateUsdtWithdraw.address)
async def get_withdraw_usdt_confirmation(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await message.delete()
    state_data = await state.get_data()

    await state_data['msg'].edit_text(
        text=withdraw_details_text(
            to_address=message.text,
            amount=state_data['amount'],
            currency='USDT',
        ),
        reply_markup=kb_builder.get_withdraw_confirmation_kb().as_markup(),
    )
    await state.update_data(address=message.text)
    await state.set_state(CreateUsdtWithdraw.confirm)


@router.message(CreateTrxWithdraw.amount)
async def get_withdraw_trx_address(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await message.delete()
    state_data = await state.get_data()

    await state_data['msg'].edit_text(
        text=get_address_for_withdraw(),
        reply_markup=kb_builder.get_wallet_manu_return_kb().as_markup(),
    )
    await state.update_data(amount=message.text)
    await state.set_state(CreateTrxWithdraw.address)


@router.message(CreateTrxWithdraw.address)
async def get_withdraw_trx_confirmation(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await message.delete()
    state_data = await state.get_data()

    await state_data['msg'].edit_text(
        text=withdraw_details_text(
            to_address=message.text,
            amount=state_data['amount'],
            currency='TRX',
        ),
        reply_markup=kb_builder.get_withdraw_confirmation_kb().as_markup(),
    )
    await state.update_data(address=message.text)
    await state.set_state(CreateTrxWithdraw.confirm)


@router.message(CreateMailing.text)
async def get_mailing_button(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await message.delete()
    state_data = await state.get_data()

    await state_data['msg'].edit_text(
        text=get_mailing_button_text(),
        reply_markup=kb_builder.get_users_menu_return_kb().as_markup(),
    )
    await state.update_data(text=message.text)
    await state.set_state(CreateMailing.button)


@router.message(CreateMailing.media)
async def get_caption_for_spam(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await message.delete()
    content = message.content_type
    content_list = ['photo', 'animation', 'video']
    if content in content_list:
        state_data = await state.get_data()
        await state_data['msg'].edit_text(
            text=get_mailing_caption_text(content_type=content),
            reply_markup=kb_builder.get_users_menu_return_kb().as_markup(),
        )

        file_id = get_file_id_by_content_type(message=message)  # type: ignore
        await state.update_data(file=file_id)

        await state.set_state(CreateMailing.caption)


@router.message(CreateMailing.caption)
async def get_keyboard_for_media_spam(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await message.delete()
    state_data = await state.get_data()

    await state_data['msg'].edit_text(
        text=get_mailing_button_text(),
        reply_markup=kb_builder.get_users_menu_return_kb().as_markup(),
    )
    await state.update_data(caption=message.text)
    await state.set_state(CreateMailing.button)


@router.message(CreateMailing.button)
async def display_mailing_example(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
):
    await message.delete()
    state_data = await state.get_data()

    keyboard = get_spam_keyboard(message_text=message.text, kb_builder=kb_builder)
    await state.update_data(keyboard=keyboard)
    await state_data['msg'].delete()

    if state_data['content_type'] == 'text':
        msg = await message.answer(
            text=example_mailing_text(mailing_text=state_data['text']),
            reply_markup=keyboard.as_markup(),
        )

    elif state_data['content_type'] == 'photo':
        msg = await message.answer_photo(
            photo=state_data['file'],
            caption=example_mailing_text(mailing_text=state_data['caption']),
            reply_markup=keyboard.as_markup(),
        )

    elif state_data['content_type'] == 'video':
        msg = await message.answer_video(
            video=state_data['file'],
            caption=example_mailing_text(mailing_text=state_data['caption']),
            reply_markup=keyboard.as_markup(),
        )

    elif state_data['content_type'] == 'animation':
        msg = await message.answer_animation(
            animation=state_data['file'],
            caption=example_mailing_text(mailing_text=state_data['caption']),
            reply_markup=keyboard.as_markup(),
        )
    else:
        msg = None

    await state.update_data(msg=msg)
    await state.set_state(CreateMailing.confirm)


@router.message(CreateMailing.confirm)
async def get_confirm(
    message: Message,
    state: FSMContext,
    interactor: FromDishka[MailingInteractor],
):
    await message.delete()
    state_data = await state.get_data()
    await state.clear()
    await state_data['msg'].delete()

    if '+' in message.text:
        await message.answer('➕ <b>Рассылка успешно запущена!</b>')

        mailing_stat = await interactor(
            keyboard=state_data.get('keyboard'),
            content_type=state_data.get('content_type'),
            text=state_data.get('text', None),
            caption=state_data.get('caption', None),
            file_id=state_data.get('file_id', None),
        )

        await message.answer(
            '✅ <b>Рассылка успешно окончена!</b>\n\n'
            f'➕ <b>Успешно отправлено: {mailing_stat.success} смс.</b>\n'
            f'➖ <b>Не отправлено: {mailing_stat.un_success} смс.</b>',
        )
    else:
        await message.answer('➖ <b>Рассылка успешно отменена!</b>')


@router.message(SearchUser.user_id)
async def display_user_info_by_id(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[SearchUserByIdInteractor],
):
    await message.delete()
    state_data = await state.get_data()

    try:
        details = await interactor(user_id=message.text)
        await state_data['msg'].edit_text(
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
    except exceptions.IncorrectUserIdError:
        pass
    except domain_exceptions.UserNotFoundByIdError:
        pass


@router.message(SearchUser.username)
async def display_user_info_by_username(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[SearchUserByUsernameInteractor],
):
    await message.delete()
    state_data = await state.get_data()

    try:
        details = await interactor(username=message.text)
        await state_data['msg'].edit_text(
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
    except exceptions.IncorrectUserIdError:
        pass
    except domain_exceptions.UserNotFoundByUsernameError:
        pass


@router.message(AddContact.contact)
async def save_new_contact(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[SaveContactInteractor],
):
    await message.delete()
    try:
        state_data = await state.get_data()
        await state.clear()

        await interactor(contact=message.text)
        return await state_data['msg'].edit_text(
            text=contacts_admin_menu_text(),
            reply_markup=kb_builder.get_admin_contacts_menu_kb().as_markup(),
        )

    except exceptions.IncorrectContactError:
        pass


@router.message(CancelBuyOrder.note)
async def process_reject_buy_order(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[RejectBuyOrderInteractor],
):
    await message.delete()
    state_data = await state.get_data()
    await state.clear()

    order = await interactor(order_id=state_data['order_id'], note=message.text)

    await state_data['msg'].edit_caption(
        caption=buy_exchange_order_details_notification_text(
            user_id=order.order.user_id,
            username=order.user.username,
            full_name=order.user.full_name,
            crypto_amount=order.order.crypto_amount,
            fiat_amount=order.order.fiat_amount,
            service_requisites=order.card.number.card_number,
            user_requisites=order.order.user_requisites.address,
        )
        + '\n\n❌ <b>Ордер отменен</b>',
        reply_markup=kb_builder.get_order_confirm_kb(
            order_id=order.order.id,
            order_type='buy',
            is_banned=order.user.is_banned,
        ).as_markup(),
    )


@router.message(CancelSellOrder.note)
async def process_reject_sell_order(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.AdminKeyboardBuilder],
    interactor: FromDishka[RejectSellOrderInteractor],
):
    await message.delete()
    state_data = await state.get_data()
    await state.clear()

    order = await interactor(order_id=state_data['order_id'], note=message.text)

    await state_data['msg'].edit_caption(
        caption=sell_exchange_order_details_notification_text(
            user_id=order.order.user_id,
            username=order.user.username,
            full_name=order.user.full_name,
            crypto_amount=order.order.crypto_amount,
            fiat_amount=order.order.fiat_amount,
            service_requisites=order.order.service_requisites.address,
            user_requisites=order.order.user_requisites.card_number,
        )
        + '\n\n❌ <b>Ордер отменен</b>',
        reply_markup=kb_builder.get_order_confirm_kb(
            order_id=order.order.id,
            order_type='sell',
            is_banned=order.user.is_banned,
        ).as_markup(),
    )
