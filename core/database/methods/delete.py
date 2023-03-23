from aiogram import types
from sqlalchemy import delete

from core.database import session_maker
from core.database.models import Chat, SamDB


async def delete_chat(tg_chat: types.Chat):
    async with session_maker.begin() as session:
        query = delete(Chat).where(Chat.chat_id == tg_chat.id)
        await session.execute(query)


async def delete_sam_db(numbers: set[int]):
    async with session_maker.begin() as session:
        query = delete(SamDB).where(SamDB.number.in_(numbers))
        await session.execute(query)
