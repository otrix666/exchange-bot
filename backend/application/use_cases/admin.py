from datetime import datetime
from decimal import Decimal
from uuid import UUID

from backend.application import exceptions, interfaces
from backend.application.dto.admin import BasicUser, UserProfile
from backend.application.dto.statistic import ExchangeStat, MailingStat
from backend.application.use_cases.buy_order import BuyOrderUpdateManager
from backend.application.use_cases.sell_order import SellOrderUpdateManager
from backend.application.use_cases.user import UserUpdateManager
from backend.domain import exceptions as domain_exceptions
from backend.domain.entities.admin import FullBuyOrder, FullSellOrder
from backend.domain.entities.order import OrderStatus
from backend.domain.templates.user_texts import (
    confirm_buy_order_notification_text,
    confirm_sell_order_notification_text,
    reject_buy_order_notification_text,
    reject_sell_order_notification_text,
)


class GetExchangeStatInteractor:
    def __init__(
        self,
        sell_order_reader: interfaces.SellOrderReader,
        buy_order_reader: interfaces.BuyOrderReader,
    ):
        self._sell_order_reader = sell_order_reader
        self._buy_order_reader = buy_order_reader

    async def __call__(self) -> ExchangeStat:
        sell_orders = await self._sell_order_reader.get_all()
        buy_orders = await self._buy_order_reader.get_all()

        total_sold_amount = sum(
            (order.crypto_amount for order in sell_orders if order.status == OrderStatus.COMPLETED),
            Decimal('0.0'),
        )
        total_bought_amount = sum(
            (order.crypto_amount for order in buy_orders if order.status == OrderStatus.COMPLETED),
            Decimal('0.0'),
        )

        sell_order_count = len([order for order in sell_orders if order.status == OrderStatus.COMPLETED])
        buy_order_count = len([order for order in buy_orders if order.status == OrderStatus.COMPLETED])

        return ExchangeStat(
            total_sold_amount=total_sold_amount,
            total_bought_amount=total_bought_amount,
            sell_order_count=sell_order_count,
            buy_order_count=buy_order_count,
        )


class MailingInteractor:
    def __init__(
        self,
        user_reader: interfaces.UserReader,
        broadcaster: interfaces.Broadcaster,
    ):
        self._user_reader = user_reader
        self._broadcaster = broadcaster

    async def __call__(
        self,
        keyboard: interfaces.Keyboard,
        content_type: str,
        text: str | None = None,
        caption: str | None = None,
        file_id: str | None = None,
    ) -> MailingStat:
        users = await self._user_reader.get_all()
        users_id = [user.id for user in users]

        if content_type == 'text':
            count = await self._broadcaster.broadcast(
                users=users_id,
                text=text,
                keyboard=keyboard,
            )

        elif content_type == 'photo':
            count = await self._broadcaster.broadcast(
                users=users_id,
                photo_id=file_id,
                caption=caption,
                keyboard=keyboard,
            )

        elif content_type == 'video':
            count = await self._broadcaster.broadcast(
                users=users_id,
                video_id=file_id,
                caption=caption,
                keyboard=keyboard,
            )

        elif content_type == 'animation':
            count = await self._broadcaster.broadcast(
                users=users_id,
                gif_id=file_id,
                caption=caption,
                keyboard=keyboard,
            )
        else:
            count = 0

        un_success = len(users_id) - count

        return MailingStat(
            success=count,
            un_success=un_success,
        )


class SearchUserByIdInteractor:
    def __init__(
        self,
        user_reader: interfaces.UserReader,
        sell_order_reader: interfaces.SellOrderReader,
        buy_order_reader: interfaces.BuyOrderReader,
    ):
        self._user_reader = user_reader
        self._sell_order_reader = sell_order_reader
        self._buy_order_reader = buy_order_reader

    async def __call__(self, user_id: str) -> UserProfile:
        if not user_id.isdigit():
            raise exceptions.IncorrectUserIdError

        user_id = int(user_id)

        user = await self._user_reader.get_by_id(user_id=user_id)
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

        return UserProfile(
            user=BasicUser(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                created_at=user.created_at,
                is_banned=user.is_banned,
            ),
            statistic=ExchangeStat(
                total_sold_amount=total_sold_amount,
                total_bought_amount=total_bought_amount,
                sell_order_count=sell_order_count,
                buy_order_count=buy_order_count,
            ),
        )


