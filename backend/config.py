from dataclasses import dataclass, field
from os import environ as env


@dataclass
class PgConfig:
    db: str = field(default_factory=lambda: env.get('POSTGRES_DB').strip())
    host: str = field(default_factory=lambda: env.get('POSTGRES_HOST').strip())
    port: int = field(default_factory=lambda: int(env.get('POSTGRES_PORT').strip()))
    user: str = field(default_factory=lambda: env.get('POSTGRES_USER').strip())
    password: str = field(default_factory=lambda: env.get('POSTGRES_PASSWORD').strip())

    def create_connection_string(self) -> str:
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


@dataclass
class TgBotConfig:
    token: str = field(default_factory=lambda: env.get('TG_BOT_TOKEN').strip())
    admins: list[int] = field(default_factory=lambda: list(map(int, env.get('ADMINS').strip().split(','))))
    operators: list[int] = field(default_factory=lambda: list(map(int, env.get('OPERATORS').strip().split(','))))


@dataclass
class WebHookConfig:
    host: str = field(default_factory=lambda: env.get('WEBHOOK_HOST').strip())
    port: int = field(default_factory=lambda: int(env.get('WEBHOOK_PORT').strip()))
    url: str = field(default_factory=lambda: env.get('WEBHOOK_URL').strip())
    path: str = field(default_factory=lambda: env.get('WEBHOOK_PATH').strip())


@dataclass
class SettingsConfig:
    file_path: str = field(default_factory=lambda: env.get('SETTINGS_PATH').strip())


@dataclass
class BannerConfig:
    file_path: str = field(default_factory=lambda: env.get('BANNER_PATH').strip())


@dataclass
class TrcConfig:
    api_key: str = field(default_factory=lambda: env.get('TRONGRID_API_KEY').strip())
    testnet_contract_address: str = field(default_factory=lambda: env.get('TESTNET_CONTRACT_ADDRESS').strip())
    mainnet_contract_address: str = field(default_factory=lambda: env.get('MAINNET_CONTRACT_ADDRESS').strip())


@dataclass
class Config:
    pg: PgConfig = field(default_factory=PgConfig)
    bot: TgBotConfig = field(default_factory=TgBotConfig)
    webhook: WebHookConfig = field(default_factory=WebHookConfig)
    settings: SettingsConfig = field(default_factory=SettingsConfig)
    banner: BannerConfig = field(default_factory=BannerConfig)
    trc: TrcConfig = field(default_factory=TrcConfig)
