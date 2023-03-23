from aiogram.fsm.state import StatesGroup, State


class SamDBSettings(StatesGroup):
    DB_SETTINGS = State()  # Выбор действия с базой данных
    CHECK_DB = State()  # Проверка в базе данных
    ADD_DB = State()  # Добавление в базу данных
    DELETE_DB = State()  # Удаление из базы данных
