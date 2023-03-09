from sqlalchemy import select

from core.database import session_maker
from core.database.models import User, Chat


async def get_tg_user(user_id: int) -> User:
    async with session_maker() as session:
        query = select(User).where(User.user_id == user_id)

        return await session.scalar(query)


async def get_tg_chat(chat_id: int) -> Chat:
    async with session_maker() as session:
        query = select(Chat).where(Chat.chat_id == chat_id)

        return await session.scalar(query)
