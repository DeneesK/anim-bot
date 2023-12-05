from aiogram import Dispatcher

from src.tgbot.handlers.users import user_start
from src.tgbot.handlers.handlers import photo_handler
from src.tgbot.handlers.message_wrappers import call_back_handler


def register_commands(dp: Dispatcher):
    dp.register_message_handler(user_start, state="*", commands=["start"])


def register_content_type(dp: Dispatcher) -> None:
    dp.register_message_handler(photo_handler,
                                state='*',
                                content_types=['photo'])


def register_callback(dp) -> None:
    dp.register_callback_query_handler(call_back_handler,
                                       lambda callback_query: True)
