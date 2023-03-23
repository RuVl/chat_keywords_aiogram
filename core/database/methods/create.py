from aiogram import types

from core.database import session_maker
from core.database.models import SamDB
from core.misc import tg_user_adapter, tg_chat_adapter


async def create_user(tg_user: types.User):
    async with session_maker.begin() as session:
        user = tg_user_adapter(tg_user)
        session.add(user)


async def create_chat(tg_chat: types.Chat, tg_user: types.User):
    async with session_maker.begin() as session:
        chat = tg_chat_adapter(tg_chat, tg_user)
        session.add(chat)


async def create_sam_dbs(rows: set[SamDB]):
    async with session_maker.begin() as session:
        session.add_all(rows)
