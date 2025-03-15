from uuid import uuid4

from aiogram import Bot
from dishka import Provider, Scope, from_context, provide

from backend.application import interfaces
from backend.application.services.access_manager import AccessManager
from backend.application.services.csv_creator import CsvCreator
from backend.application.use_cases.admin import (
    BanUserByBuyOrderInteractor,
    BanUserBySellOrderInteractor,
    ConfirmBuyOrderInteractor,
    ConfirmSellOrderInteractor,
    GetExchangeStatInteractor,
    GetFullBuyOrderInteractor,
    GetFullSellOrderInteractor,
    MailingInteractor,
    RejectBuyOrderInteractor,
    RejectSellOrderInteractor,
    SearchUserByIdInteractor,
    SearchUserByUsernameInteractor,
    UserBanInteractor,
)
from backend.application.use_cases.buy_order import (
    CalculateBuyOrderAmountInteractor,
    CreateBuyOrderInteractor,
    GetBuyOrderInteractor,
)
from backend.application.use_cases.card import (
    DeleteCardInteractor,
    GetCardInteractor,
    GetCardsInteractor,
    SaveCardInteractor,
)
from backend.application.use_cases.contact import DeleteContactInteractor, GetContactsInteractor, SaveContactInteractor
from backend.application.use_cases.sell_order import (
    CalculateSellOrderAmountInteractor,
    CreateSellOrderInteractor,
    GetSellOrderInteractor,
)
from backend.application.use_cases.settings import (
    GetSettingsInteractor,
    UpdateBuyUsdtRateInteractor,
    UpdateSellUsdtRateInteractor,
    UpdateTgChatIdInteractor,
    UpdateUsdtRequisitesInteractor,
)
from backend.application.use_cases.user import (
    GetUserExchangeHistoryReportInteractor,
    GetUserExchangeStatInteractor,
    OperatorAccessInteractor,
    PanelAccessInteractor,
    SyncTelegramUserInteractor,
)
from backend.application.use_cases.wallet import (
    CreateTrxWithdrawInteractor,
    CreateUsdtWithdrawInteractor,
    CreateWalletInteractor,
    GetAccountBalanceInteractor,
    GetWalletInteractor,
)
from backend.config import Config


class ApplicationProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    bot = from_context(provides=Bot, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4

    access_manager = provide(
        AccessManager,
        scope=Scope.REQUEST,
        provides=interfaces.AccessManager,
    )

    csv_creator = provide(
        CsvCreator,
        scope=Scope.REQUEST,
        provides=interfaces.CsvCreator,
    )

    calculate_buy_order_amount_interactor = provide(CalculateBuyOrderAmountInteractor, scope=Scope.REQUEST)
    create_buy_order_interactor = provide(CreateBuyOrderInteractor, scope=Scope.REQUEST)
    get_buy_order_interactor = provide(GetBuyOrderInteractor, scope=Scope.REQUEST)

    calculate_sell_order_amount_interactor = provide(CalculateSellOrderAmountInteractor, scope=Scope.REQUEST)
    create_sell_order_interactor = provide(CreateSellOrderInteractor, scope=Scope.REQUEST)
    get_sell_order_interactor = provide(GetSellOrderInteractor, scope=Scope.REQUEST)

    get_settings_interactor = provide(GetSettingsInteractor, scope=Scope.REQUEST)
    update_usdt_requisites_interactor = provide(UpdateUsdtRequisitesInteractor, scope=Scope.REQUEST)
    update_sell_usdt_rate_interactor = provide(UpdateSellUsdtRateInteractor, scope=Scope.REQUEST)
    update_buy_usdt_rate_interactor = provide(UpdateBuyUsdtRateInteractor, scope=Scope.REQUEST)
    update_tg_chat_id_interactor = provide(UpdateTgChatIdInteractor, scope=Scope.REQUEST)

    sync_tg_user_interactor = provide(SyncTelegramUserInteractor, scope=Scope.REQUEST)
    panel_access_interactor = provide(PanelAccessInteractor, scope=Scope.REQUEST)
    operator_access_interactor = provide(OperatorAccessInteractor, scope=Scope.REQUEST)
    get_user_exchange_stat_interactor = provide(GetUserExchangeStatInteractor, scope=Scope.REQUEST)
    get_user_exchange_history_interactor = provide(GetUserExchangeHistoryReportInteractor, scope=Scope.REQUEST)

    get_exchange_stat_interactor = provide(GetExchangeStatInteractor, scope=Scope.REQUEST)
    mailing_interactor = provide(MailingInteractor, scope=Scope.REQUEST)
    search_user_by_id_interactor = provide(SearchUserByIdInteractor, scope=Scope.REQUEST)
    search_user_by_username_interactor = provide(SearchUserByUsernameInteractor, scope=Scope.REQUEST)
    get_full_buy_order_interactor = provide(GetFullBuyOrderInteractor, scope=Scope.REQUEST)
    get_full_sell_order_interactor = provide(GetFullSellOrderInteractor, scope=Scope.REQUEST)
    user_ban_interactor = provide(UserBanInteractor, scope=Scope.REQUEST)
    ban_user_by_sell_order = provide(BanUserBySellOrderInteractor, scope=Scope.REQUEST)
    ban_user_by_buy_order = provide(BanUserByBuyOrderInteractor, scope=Scope.REQUEST)
    reject_sell_order_interactor = provide(RejectSellOrderInteractor, scope=Scope.REQUEST)
    reject_buy_order_interactor = provide(RejectBuyOrderInteractor, scope=Scope.REQUEST)
    confirm_buy_order_interactor = provide(ConfirmBuyOrderInteractor, scope=Scope.REQUEST)
    confirm_sell_order_interactor = provide(ConfirmSellOrderInteractor, scope=Scope.REQUEST)

    get_contacts_interactor = provide(GetContactsInteractor, scope=Scope.REQUEST)
    save_contact_interactor = provide(SaveContactInteractor, scope=Scope.REQUEST)
    delete_contact_interactor = provide(DeleteContactInteractor, scope=Scope.REQUEST)

    create_wallet_interactor = provide(CreateWalletInteractor, scope=Scope.REQUEST)
    get_account_balance_interactor = provide(GetAccountBalanceInteractor, scope=Scope.REQUEST)
    get_wallet_interactor = provide(GetWalletInteractor, scope=Scope.REQUEST)
    create_trx_withdraw_interactor = provide(CreateTrxWithdrawInteractor, scope=Scope.REQUEST)
    create_usdt_withdraw_interactor = provide(CreateUsdtWithdrawInteractor, scope=Scope.REQUEST)

    get_cards_interactor = provide(GetCardsInteractor, scope=Scope.REQUEST)
    get_card_interactor = provide(GetCardInteractor, scope=Scope.REQUEST)
    save_card_interactor = provide(SaveCardInteractor, scope=Scope.REQUEST)
    delete_card_interactor = provide(DeleteCardInteractor, scope=Scope.REQUEST)
