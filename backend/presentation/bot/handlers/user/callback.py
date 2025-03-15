from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder
from dishka import FromDishka

from backend.application import interfaces
from backend.application.use_cases.contact import GetContactsInteractor
from backend.application.use_cases.user import GetUserExchangeHistoryReportInteractor, GetUserExchangeStatInteractor
from backend.domain.entities.user import User
from backend.domain.templates.user_texts import (
    contacts_menu_text,
    exchange_menu_text,
    get_buy_usdt_amount_text,
    get_sell_usdt_amount_text,
    main_menu_text,
    profile_menu_text,
)
from backend.presentation.bot.states.user import CreateBuyExchangeOrder, CreateSellExchangeOrder

router = Router()


@router.callback_query(F.data == 'main_menu')
async def display_user_main_menu(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
) -> None:
    await call.answer()
    await call.message.edit_caption(caption=main_menu_text(), reply_markup=kb_builder.get_main_menu_kb().as_markup())


@router.callback_query(F.data == 'profile_menu')
async def display_user_profile(
    call: CallbackQuery,
    user: User,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
    interactor: FromDishka[GetUserExchangeStatInteractor],
) -> None:
    await call.answer()
    stats = await interactor(user_id=user.id)

    await call.message.edit_caption(
        caption=profile_menu_text(
            user_id=user.id,
            created_at=user.created_at,
            buy_order_count=stats.buy_order_count,
            sell_order_count=stats.sell_order_count,
            total_bought_amount=stats.total_bought_amount,
            total_sold_amount=stats.total_sold_amount,
        ),
        reply_markup=kb_builder.get_profile_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'order_history')
async def display_user_order_history(
    call: CallbackQuery,
    user: User,
    interactor: FromDishka[GetUserExchangeHistoryReportInteractor],
):
    await call.answer()

    reports = await interactor(user_id=user.id)

    media_group = MediaGroupBuilder()
    media_group.add_document(media=BufferedInputFile(file=reports.sell, filename='sell orders history.csv'))
    media_group.add_document(media=BufferedInputFile(file=reports.buy, filename='buy orders history.csv'))

    await call.message.answer_media_group(media=media_group.build())


@router.callback_query(F.data == 'exchange_menu')
async def display_exchange_menu(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
):
    await call.answer()
    await state.clear()

    await call.message.edit_caption(
        caption=exchange_menu_text(),
        reply_markup=kb_builder.get_exchange_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'contacts_menu')
async def display_contacts_menu(
    call: CallbackQuery,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
    interactor: FromDishka[GetContactsInteractor],
):
    await call.answer()

    contacts = await interactor()

    await call.message.edit_caption(
        caption=contacts_menu_text(),
        reply_markup=kb_builder.get_contact_menu_kb(contacts=contacts).as_markup(),
    )


@router.callback_query(F.data == 'buy')
async def get_buy_usdt_amount(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
):
    msg = await call.message.edit_caption(
        caption=get_buy_usdt_amount_text(),
        reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(CreateBuyExchangeOrder.amount)


@router.callback_query(F.data == 'sell')
async def get_buy_usdt_amount(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
):
    msg = await call.message.edit_caption(
        caption=get_sell_usdt_amount_text(),
        reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(CreateSellExchangeOrder.amount)
