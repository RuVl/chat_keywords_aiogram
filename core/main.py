from aiogram import Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from core import bot
from core.handlers import register_all_handlers


async def set_default_commands(bot):
    await bot.set_my_commands(
        [
            types.BotCommand(command='start', description='Запустить бота'),
            types.BotCommand(command='chats', description='Выбрать чат'),
            types.BotCommand(command='cancel', description='Отменить действие'),
        ]
    )


async def start_bot():
    dp = Dispatcher(storage=MemoryStorage())

    register_all_handlers(dp)

    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
