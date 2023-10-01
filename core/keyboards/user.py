from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.database.models import Chat


def inline_select_chat(chats: List[Chat]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for chat in chats:
        builder.add(InlineKeyboardButton(
            text=chat.chat_title,
            callback_data=str(chat.id)
        ))

    return builder.as_markup()


def inline_chat_settings() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Ключевые слова',
            callback_data='keywords'
        ),
        InlineKeyboardButton(
            text='Сложные условия',
            callback_data='conditions'
        )
    ).row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='return'
        )
    )

    return builder.as_markup()


def inline_keywords_settings() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Добавить',
            callback_data='add_keywords'
        ),
        InlineKeyboardButton(
            text='Удалить',
            callback_data='delete_keywords'
        ),
        InlineKeyboardButton(
            text='Показать',
            callback_data='show_keywords'
        ),
    ).row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='return'
        )
    )

    return builder.as_markup()


def inline_conditions_settings() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Добавить',
            callback_data='add_expression'
        ),
        InlineKeyboardButton(
            text='Удалить',
            callback_data='delete_expression'
        ),
        InlineKeyboardButton(
            text='Показать',
            callback_data='show_expressions'
        ),
    ).row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='return'
        )
    )

    return builder.as_markup()


def inline_condition_help() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Помощь',
            callback_data='condition_help'
        )
    )
    return builder.as_markup()


def inline_db_settings() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Добавить',
            callback_data='add_db'
        ),
        InlineKeyboardButton(
            text='Удалить',
            callback_data='delete_db'
        ),
        InlineKeyboardButton(
            text='Показать',
            callback_data='show_db'
        )
    ).row(
        InlineKeyboardButton(
            text='Проверить в базе',
            callback_data='check_db'
        )
    )

    return builder.as_markup()