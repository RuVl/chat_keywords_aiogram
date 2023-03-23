from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.database.methods import get_sam_db, get_by_numbers, delete_sam_db, create_sam_dbs
from core.keyboards.user import inline_db_settings
from core.misc import parse_sam_db, parse_db_numbers
from core.state_machines import SamDBSettings

sam_db_router = Router()

sam_db_router.message.filter(
    F.from_user.id.in_({1167202040, 1285638448}),
)

sam_db_router.callback_query.filter(
    F.from_user.id.in_({1167202040, 1285638448}),
)


@sam_db_router.message(Command('db'))
async def db(msg: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(SamDBSettings.DB_SETTINGS)
    await msg.answer('Выберите действие с базой данных:', reply_markup=inline_db_settings())


@sam_db_router.callback_query(SamDBSettings.DB_SETTINGS)
async def action_selected(callback: types.CallbackQuery, state: FSMContext):
    match callback.data:
        case 'add_db':
            await state.set_state(SamDBSettings.ADD_DB)
            await callback.answer()
            await callback.message.answer('Напишите данные для добавления в базу данных в формате "имя", "фамилия при наличии" - "номер".\n'
                                          'Для добавления нескольких строк напишите данные с новой строки.')

        case 'delete_db':
            await state.set_state(SamDBSettings.DELETE_DB)
            await callback.answer()
            await callback.message.answer('Напишите данные для удаления из базы данных в формате как при добавлении или только номера.\n'
                                          'Для удаления нескольких строк напишите данные с новой строки.')

        case 'show_db':
            db = await get_sam_db()
            data = '\n'.join(map(str, db))

            await callback.answer()
            if db:
                await callback.message.answer(data)
            else:
                await callback.message.answer('В базе пока нет данных.')

        case 'check_db':
            await state.set_state(SamDBSettings.CHECK_DB)
            await callback.answer()
            await callback.message.answer('Напишите номер телефона для поиска (если более одного - с новой строки):')


@sam_db_router.message(~Command('cancel'), SamDBSettings.CHECK_DB)
async def check_number(msg: types.Message):
    numbers = parse_db_numbers(msg.text)
    if isinstance(numbers, str):
        await msg.answer(f'Ошибка в строке:\n{numbers}\nПовторите ввод или остановите меня /cancel')
        return

    data = await get_by_numbers(numbers)
    result = '\n'.join(map(str, data) if isinstance(data, list) else [str(data)])

    await msg.answer(
        f'Данные найдены:\n{result}\nВведите ещё строки или остановите меня /cancel'
        if data else
        'В базе данных нет такого номера!\nВведите ещё строки или остановите меня /cancel'
    )


@sam_db_router.message(~Command('cancel'), SamDBSettings.ADD_DB)
async def add_data(msg: types.Message):
    res = parse_sam_db(msg.text)
    if isinstance(res, str):
        await msg.answer(f'Ошибка в строке:\n{res}\nПовторите ввод или остановите меня /cancel')
        return

    await create_sam_dbs(res)
    await msg.answer('Данные записаны в базу данных.\nВведите ещё строки или остановите меня /cancel')


@sam_db_router.message(~Command('cancel'), SamDBSettings.DELETE_DB)
async def delete_data(msg: types.Message):
    numbers = parse_db_numbers(msg.text)
    if isinstance(numbers, str):
        await msg.answer(f'Ошибка в строке:\n{numbers}\nПовторите ввод или остановите меня /cancel')
        return

    await delete_sam_db(numbers)
    await msg.answer('Данные удалены из базы данных.\nВведите ещё строки или остановите меня /cancel')


@sam_db_router.message(Command('cancel'), SamDBSettings.ADD_DB)
@sam_db_router.message(Command('cancel'), SamDBSettings.DELETE_DB)
@sam_db_router.message(Command('cancel'), SamDBSettings.CHECK_DB)
async def cancel(msg: types.Message, state: FSMContext):
    await state.set_state(SamDBSettings.DB_SETTINGS)
    await msg.answer('Выберите действие с базой данных:', reply_markup=inline_db_settings())
