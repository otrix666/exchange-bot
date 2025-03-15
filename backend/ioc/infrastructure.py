from collections.abc import AsyncIterable, Iterable
from concurrent.futures.thread import ThreadPoolExecutor

from aiogram import Bot
from dishka import AnyOf, Provider, Scope, provide
from psycopg_pool import AsyncConnectionPool
from tronpy import AsyncTron
from tronpy.defaults import CONF_NILE
from tronpy.providers import AsyncHTTPProvider

from backend.application import interfaces
from backend.application.use_cases.buy_order import BuyOrderUpdateManager
from backend.application.use_cases.card import DeleteCardManager
from backend.application.use_cases.contact import DeleteContactManager
from backend.application.use_cases.sell_order import SellOrderUpdateManager
from backend.application.use_cases.settings import SettingsUpdateManager
from backend.application.use_cases.user import UserUpdateManager
from backend.application.use_cases.wallet import SaveWalletManager
from backend.config import Config
from backend.infrastructure.mapper.buy_order import BuyOrderMapper, FullBuyOrderMapper
from backend.infrastructure.mapper.card import CardMapper
from backend.infrastructure.mapper.sell_order import FullSellOrderMapper, SellOrderMapper
from backend.infrastructure.repositories.buy_order import BuyOrderRepository
from backend.infrastructure.repositories.card import CardRepository
from backend.infrastructure.repositories.contact import ContactRepository
from backend.infrastructure.repositories.sell_order import SellOrderRepository
from backend.infrastructure.repositories.settings import SettingsRepository
from backend.infrastructure.repositories.user import UserRepository
from backend.infrastructure.repositories.wallet import WalletRepository
from backend.infrastructure.services.keybords.admin import AdminKeyboardBuilder
from backend.infrastructure.services.keybords.user import UserKeyboardBuilder
from backend.infrastructure.services.tg.broadcaster import Broadcaster
from backend.infrastructure.services.trc.trc_client import PrivateKeyCreator, TrcClient


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_thread_pool(self) -> Iterable[ThreadPoolExecutor]:
        thread_pool = ThreadPoolExecutor(max_workers=8)
        yield thread_pool
        thread_pool.shutdown()

    @provide(scope=Scope.APP)
    async def get_connection_pool(self, config: Config) -> AsyncIterable[AsyncConnectionPool]:
        pool = AsyncConnectionPool(
            conninfo=config.pg.create_connection_string(),
            min_size=40,
            max_size=80,
            open=False,
        )
        await pool.open()
        try:
            yield pool
        finally:
            await pool.close()

    @provide(scope=Scope.REQUEST, provides=interfaces.TrcClient)
    async def get_tron_client(self, config: Config) -> TrcClient:
        provider = AsyncHTTPProvider(endpoint_uri=CONF_NILE, api_key=config.trc.api_key)
        client = AsyncTron(provider=provider)

        return TrcClient(client=client, contract_address=config.trc.testnet_contract_address)

    @provide(scope=Scope.REQUEST, provides=interfaces.Broadcaster)
    def get_broadcaster(self, bot: Bot) -> Broadcaster:
        return Broadcaster(bot)

    admin_kb_builder = provide(
        AdminKeyboardBuilder,
        scope=Scope.REQUEST,
        provides=interfaces.AdminKeyboardBuilder,
    )

    user_kb_builder = provide(
        UserKeyboardBuilder,
        scope=Scope.REQUEST,
        provides=interfaces.UserKeyboardBuilder,
    )

    user_repo = provide(
        UserRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.UserReader, interfaces.UserSaver, UserUpdateManager],
    )

    settings_repo = provide(
        SettingsRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.SettingsReader, SettingsUpdateManager],
    )

    buy_order_full_mapper = provide(FullBuyOrderMapper, scope=Scope.REQUEST)
    buy_order_mapper = provide(BuyOrderMapper, scope=Scope.REQUEST)
    buy_order_repo = provide(
        BuyOrderRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.BuyOrderReader, interfaces.BuyOrderSaver, BuyOrderUpdateManager],
    )

    sell_order_full_mapper = provide(FullSellOrderMapper, scope=Scope.REQUEST)
    sell_order_mapper = provide(SellOrderMapper, scope=Scope.REQUEST)
    sell_order_repo = provide(
        SellOrderRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.SellOrderReader, interfaces.SellOrderSaver, SellOrderUpdateManager],
    )

    contact_repo = provide(
        ContactRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.ContactReader, interfaces.ContactSaver, DeleteContactManager],
    )

    wallet_repo = provide(
        WalletRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.WalletReader, SaveWalletManager],
    )

    card_mapper = provide(
        CardMapper,
        scope=Scope.REQUEST,
    )
    card_repo = provide(
        CardRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.CardReader, interfaces.CardSaver, DeleteCardManager],
    )

    private_key_creator = provide(
        PrivateKeyCreator,
        scope=Scope.REQUEST,
        provides=interfaces.PrivateKeyCreator,
    )
