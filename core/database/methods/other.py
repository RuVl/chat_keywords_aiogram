from aiogram import types
from sqlalchemy import select

from core.database import session_maker
from core.database.models import User
from core.misc import tg_user_adapter


async def get_or_create_tg_user(tg_user: types.User) -> User:
    async with session_maker() as session:
        query = select(User).where(User.user_id == tg_user.id)
        user = await session.scalar(query)

        if user is None:
            session.add(tg_user_adapter(tg_user))
            await session.commit()

        return await session.scalar(query)
