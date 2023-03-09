import json
from typing import Union, Any, Dict

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class CallbackDictKeysFilter(BaseFilter):
    __slots__ = (
        "keys",
    )

    def __init__(self, *keys):
        self.keys: frozenset = frozenset(keys)

    async def __call__(self, callback: CallbackQuery) -> Union[bool, Dict[str, Any]]:
        data = json.loads(callback.data)

        # Не распарсили в словарь
        if not isinstance(data, dict):
            return False

        # Все ключи есть в данном словаре
        if self.keys.issubset(data.keys()):
            return {'data': data}
