from aiogram import types

from core.database import models


def tg_chat_adapter(tg_chat: types.Chat, tg_owner: types.User) -> models.Chat:
    chat = models.Chat()
    chat.chat_id = tg_chat.id
    chat.chat_title = tg_chat.title
    chat.owner_id = tg_owner.id

    return chat


def tg_user_adapter(tg_user: types.User) -> models.User:
    user = models.User()
    user.user_id = tg_user.id

    return user
