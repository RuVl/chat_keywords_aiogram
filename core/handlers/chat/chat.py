from aiogram import Router, types, F
from aiogram.enums import ContentType
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION

from core import bot
from core.database.methods import get_tg_user, create_chat, delete_chat, get_tg_chat

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
    user = await get_tg_user(upd.from_user.id)
    if not user:
        await bot.send_message(upd.chat.id, 'Вы не пользуетесь ботом, вызовите /start в в ЛС\nЯ ухожу...')
        await upd.chat.leave()
        return

    await create_chat(upd.chat, upd.from_user)
    await bot.send_message(upd.from_user.id, f'Меня добавили в чат: {upd.chat.title}')


@chat_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION)
)
async def me_kicked(upd: types.ChatMemberUpdated):
    await delete_chat(upd.chat)
    await bot.send_message(upd.from_user.id, f'Меня больше нет в этом чате: {upd.chat.title}')


@chat_router.message(F.content_type == ContentType.TEXT)
async def new_message(msg: types.Message):
    chat = await get_tg_chat(msg.chat.id)
    if chat is None:
        await msg.answer('Я забыл своего создателя...\nМне придется покинуть этот чат :(')
        await msg.chat.leave()
        return

    keywords = set(chat.keywords.split(';'))
    words = msg.text.lower().split()

    if keywords.intersection(words):
        forward_msg = await bot.forward_message(chat.owner_id, msg.chat.id, msg.message_id, disable_notification=True)
        await forward_msg.answer(f'Сообщение из чата @{msg.chat.username}', disable_notification=True)
