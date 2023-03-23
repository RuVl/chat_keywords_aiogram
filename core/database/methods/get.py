from typing import Union

from sqlalchemy import select

from core.database import session_maker
from core.database.models import User, Chat, SamDB


async def get_tg_user(user_id: int) -> User:
    async with session_maker() as session:
        query = select(User).where(User.user_id == user_id)
        return await session.scalar(query)


async def get_tg_chat(chat_id: int) -> Chat:
    async with session_maker() as session:
        query = select(Chat).where(Chat.chat_id == chat_id)
        return await session.scalar(query)


async def get_sam_db(limit=100) -> list[SamDB]:
    async with session_maker() as session:
        query = select(SamDB).limit(limit)
        result = await session.scalars(query)
        return result.all()


async def get_by_numbers(numbers: Union[set[int], int]) -> Union[SamDB, list[SamDB]]:
    async with session_maker() as session:
        if isinstance(numbers, int):
            query = select(SamDB).where(SamDB.number == numbers)
            return await session.scalar(query)

        query = select(SamDB).where(SamDB.number.in_(numbers))
        result = await session.scalars(query)
        return result.all()
