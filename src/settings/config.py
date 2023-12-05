from aiogram import Dispatcher

from src.tgbot.handlers.commands import register_commands, register_content_type, register_callback  # noqa


async def register_all_services(dp: Dispatcher):
    register_commands(dp)
    register_content_type(dp)
    register_callback(dp)
