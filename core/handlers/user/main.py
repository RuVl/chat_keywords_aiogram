import logging

from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from core.database.methods import get_or_create_tg_user
from core.handlers.user.settings import settings_router

user_router = Router()

user_router.message.filter(
    F.chat.type == 'private',
)

user_router.include_router(settings_router)


@user_router.message(CommandStart())
async def start(msg: types.Message):
    logging.info(f'Command /start from user: {msg.from_user.id}')

    user = await get_or_create_tg_user(msg.from_user)
    await msg.answer(
        'Введите "/chats" для получения информации по чатам.'
        if user.chats else
        'Добавьте меня в чаты для начала контроля.'
    )
