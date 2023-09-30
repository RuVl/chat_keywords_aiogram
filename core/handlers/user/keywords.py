import logging

from aiogram import Router, types
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext

from core.database.methods import add_chat_keywords, delete_chat_keywords
from core.database.models import Chat
from core.keyboards import inline_keywords_settings, inline_chat_settings
from core.misc import get_chat_from_state
from core.parsers import parse_keywords
from core.state_machines import UserSettings

keywords_router = Router()


@keywords_router.callback_query(UserSettings.KEYWORDS_HANDLER)
async def keywords_settings(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f'Callback data {callback.data} from user: {callback.from_user.id}')

    match callback.data:
        case 'return':
            chat = await get_chat_from_state(callback.message, state)

            await callback.answer()
            await state.set_state(UserSettings.CHAT_SETTINGS)

            await callback.message.edit_text(f'Настройки чата {chat.chat_title}', reply_markup=inline_chat_settings())

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

        case 'show_keywords':
            await callback.answer()

            msg = await show_keywords(callback, state)
            await callback.message.answer(msg)


async def show_keywords(callback: types.CallbackQuery, state: FSMContext) -> str:
    chat = await get_chat_from_state(callback.message, state)
    return (
        '\n'.join(chat.keywords.split(';'))
        if chat.keywords else 'Нет ключевых слов!'
    )


@keywords_router.message(~Command('cancel'), UserSettings.ADDING_KEYWORDS)
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


@keywords_router.message(~Command('cancel'), UserSettings.DELETING_KEYWORDS)
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


@keywords_router.message(Command('cancel'), or_f(
    UserSettings.ADDING_KEYWORDS,
    UserSettings.DELETING_KEYWORDS
))
async def cancel(msg: types.Message, state: FSMContext):
    logging.info(f'Cancel command from user: {msg.from_user.id}')

    await state.set_state(UserSettings.KEYWORDS_HANDLER)

    data = await state.get_data()

    chat: Chat | None = data.get('chat')
    if chat is None:
        logging.warning('No chat selected!')
        await msg.answer(f'Ключевые слова', reply_markup=inline_keywords_settings())
        return

    await msg.answer(f'Ключевые слова чата {chat.chat_title}', reply_markup=inline_keywords_settings())