class SearchUserByUsernameInteractor:
    def __init__(
        self,
        user_reader: interfaces.UserReader,
        sell_order_reader: interfaces.SellOrderReader,
        buy_order_reader: interfaces.BuyOrderReader,
    ):
        self._user_reader = user_reader
        self._sell_order_reader = sell_order_reader
        self._buy_order_reader = buy_order_reader

    async def __call__(self, username: str) -> UserProfile:
        if '@' in username:
            username = username.replace('@', '')

        user = await self._user_reader.get_by_username(username=username)
        sell_orders = await self._sell_order_reader.get_all_by_user_id(user_id=user.id)
        buy_orders = await self._buy_order_reader.get_all_by_user_id(user_id=user.id)

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

        return UserProfile(
            user=BasicUser(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                created_at=user.created_at,
                is_banned=user.is_banned,
            ),
            statistic=ExchangeStat(
                total_sold_amount=total_sold_amount,
                total_bought_amount=total_bought_amount,
                sell_order_count=sell_order_count,
                buy_order_count=buy_order_count,
            ),
        )


class UserBanInteractor:
    def __init__(
        self,
        user_update_manager: UserUpdateManager,
        sell_order_reader: interfaces.SellOrderReader,
        buy_order_reader: interfaces.BuyOrderReader,
    ):
        self._user_update_manager = user_update_manager
        self._sell_order_reader = sell_order_reader
        self._buy_order_reader = buy_order_reader

    async def __call__(self, user_id: str, ban_status: bool) -> UserProfile:
        if not user_id.isdigit():
            raise exceptions.IncorrectUserIdError

        user_id = int(user_id)

        user = await self._user_update_manager.get_by_id(user_id=user_id)
        user.is_banned = ban_status
        await self._user_update_manager.update(user=user)

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

        return UserProfile(
            user=BasicUser(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                created_at=user.created_at,
                is_banned=user.is_banned,
            ),
            statistic=ExchangeStat(
                total_sold_amount=total_sold_amount,
                total_bought_amount=total_bought_amount,
                sell_order_count=sell_order_count,
                buy_order_count=buy_order_count,
            ),
        )


class GetFullSellOrderInteractor:
    def __init__(
        self,
        order_reader: interfaces.SellOrderReader,
    ):
        self._order_reader = order_reader

    async def __call__(self, order_id: UUID) -> FullSellOrder:
        order = await self._order_reader.get_full_info(order_id=order_id)
        return order


class GetFullBuyOrderInteractor:
    def __init__(
        self,
        order_reader: interfaces.BuyOrderReader,
    ):
        self._order_reader = order_reader

    async def __call__(self, order_id: UUID) -> FullBuyOrder:
        order = await self._order_reader.get_full_info(order_id=order_id)
        return order


class RejectBuyOrderInteractor:
    def __init__(
        self,
        order_update_manager: BuyOrderUpdateManager,
        broadcaster: interfaces.Broadcaster,
    ):
        self._order_update_manager = order_update_manager
        self._broadcaster = broadcaster

    async def __call__(self, order_id: UUID, note: str) -> FullBuyOrder:
        order = await self._order_update_manager.get_full_info(order_id=order_id)
        order.order.note = note
        order.order.status = OrderStatus.CANCELED

        await self._order_update_manager.update(order=order.order)

        await self._broadcaster.send_message(
            user_id=order.order.user_id,
            text=reject_buy_order_notification_text(order_id=order_id, note=note),
        )

        return order


