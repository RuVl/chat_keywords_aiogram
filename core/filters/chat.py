import asyncio
from typing import Union, Any, Dict

from aiogram import types
from aiogram.filters import BaseFilter

from core.database.methods import get_tg_chat
from core.misc import parse_text


# Message filter by keywords from database
class KeywordsMessageFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> Union[bool, Dict[str, Any]]:
        chat = await get_tg_chat(msg.chat.id)

        if chat is None:
            await msg.answer('Я забыл своего создателя...\nМне придется покинуть этот чат :(')
            await asyncio.sleep(1)

            await msg.chat.leave()
            return False

        keywords = set(chat.keywords.split(';'))
        words = parse_text(msg.text)

        print(words)

        return {'chat': chat} if keywords.intersection(words) else False
