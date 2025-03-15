import json
from dataclasses import asdict
from decimal import Decimal

from backend.application import interfaces
from backend.config import Config
from backend.domain import exceptions
from backend.domain.entities.settings import Settings


class SettingsRepository(
    interfaces.SettingsReader,
    interfaces.SettingsWriter,
):
    def __init__(self, config: Config):
        self._file_path = config.settings.file_path

    def read(self) -> Settings:
        try:
            with open(self._file_path, encoding='utf-8') as file:
                data = json.load(file)
                return Settings(
                    usdt_requisites=data['usdt_requisites'],
                    sell_usdt_rate=Decimal(data['sell_usdt_rate']),
                    buy_usdt_rate=Decimal(data['buy_usdt_rate']),
                    tg_chat_id=data['tg_chat_id'],
                )
        except (FileNotFoundError, json.JSONDecodeError):
            raise exceptions.SettingsReadError

    def write(self, settings: Settings) -> None:
        with open(self._file_path, 'w', encoding='utf-8') as file:
            json.dump(asdict(settings), file, indent=4, ensure_ascii=False, default=str)
