import asyncio
import logging
import re
from typing import Union, Any, Dict

from aiogram import types
from aiogram.filters import BaseFilter

from core.database.methods import get_tg_chat
from core.parsers import parse_text


async def check_chat(chat, msg: types.Message) -> bool:
    if chat is None:
        await msg.answer('Я забыл своего создателя...\nМне придется покинуть этот чат :(')
        await asyncio.sleep(1)

        await msg.chat.leave()
        return False
    return True


# Message filter by keywords from database
class KeywordsMessageFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> Union[bool, Dict[str, Any]]:
        chat = await get_tg_chat(msg.chat.id)

        if not await check_chat(chat, msg):
            return False

        keywords = set(chat.keywords.split(';'))
        words = parse_text(msg.text)

        return {'chat': chat} if keywords.intersection(words) else False


# Message filter by conditions from db
class ConditionsMessageFilter(BaseFilter):
    flags = re.IGNORECASE | re.DOTALL | re.UNICODE

    async def __call__(self, msg: types.Message) -> bool | dict[str, Any]:
        chat = await get_tg_chat(msg.chat.id)

        if not await check_chat(chat, msg):
            return False

        expr = chat.parsed_conditions
        if chat.parsed_conditions is None:
            return False

        try:
            res = re.search(expr, msg.text, flags=self.flags)
        except re.error as e:
            logging.error(f'Regex error: {e.msg}!')

        return {'chat': chat} if res is not None else False
