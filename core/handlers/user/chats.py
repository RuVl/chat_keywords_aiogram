import logging

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.database import session_maker
from core.database.methods import get_or_create_tg_user, get_tg_user
from core.database.models import Chat
from core.handlers.user.conditions import conditions_router
from core.handlers.user.keywords import keywords_router
from core.keyboards import inline_select_chat, inline_chat_settings, inline_keywords_settings, inline_conditions_settings
from core.state_machines import UserSettings

chats_router = Router()
chats_router.include_routers(keywords_router, conditions_router)

chats_router.message.filter(
    F.chat.type == 'private',
)

chats_router.callback_query.filter(
    F.message.chat.type == 'private',
)


@chats_router.message(Command('chats'))
async def chats(msg: types.Message, state: FSMContext):
    logging.info(f'Command /chats from user: {msg.from_user.id}')

    user = await get_or_create_tg_user(msg.from_user)
    if user and user.chats:
        await state.update_data(user=user)
        await state.set_state(UserSettings.CHOOSE_CHAT)
        await msg.answer('Выберите чаты: ', reply_markup=inline_select_chat(user.chats))
    else:
        await msg.answer('Для начала добавьте меня в чаты.')


@chats_router.callback_query(UserSettings.CHOOSE_CHAT)
async def chat_selected(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f'Callback data {callback.data} from user: {callback.from_user.id}')

    if not callback.data.isdigit():
        return

    async with session_maker() as session:
        chat = await session.get(Chat, int(callback.data))

    if chat is None:
        await callback.answer('Меня нет в этом чате ://', show_alert=True)
        await state.clear()
        await callback.message.delete()
        return

    if chat.owner_id != callback.from_user.id:
        await callback.answer('Вы не владелец этого чата!', show_alert=True)
        await state.clear()
        await callback.message.delete()
        return

    await callback.answer()

    await state.update_data(chat=chat)
    await state.set_state(UserSettings.CHAT_SETTINGS)
    await callback.message.edit_text(f'Настройки чата {chat.chat_title}', reply_markup=inline_chat_settings())


@chats_router.callback_query(UserSettings.CHAT_SETTINGS)
async def chat_settings(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f'Callback data {callback.data} from user: {callback.from_user.id}')

    data = await state.get_data()

    chat: Chat | None = data.get('chat')
    if chat is None:
        logging.warning('No chat selected!')

    match callback.data:
        case 'return':
            user = data.get('user')
            if user is None:
                user = get_tg_user(callback.from_user.id)

            await state.clear()
            await callback.answer()

            await state.update_data(user=user)
            await state.set_state(UserSettings.CHOOSE_CHAT)
            await callback.message.edit_text('Выберите чаты', reply_markup=inline_select_chat(user.chats))

        case 'keywords':
            if chat is None:
                await callback.answer('Чат не выбран!')
                return

            await callback.answer()

            await state.set_state(UserSettings.KEYWORDS_HANDLER)
            await callback.message.edit_text(f'Ключевые слова чата {chat.chat_title}', reply_markup=inline_keywords_settings())

        case 'conditions':
            if chat is None:
                await callback.answer('Чат не выбран!')
                return

            await callback.answer()

            await state.set_state(UserSettings.CONDITION_HANDLER)
            await callback.message.edit_text(f'Сложными условия чата {chat.chat_title}', reply_markup=inline_conditions_settings())
