from aiogram.fsm.state import StatesGroup, State


class UserSettings(StatesGroup):
    CHOOSE_CHAT = State()  # Выбор чата
    CHAT_SETTINGS = State()  # Выбор действия с чатом

    KEYWORDS_HANDLER = State()  # Действие с ключевыми словами
    ADDING_KEYWORDS = State()  # Добавление ключевых слов
    DELETING_KEYWORDS = State()  # Удаление ключевых слов

    CONDITION_HANDLER = State()  # Действие с условиями
    ADDING_CONDITION = State()  # Добавление условия
    DELETING_CONDITION = State()  # Удаление условия
