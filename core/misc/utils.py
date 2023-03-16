import re
import string
from typing import Union

from aiogram import types
from aiogram.fsm.context import FSMContext

from core.database.models import Chat


chars = f'[{re.escape(string.punctuation)}]'


def parse_text(text: str) -> set[str]:
    words = re.sub(chars, '', text.lower()).split()
    return set(map(str.strip, words))


def parse_keywords(parse_string: str) -> set[str]:
    keywords = parse_string.strip().lower().split(';')
    return set(map(str.strip, keywords))


async def get_chat_from_state(msg: types.Message, state: FSMContext) -> Union[Chat, None]:
    data = await state.get_data()
    chat = data.get('chat')

    if chat is None:
        await msg.answer('Ошибка: чат не выбран!\nПопробуйте ещё раз.')
        await state.clear()
        return None

    return chat
