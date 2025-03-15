from backend.presentation.bot.handlers.admin.callback import router as admin_callback_router
from backend.presentation.bot.handlers.admin.message import router as admin_message_router
from backend.presentation.bot.handlers.common.message import router as common_massage_router
from backend.presentation.bot.handlers.user.callback import router as user_callback_router
from backend.presentation.bot.handlers.user.message import router as user_message_router

router_list = [
    admin_message_router,
    admin_callback_router,
    common_massage_router,
    user_callback_router,
    user_message_router,
]

__all__ = [
    'router_list',
]
