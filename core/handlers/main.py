from aiogram import Dispatcher

from .chat import chat_router
from .user import user_router


def register_all_handlers(dp: Dispatcher) -> None:
    dp.include_routers(user_router, chat_router)
