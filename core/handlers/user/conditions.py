import logging

from aiogram import Router, types
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext

from core.database.methods import add_chat_condition, delete_chat_condition
from core.database.models import Chat
from core.keyboards import inline_chat_settings, inline_condition_help, inline_conditions_settings
from core.misc import get_chat_from_state
from core.parsers import parse_condition
from core.state_machines import UserSettings

conditions_router = Router()


@conditions_router.callback_query(UserSettings.CONDITION_HANDLER)
async def conditions_settings(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f'Callback data {callback.data} from user: {callback.from_user.id}')

    match callback.data:
        case 'return':
            chat = await get_chat_from_state(callback.message, state)

            await callback.answer()
            await state.set_state(UserSettings.CHAT_SETTINGS)

            await callback.message.edit_text(f'Настройки чата {chat.chat_title}', reply_markup=inline_chat_settings())

        case 'add_expression':
            await callback.answer()

            await state.set_state(UserSettings.ADDING_CONDITION)
            await callback.message.answer('Введите сложное условие условие для добавления:\n'
                                          '/cancel для отмены',
                                          reply_markup=inline_condition_help())

        case 'delete_expression':
            await callback.answer()

            await state.set_state(UserSettings.DELETING_CONDITION)
            await callback.message.answer('Введите условие, которое хотите удалить\n'
                                          '/cancel для отмены')

        case 'show_expressions':
            await callback.answer()

            msg = await show_expressions(callback, state)
            await callback.message.answer(msg)


async def show_expressions(callback: types.CallbackQuery, state: FSMContext) -> str:
    chat = await get_chat_from_state(callback.message, state)
    if chat is None:
        return 'Chat not found!'

    return chat.raw_conditions.replace('^', '^\n') if chat.raw_conditions else 'Нет сложных условий!'


@conditions_router.callback_query(UserSettings.ADDING_CONDITION)
async def show_help(callback: types.CallbackQuery):
    help_text = (
        'Краткий справочник по созданию условий:\n'
        'Допустимы все Unicode символы, кроме: "[", "]", "^" и комбинации: "->"\n'
        'Ветвь условий: [условие] -> [условие] -> [условие]\n'
        'Условие: hello|привет\n'
        'Для добавления сразу нескольких ветвей используйте ^ после ветви\n'
        '=============\n'
        'Пример всех возможностей:\n'
        '[привет|пока]->[коин|руб|дол] -> [мне|тебе] -> [пж|спс] ^ [air|water] -> [port|clear]\n'
        'Соответствует строкам:\n'
        'Привет, МНЕ нужен один рУбЛь, скинь пж\n'
        'Я дышу clear air!!\n'
        '=============\n'        
        'Введите сложное условие условие для добавления:\n'
        '/cancel для отмены'
    )

    match callback.data:
        case 'condition_help':
            await callback.message.edit_text(help_text)


@conditions_router.message(~Command('cancel'), UserSettings.ADDING_CONDITION)
async def add_condition(msg: types.Message, state: FSMContext):
    logging.info(f'Add condition from user: {msg.from_user.id}')

    chat = await get_chat_from_state(msg, state)
    if chat is None:
        return

    try:
        parsed = parse_condition(msg.text)
    except SyntaxError as e:
        await msg.answer(f'Некорректный синтаксис:\n{e.msg}')
    else:
        chat = await add_chat_condition(msg.text, parsed, chat)
        await state.update_data(chat=chat)
        await msg.answer('Условие добавлено!')
    finally:
        await msg.answer('Введите сложное условие условие для добавления:\n'
                         '/cancel для отмены')


@conditions_router.message(~Command('cancel'), UserSettings.DELETING_CONDITION)
async def delete_keywords(msg: types.Message, state: FSMContext):
    logging.info(f'Delete condition from user: {msg.from_user.id}')

    chat = await get_chat_from_state(msg, state)
    if chat is None:
        return

    try:
        parsed = parse_condition(msg.text)
    except SyntaxError as e:
        await msg.answer(f'Некорректный синтаксис:\n{e.msg}')
    else:
        chat = await delete_chat_condition(msg.text, parsed, chat)
        await state.update_data(chat=chat)
        await msg.answer('Условие удалено!')
    finally:
        await msg.answer('Введите сложное условие условие для удаления:\n'
                         '/cancel для отмены')


@conditions_router.message(Command('cancel'), or_f(
    UserSettings.ADDING_CONDITION,
    UserSettings.DELETING_CONDITION
))
async def cancel(msg: types.Message, state: FSMContext):
    logging.info(f'Cancel command from user: {msg.from_user.id}')

    await state.set_state(UserSettings.CONDITION_HANDLER)

    data = await state.get_data()

    chat: Chat | None = data.get('chat')
    if chat is None:
        logging.warning('No chat selected!')
        await msg.answer(f'Сложные условия', reply_markup=inline_conditions_settings())
        return

    await msg.answer(f'Сложные условия чата {chat.chat_title}', reply_markup=inline_conditions_settings())
