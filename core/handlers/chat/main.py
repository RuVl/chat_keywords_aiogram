import asyncio
import logging

from aiogram import Router, types, F
from aiogram.enums import ContentType
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION

from core import bot
from core.database.methods import get_tg_user, create_chat, delete_chat
from core.database.models import Chat
from core.filters import KeywordsMessageFilter

chat_router = Router()

chat_router.message.filter(
    F.chat.type.in_({'group', 'supergroup'})
)

chat_router.my_chat_member.filter(
    F.chat.type.in_({'group', 'supergroup'})
)


@chat_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION)
)
async def me_invited(upd: types.ChatMemberUpdated):
    logging.info(f'Trying to add bot in chat {upd.chat.id}')

    user = await get_tg_user(upd.from_user.id)
    if not user:
        logging.info(f'No user in database with id {upd.from_user.id}')

        await bot.send_message(upd.chat.id, 'Вы не использовали ботом, вызовите /start в ЛС\nЯ ухожу...')
        await asyncio.sleep(3)

        await upd.chat.leave()
        return

    await create_chat(upd.chat, upd.from_user)
    await bot.send_message(upd.from_user.id, f'Меня добавили в чат: {upd.chat.title}.\nВведите /chats для просмотра активных чатов.')


@chat_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION)
)
async def me_kicked(upd: types.ChatMemberUpdated):
    logging.info(f'Kicked bot from chat {upd.chat.id}')

    await delete_chat(upd.chat)
    await bot.send_message(upd.from_user.id, f'Меня больше нет в этом чате: {upd.chat.title}')


@chat_router.message(
    F.content_type == ContentType.TEXT,
    KeywordsMessageFilter()
)
async def new_message(msg: types.Message, chat: Chat):
    if msg.chat.username:
        await bot.send_message(chat.owner_id, f'https://t.me/{msg.chat.username}/{msg.message_id}', disable_notification=True)
    else:
        forward_msg = await bot.forward_message(chat.owner_id, msg.chat.id, msg.message_id, disable_notification=True)
        await forward_msg.answer(chat.owner_id, f'https://t.me/c/{msg.chat.shifted_id}/{msg.message_id}', disable_notification=True)
