from typing import Union

from aiogram import types
from aiogram.fsm.context import FSMContext

from core.database.models import Chat


async def get_chat_from_state(msg: types.Message, state: FSMContext) -> Union[Chat, None]:
    data = await state.get_data()
    chat = data.get('chat')

    if chat is None:
        await msg.answer('Ошибка: чат не выбран!\nПопробуйте ещё раз.')
        await state.clear()
        return None

    return chat