class RejectSellOrderInteractor:
    def __init__(
        self,
        order_update_manager: SellOrderUpdateManager,
        broadcaster: interfaces.Broadcaster,
    ):
        self._order_update_manager = order_update_manager
        self._broadcaster = broadcaster

    async def __call__(self, order_id: UUID, note: str) -> FullSellOrder:
        order = await self._order_update_manager.get_full_info(order_id=order_id)
        order.order.note = note
        order.order.status = OrderStatus.CANCELED

        await self._order_update_manager.update(order=order.order)

        await self._broadcaster.send_message(
            user_id=order.order.user_id,
            text=reject_sell_order_notification_text(order_id=order.order.id, note=note),
        )

        return order


class ConfirmBuyOrderInteractor:
    def __init__(
        self,
        updater_manager: BuyOrderUpdateManager,
        wallet_reader: interfaces.WalletReader,
        trc_client: interfaces.TrcClient,
        broadcaster: interfaces.Broadcaster,
    ):
        self._updater_manager = updater_manager
        self._wallet_reader = wallet_reader
        self._trc_client = trc_client
        self._broadcaster = broadcaster

    async def __call__(self, order_id: UUID, user_id: int) -> FullBuyOrder:
        order = await self._updater_manager.get_full_info(order_id=order_id)
        if order.card.user_id != user_id:
            raise domain_exceptions.UserPermissionError

        if order.order.status != OrderStatus.PAID:
            raise exceptions.InvalidOrderStatusForConfirmationError

        wallet = await self._wallet_reader.get_current()
        tx = await self._trc_client.transfer_usdt(
            private_key_hex=wallet.private_key_hex,
            to_address=order.order.user_requisites.address,
            amount=int(order.order.crypto_amount),
        )

        order.order.status = OrderStatus.COMPLETED
        order.order.completed_at = datetime.now()
        await self._updater_manager.update(order=order.order)

        await self._broadcaster.send_message(
            user_id=order.order.user_id,
            text=confirm_buy_order_notification_text(
                order_id=order_id,
                tx_id=tx.tx_id,
            ),
        )

        return order


class ConfirmSellOrderInteractor:
    def __init__(
        self,
        updater_manager: SellOrderUpdateManager,
        broadcaster: interfaces.Broadcaster,
    ):
        self._updater_manager = updater_manager
        self._broadcaster = broadcaster

    async def __call__(self, order_id: UUID) -> FullSellOrder:
        order = await self._updater_manager.get_full_info(order_id=order_id)

        if order.order.status != OrderStatus.PAID:
            raise exceptions.InvalidOrderStatusForConfirmationError

        order.order.status = OrderStatus.COMPLETED
        order.order.completed_at = datetime.now()
        await self._updater_manager.update(order=order.order)

        await self._broadcaster.send_message(
            user_id=order.order.user_id,
            text=confirm_sell_order_notification_text(order_id=order_id),
        )

        return order


class BanUserBySellOrderInteractor:
    def __init__(
        self,
        order_reader: interfaces.SellOrderReader,
        user_update_manager: UserUpdateManager,
    ):
        self._order_reader = order_reader
        self._user_update_manager = user_update_manager

    async def __call__(self, order_id: UUID, ban_status: bool) -> FullSellOrder:
        full_order = await self._order_reader.get_full_info(order_id=order_id)
        full_order.user.is_banned = ban_status
        await self._user_update_manager.update(user=full_order.user)

        return full_order


class BanUserByBuyOrderInteractor:
    def __init__(
        self,
        order_reader: interfaces.BuyOrderReader,
        user_update_manager: UserUpdateManager,
    ):
        self._order_reader = order_reader
        self._user_update_manager = user_update_manager

    async def __call__(self, order_id: UUID, ban_status: bool) -> FullBuyOrder:
        full_order = await self._order_reader.get_full_info(order_id=order_id)
        full_order.user.is_banned = ban_status
        await self._user_update_manager.update(user=full_order.user)

        return full_order
