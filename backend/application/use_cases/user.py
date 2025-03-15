import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from decimal import Decimal
from functools import partial
from typing import Protocol

from backend.application import interfaces
from backend.application.dto.report import CsvExchangeReport
from backend.application.dto.statistic import ExchangeStat
from backend.config import Config
from backend.domain import exceptions
from backend.domain.entities.order import OrderStatus
from backend.domain.entities.user import User


class SyncTelegramUserInteractor:
    def __init__(
        self,
        saver: interfaces.UserSaver,
    ):
        self._saver = saver

    async def __call__(self, user_id: int, username: str, full_name: str) -> User:
        user = User(
            id=user_id,
            username=username,
            full_name=full_name,
            is_banned=False,
            created_at=datetime.now(),
        )

        saved_user = await self._saver.save_or_update(user=user)
        return saved_user


class PanelAccessInteractor:
    def __init__(
        self,
        config: Config,
        access_manager: interfaces.AccessManager,
        kb_builder: interfaces.AdminKeyboardBuilder,
    ):
        self._config = config
        self._access_manager = access_manager
        self._kb_builder = kb_builder

    def __call__(self, user_id: int) -> interfaces.Keyboard:
        if not self._access_manager.is_admin(
            user_id=user_id,
            admin_ids=self._config.bot.admins,
        ) or not self._access_manager.is_admin(user_id=user_id, admin_ids=self._config.bot.operators):
            raise exceptions.UserPermissionError

        return self._kb_builder.get_admin_menu_kb()


class OperatorAccessInteractor:
    def __init__(
        self,
        config: Config,
        access_manager: interfaces.AccessManager,
        kb_builder: interfaces.AdminKeyboardBuilder,
    ):
        self._config = config
        self._access_manager = access_manager
        self._kb_builder = kb_builder

    def __call__(self, user_id: int) -> interfaces.Keyboard:
        if not self._access_manager.is_admin(user_id=user_id, admin_ids=self._config.bot.operators):
            raise exceptions.UserPermissionError
        return self._kb_builder.get_card_menu_kb()


class GetUserExchangeStatInteractor:
    def __init__(
        self,
        sell_order_reader: interfaces.SellOrderReader,
        buy_order_reader: interfaces.BuyOrderReader,
    ):
        self._sell_order_reader = sell_order_reader
        self._buy_order_reader = buy_order_reader

    async def __call__(self, user_id: int) -> ExchangeStat:
        sell_orders = await self._sell_order_reader.get_all_by_user_id(user_id=user_id)
        buy_orders = await self._buy_order_reader.get_all_by_user_id(user_id=user_id)

        total_sold_amount = sum(
            (order.crypto_amount for order in sell_orders if order.status == OrderStatus.COMPLETED),
            Decimal('0.0'),
        )
        total_bought_amount = sum(
            (order.order.crypto_amount for order in buy_orders if order.order.status == OrderStatus.COMPLETED),
            Decimal('0.0'),
        )

        sell_order_count = len([order for order in sell_orders if order.status == OrderStatus.COMPLETED])
        buy_order_count = len([order for order in buy_orders if order.order.status == OrderStatus.COMPLETED])

        return ExchangeStat(
            total_sold_amount=total_sold_amount,
            total_bought_amount=total_bought_amount,
            sell_order_count=sell_order_count,
            buy_order_count=buy_order_count,
        )


class UserUpdateManager(interfaces.UserReader, interfaces.UserUpdater, Protocol): ...


class GetUserExchangeHistoryReportInteractor:
    def __init__(
        self,
        sell_order_reader: interfaces.SellOrderReader,
        buy_order_reader: interfaces.BuyOrderReader,
        csv_creator: interfaces.CsvCreator,
        thread_pool: ThreadPoolExecutor,
    ):
        self._sell_order_reader = sell_order_reader
        self._buy_order_reader = buy_order_reader
        self._csv_creator = csv_creator
        self._thread_pool = thread_pool

    async def __call__(self, user_id: int) -> CsvExchangeReport:
        sell_orders = await self._sell_order_reader.get_all_by_user_id(user_id=user_id)
        buy_orders = await self._buy_order_reader.get_all_by_user_id(user_id=user_id)

        loop = asyncio.get_event_loop()

        calls = [
            loop.run_in_executor(self._thread_pool, partial(self._csv_creator.create_report, sell_orders)),
            loop.run_in_executor(self._thread_pool, partial(self._csv_creator.create_report, buy_orders)),
        ]

        sell_report, buy_report = await asyncio.gather(*calls)

        return CsvExchangeReport(
            sell=sell_report,
            buy=buy_report,
        )
