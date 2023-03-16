import logging

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.database import session_maker
from core.database.methods import get_or_create_tg_user, get_tg_user, add_chat_keywords, delete_chat_keywords
from core.database.models import Chat
from core.keyboards import inline_select_chat, inline_chat_settings, inline_keywords_settings
from core.misc import parse_keywords, get_chat_from_state
from core.state_machines import UserSettings

settings_router = Router()

settings_router.my_chat_member.filter(
    F.chat.type == 'private',
)


@settings_router.message(Command('chats'))
async def chats(msg: types.Message, state: FSMContext):
    logging.info(f'Command /chats from user: {msg.from_user.id}')

    user = await get_or_create_tg_user(msg.from_user)
    if user and user.chats:
        await state.update_data(user=user)
        await state.set_state(UserSettings.CHOOSE_CHAT)
        await msg.answer('Выберите чаты: ', reply_markup=inline_select_chat(user.chats))
    else:
        await msg.answer('Для начала добавьте меня в чаты.')


@settings_router.callback_query(UserSettings.CHOOSE_CHAT)
async def chat_selected(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f'Callback data {callback.data} from user: {callback.from_user.id}')

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


@settings_router.callback_query(UserSettings.CHAT_SETTINGS)
async def chat_settings(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f'Callback data {callback.data} from user: {callback.from_user.id}')

    match callback.data:
        case 'return':
            data = await state.get_data()

            user = data.get('user')
            if user is None:
                user = get_tg_user(callback.from_user.id)

            await state.clear()
            await callback.answer()

            await state.update_data(user=user)
            await state.set_state(UserSettings.CHOOSE_CHAT)
            await callback.message.edit_text('Выберите чаты', reply_markup=inline_select_chat(user.chats))

        case 'keywords':
            await callback.answer()

            await state.set_state(UserSettings.KEYWORDS_HANDLER)
            await callback.message.edit_text('Выберите действие с ключевыми словами', reply_markup=inline_keywords_settings())


@settings_router.callback_query(UserSettings.KEYWORDS_HANDLER)
async def keywords_settings(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f'Callback data {callback.data} from user: {callback.from_user.id}')

    match callback.data:
        case 'return':
            chat = await get_chat_from_state(callback.message, state)

            await callback.answer()
            await state.set_state(UserSettings.CHAT_SETTINGS)

            await callback.message.edit_text(f'Настройки чата {chat.chat_title}', reply_markup=inline_chat_settings())

        case 'show_keywords':
            chat = await get_chat_from_state(callback.message, state)

            await callback.answer()
            await callback.message.answer(
                '\n'.join(chat.keywords.split(';'))
                if chat.keywords else
                'Нет ключевых слов!'
            )

        case 'add_keywords':
            await callback.answer()

            await state.set_state(UserSettings.ADDING_KEYWORDS)
            await callback.message.answer('Введите ключевые слова по одному или через ";" для добавления\n'
                                          '/cancel для отмены')

        case 'delete_keywords':
            await callback.answer()

            await state.set_state(UserSettings.DELETING_KEYWORDS)
            await callback.message.answer('Введите ключевые слова по одному или через ";" для удаления\n'
                                          '/cancel для отмены')


@settings_router.message(~Command('cancel'), UserSettings.ADDING_KEYWORDS)
async def add_keywords(msg: types.Message, state: FSMContext):
    logging.info(f'Add keywords from user: {msg.from_user.id}')

    chat = await get_chat_from_state(msg, state)
    if chat is None:
        return

    keywords = parse_keywords(msg.text)
    chat = await add_chat_keywords(keywords, chat)
    await state.update_data(chat=chat)

    await msg.answer('Ключевые слова добавлены!')

    await msg.answer('Введите ключевые слова по одному или через ";" для добавления\n'
                     '/cancel для отмены')


@settings_router.message(~Command('cancel'), UserSettings.DELETING_KEYWORDS)
async def delete_keywords(msg: types.Message, state: FSMContext):
    logging.info(f'Delete keywords from user: {msg.from_user.id}')

    chat = await get_chat_from_state(msg, state)
    if chat is None:
        return

    keywords = parse_keywords(msg.text)
    chat = await delete_chat_keywords(keywords, chat)
    await state.update_data(chat=chat)

    await msg.answer('Ключевые слова удалены!')

    await msg.answer('Введите ключевые слова по одному или через ";" для удаления\n'
                     '/cancel для отмены')


@settings_router.message(Command('cancel'), UserSettings.ADDING_KEYWORDS)
@settings_router.message(Command('cancel'), UserSettings.DELETING_KEYWORDS)
async def cancel(msg: types.Message, state: FSMContext):
    logging.info(f'Cancel command from user: {msg.from_user.id}')

    await state.set_state(UserSettings.KEYWORDS_HANDLER)
    await msg.answer('Выберите действие с ключевыми словами', reply_markup=inline_keywords_settings())
