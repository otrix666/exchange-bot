import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from backend import ioc
from backend.config import Config
from backend.presentation.bot.handlers import router_list
from backend.presentation.bot.middlewares.sync_user import SyncUserMiddleware

config = Config()


async def on_startup(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f'{config.webhook.url}{config.webhook.path}', allowed_updates=['message', 'callback_query'])


def setup_logging():
    logging.basicConfig(
        level=logging.ERROR,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting bot')


def create_bot(token: str) -> Bot:
    return Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
    )


def create_dispatcher(routers: list[Router], container: AsyncContainer) -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers)
    dp.startup.register(on_startup)

    middleware = SyncUserMiddleware(container=container)
    dp.message.outer_middleware(middleware)
    dp.callback_query.outer_middleware(middleware)

    return dp


def create_app(dp: Dispatcher, bot: Bot) -> web.Application:
    app = web.Application()

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(
        app,
        path=config.webhook.path,
    )
    setup_application(app, dp, bot=bot)
    return app


def main(bot: Bot, container: AsyncContainer, routers: list[Router]):
    setup_logging()

    dp = create_dispatcher(routers, container)
    setup_dishka(container=container, router=dp, auto_inject=True)
    app = create_app(dp, bot)

    web.run_app(app, host=config.webhook.host, port=config.webhook.port)


if __name__ == '__main__':
    bot = create_bot(token=config.bot.token)
    container = make_async_container(
        ioc.ApplicationProvider(),
        ioc.InfrastructureProvider(),
        AiogramProvider(),
        context={Config: config, Bot: bot},
    )
    main(bot=bot, container=container, routers=router_list)
