from aiogram import Dispatcher

from src.tgbot.handlers.commands import register_commands


async def register_all_services(dp: Dispatcher):
    register_commands(dp)
