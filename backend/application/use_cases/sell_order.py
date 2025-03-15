from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Protocol

from backend.application import exceptions, interfaces
from backend.application.services.tg_helpers import get_file_id_by_content_type
from backend.domain.entities.order import OrderStatus, SellOrder, Ticker
from backend.domain.entities.user import User
from backend.domain.templates.admin_texts import sell_exchange_order_details_notification_text
from backend.domain.vo.requisites import CardRequisites, UsdtRequisites


class CalculateSellOrderAmountInteractor:
    def __init__(
        self,
        settings_reader: interfaces.SettingsReader,
    ):
        self._settings_reader = settings_reader

    def __call__(self, sell_amount: str) -> Decimal:
        settings = self._settings_reader.read()
        try:
            return Decimal(sell_amount) * Decimal(settings.sell_usdt_rate)
        except InvalidOperation:
            raise exceptions.InvalidAmountError


class CreateSellOrderInteractor:
    def __init__(
        self,
        order_saver: interfaces.SellOrderSaver,
        settings_reader: interfaces.SettingsReader,
        adm_kb_builder: interfaces.AdminKeyboardBuilder,
        broadcaster: interfaces.Broadcaster,
        uuid_generator: interfaces.UUIDGenerator,
    ):
        self._order_saver = order_saver
        self._settings_reader = settings_reader
        self._adm_kb_builder = adm_kb_builder
        self._broadcaster = broadcaster
        self._uuid_generator = uuid_generator

    async def __call__(
        self,
        message: interfaces.Message,
        user: User,
        crypto_amount: Decimal,
        fiat_amount: Decimal,
        user_requisites: CardRequisites,
    ) -> SellOrder:
        settings = self._settings_reader.read()

        order = SellOrder(
            id=self._uuid_generator(),
            crypto_amount=crypto_amount,
            fiat_amount=fiat_amount,
            ticker=Ticker.RUB_USDT,
            status=OrderStatus.PAID,
            created_at=datetime.now(),
            completed_at=None,
            note=None,
            user_requisites=user_requisites,
            service_requisites=UsdtRequisites(address=settings.usdt_requisites),
            user_id=user.id,
            cheque_id=None,
        )

        saved_order = await self._order_saver.save(order=order)

        file_id = get_file_id_by_content_type(message=message)

        await self._broadcaster.send_message(
            user_id=settings.tg_chat_id,
            photo_id=file_id,
            caption=sell_exchange_order_details_notification_text(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                crypto_amount=crypto_amount,
                fiat_amount=fiat_amount,
                service_requisites=settings.usdt_requisites,
                user_requisites=user_requisites.card_number,
            ),
            keyboard=self._adm_kb_builder.get_order_confirm_kb(
                order_id=saved_order.id,
                order_type='sell',
                is_banned=user.is_banned,
            ),
        )

        return saved_order


class GetSellOrderInteractor:
    def __init__(
        self,
        reader: interfaces.SellOrderReader,
    ):
        self._reader = reader

    async def __call__(self, order_id: int) -> SellOrder:
        order = await self._reader.get_by_id(order_id=order_id)
        return order


class SellOrderUpdateManager(interfaces.SellOrderReader, interfaces.SellOrderUpdater, Protocol): ...
