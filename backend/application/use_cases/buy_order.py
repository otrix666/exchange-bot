from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Protocol
from uuid import UUID

from backend.application import exceptions, interfaces
from backend.application.services.tg_helpers import get_file_id_by_content_type
from backend.config import Config
from backend.domain.entities.card import Card
from backend.domain.entities.order import BuyOrder, OrderStatus, Ticker
from backend.domain.entities.user import User
from backend.domain.templates.admin_texts import (
    buy_exchange_order_details_notification_text,
    operator_norification_text,
)
from backend.domain.vo.requisites import UsdtRequisites


class CalculateBuyOrderAmountInteractor:
    def __init__(
        self,
        settings_reader: interfaces.SettingsReader,
    ):
        self._settings_reader = settings_reader

    def __call__(self, buy_amount: str) -> Decimal:
        settings = self._settings_reader.read()
        try:
            return Decimal(buy_amount) * Decimal(settings.buy_usdt_rate)
        except InvalidOperation:
            raise exceptions.InvalidAmountError


class CreateBuyOrderInteractor:
    def __init__(
        self,
        order_saver: interfaces.BuyOrderSaver,
        card_reader: interfaces.CardReader,
        settings_reader: interfaces.SettingsReader,
        adm_kb_builder: interfaces.AdminKeyboardBuilder,
        broadcaster: interfaces.Broadcaster,
        uuid_generator: interfaces.UUIDGenerator,
        config: Config,
    ):
        self._order_saver = order_saver
        self._card_reader = card_reader
        self._settings_reader = settings_reader
        self._adm_kb_builder = adm_kb_builder
        self._broadcaster = broadcaster
        self._uuid_generator = uuid_generator
        self._config = config

    async def __call__(
        self,
        message: interfaces.Message,
        user: User,
        crypto_amount: Decimal,
        fiat_amount: Decimal,
        user_requisites: UsdtRequisites,
        card: Card,
    ) -> BuyOrder:
        order_id = self._uuid_generator()
        order = BuyOrder(
            id=order_id,
            crypto_amount=crypto_amount,
            fiat_amount=fiat_amount,
            ticker=Ticker.RUB_USDT,
            status=OrderStatus.PAID,
            created_at=datetime.now(),
            completed_at=None,
            note=None,
            user_requisites=user_requisites,
            card_id=card.id,
            user_id=user.id,
            cheque_id=None,
        )

        saved_order = await self._order_saver.save(order=order)
        settings = self._settings_reader.read()

        file_id = get_file_id_by_content_type(message=message)

        msg = await self._broadcaster.send_message(
            user_id=settings.tg_chat_id,
            photo_id=file_id,
            caption=buy_exchange_order_details_notification_text(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                crypto_amount=crypto_amount,
                fiat_amount=fiat_amount,
                service_requisites=card.number.card_number,
                user_requisites=user_requisites.address,
            ),
            keyboard=self._adm_kb_builder.get_order_confirm_kb(
                order_id=saved_order.id,
                order_type='buy',
                is_banned=user.is_banned,
            ),
        )

        await self._broadcaster.send_message(
            user_id=card.user_id,
            text=operator_norification_text(order_id=order_id),
            keyboard=self._adm_kb_builder.get_operator_notifications_kb(
                chat_id=settings.tg_chat_id.replace('-100', ''),
                message_id=str(msg.message_id),
            ),
        )

        return saved_order


class GetBuyOrderInteractor:
    def __init__(
        self,
        reader: interfaces.BuyOrderReader,
    ):
        self._reader = reader

    async def __call__(self, order_id: UUID) -> BuyOrder:
        order = await self._reader.get_by_id(order_id=order_id)
        return order


class BuyOrderUpdateManager(interfaces.BuyOrderReader, interfaces.BuyOrderUpdater, Protocol): ...
