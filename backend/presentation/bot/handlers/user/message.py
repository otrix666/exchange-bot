from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dishka import FromDishka

from backend.application import interfaces
from backend.application.use_cases.buy_order import CalculateBuyOrderAmountInteractor, CreateBuyOrderInteractor
from backend.application.use_cases.card import GetCardInteractor
from backend.application.use_cases.sell_order import CalculateSellOrderAmountInteractor, CreateSellOrderInteractor
from backend.application.use_cases.settings import GetSettingsInteractor
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.user import User
from backend.domain.templates.exception_texts import (
    incorrect_card_requisites_error_text,
    incorrect_exchange_amount_error_text,
    incorrect_usdt_address_error_text,
    no_cards_for_order_error_text,
)
from backend.domain.templates.user_texts import (
    buy_exchange_order_details_text,
    get_card_requisites_text,
    get_usdt_requisites_text,
    success_order_creat_text,
)
from backend.domain.vo.requisites import CardRequisites, UsdtRequisites
from backend.presentation.bot.states.user import CreateBuyExchangeOrder, CreateSellExchangeOrder

router = Router()


@router.message(CreateBuyExchangeOrder.amount)
async def get_user_usdt_requisites(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
    interactor: FromDishka[CalculateBuyOrderAmountInteractor],
):
    state_data = await state.get_data()

    try:
        await message.delete()
        order_amount = interactor(buy_amount=message.text)
        await state_data['msg'].edit_caption(
            caption=get_usdt_requisites_text(order_amount=order_amount),
            reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
        )
        await state.update_data(order_amount=order_amount, buy_amount=message.text)
        await state.set_state(CreateBuyExchangeOrder.requisites)

    except exceptions.InvalidAmountError:
        try:
            await state_data['msg'].edit_caption(
                caption=incorrect_exchange_amount_error_text(amount=message.text),
                reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
            )
        except:
            pass


@router.message(CreateSellExchangeOrder.amount)
async def get_user_card_requisites(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
    interactor: FromDishka[CalculateSellOrderAmountInteractor],
):
    state_data = await state.get_data()

    try:
        await message.delete()
        order_amount = interactor(sell_amount=message.text)
        await state_data['msg'].edit_caption(
            caption=get_card_requisites_text(order_amount=order_amount),
            reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
        )
        await state.update_data(order_amount=order_amount, sell_amount=message.text)
        await state.set_state(CreateSellExchangeOrder.requisites)

    except exceptions.InvalidAmountError:
        try:
            await state_data['msg'].edit_caption(
                caption=incorrect_exchange_amount_error_text(amount=message.text),
                reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
            )
        except:
            pass


@router.message(CreateBuyExchangeOrder.requisites)
async def get_buy_exchange_order_cheque(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
    interactor: FromDishka[GetCardInteractor],
):
    await message.delete()
    state_data = await state.get_data()
    try:
        requisites = UsdtRequisites(address=message.text)
        try:
            card = await interactor()
        except exceptions.NoCardsError:
            return await state_data['msg'].edit_caption(
                caption=no_cards_for_order_error_text(),
                reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
            )

        await state_data['msg'].edit_caption(
            caption=buy_exchange_order_details_text(
                crypto_amount=state_data['buy_amount'],
                fiat_amount=str(state_data['order_amount']),
                service_requisites=card.number.card_number,
                user_requisites=requisites.address,
            ),
            reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
        )

        await state.update_data(requisites=requisites, card=card)
        await state.set_state(CreateBuyExchangeOrder.cheque)
    except domain_exceptions.InvalidUsdtAddressError:
        try:
            await state_data['msg'].edit_caption(
                caption=incorrect_usdt_address_error_text(address=message.text),
                reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
            )
        except:
            pass


@router.message(CreateSellExchangeOrder.requisites)
async def get_sell_exchange_order_cheque(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
    interactor: FromDishka[GetSettingsInteractor],
):
    await message.delete()
    state_data = await state.get_data()
    try:
        requisites = CardRequisites(card_number=message.text)
        settings = interactor()
        await state_data['msg'].edit_caption(
            caption=buy_exchange_order_details_text(
                crypto_amount=state_data['sell_amount'],
                fiat_amount=str(state_data['order_amount']),
                service_requisites=settings.usdt_requisites,
                user_requisites=requisites.card_number,
            ),
            reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
        )

        await state.update_data(requisites=requisites)
        await state.set_state(CreateSellExchangeOrder.cheque)
    except domain_exceptions.InvalidCardNumberError:
        try:
            await state_data['msg'].edit_caption(
                caption=incorrect_card_requisites_error_text(card_number=message.text),
                reply_markup=kb_builder.get_exchange_menu_return_kb().as_markup(),
            )
        except:
            pass


@router.message(CreateBuyExchangeOrder.cheque)
async def get_sell_exchange_order_cheque(
    message: Message,
    state: FSMContext,
    user: User,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
    interactor: FromDishka[CreateBuyOrderInteractor],
):
    await message.delete()
    if message.content_type == 'photo':
        state_data = await state.get_data()
        await state.clear()

        order = await interactor(
            message=message,  # type: ignore
            user=user,
            crypto_amount=state_data['buy_amount'],
            fiat_amount=state_data['order_amount'],
            user_requisites=state_data['requisites'],
            card=state_data['card'],
        )

        await state_data['msg'].edit_caption(
            caption=success_order_creat_text(order_id=order.id, ticker=order.ticker),
            reply_markup=kb_builder.get_main_menu_return_kb().as_markup(),
        )


@router.message(CreateSellExchangeOrder.cheque)
async def get_sell_exchange_order_cheque(
    message: Message,
    state: FSMContext,
    user: User,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
    interactor: FromDishka[CreateSellOrderInteractor],
):
    await message.delete()
    if message.content_type == 'photo':
        state_data = await state.get_data()
        await state.clear()

        order = await interactor(
            message=message,  # type: ignore
            user=user,
            crypto_amount=state_data['sell_amount'],
            fiat_amount=state_data['order_amount'],
            user_requisites=state_data['requisites'],
        )

        await state_data['msg'].edit_caption(
            caption=success_order_creat_text(order_id=order.id, ticker=order.ticker),
            reply_markup=kb_builder.get_main_menu_return_kb().as_markup(),
        )
