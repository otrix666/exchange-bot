from decimal import Decimal
from typing import Protocol

from backend.application import interfaces
from backend.domain.entities.settings import Settings


class GetSettingsInteractor:
    def __init__(
        self,
        reader: interfaces.SettingsReader,
    ):
        self._reader = reader

    def __call__(self) -> Settings:
        return self._reader.read()


class SettingsUpdateManager(interfaces.SettingsReader, interfaces.SettingsWriter, Protocol): ...


class UpdateUsdtRequisitesInteractor:
    def __init__(
        self,
        updater: SettingsUpdateManager,
        access_manager: interfaces.AccessManager,
    ):
        self._updater = updater
        self._access_manager = access_manager

    def __call__(self, usdt_requisites: str) -> Settings:
        settings = self._updater.read()
        settings.usdt_requisites = usdt_requisites
        self._updater.write(settings)

        return settings


class UpdateSellUsdtRateInteractor:
    def __init__(
        self,
        updater: SettingsUpdateManager,
        access_manager: interfaces.AccessManager,
    ):
        self._updater = updater
        self._access_manager = access_manager

    def __call__(self, sell_usdt_rate: str) -> Settings:
        settings = self._updater.read()
        settings.sell_usdt_rate = Decimal(sell_usdt_rate)
        self._updater.write(settings)

        return settings


class UpdateBuyUsdtRateInteractor:
    def __init__(
        self,
        updater: SettingsUpdateManager,
        access_manager: interfaces.AccessManager,
    ):
        self._updater = updater
        self._access_manager = access_manager

    def __call__(self, buy_usdt_rate: str) -> Settings:
        settings = self._updater.read()
        settings.buy_usdt_rate = Decimal(buy_usdt_rate)
        self._updater.write(settings)

        return settings


class UpdateTgChatIdInteractor:
    def __init__(
        self,
        updater: SettingsUpdateManager,
        access_manager: interfaces.AccessManager,
    ):
        self._updater = updater
        self._access_manager = access_manager

    def __call__(self, tg_chat_id: str) -> Settings:
        settings = self._updater.read()
        settings.tg_chat_id = tg_chat_id
        self._updater.write(settings)

        return settings
