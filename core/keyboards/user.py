from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.database.models import Chat


def inline_select_chat(chats: List[Chat]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for chat in chats:
        builder.add(InlineKeyboardButton(
            text=chat.chat_title,
            callback_data=chat.id
        ))

    return builder.as_markup()


def inline_chat_settings() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Ключевые слова',
            callback_data='keywords'
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
        )
    ).row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='return'
        )
    )

    return builder.as_markup()
