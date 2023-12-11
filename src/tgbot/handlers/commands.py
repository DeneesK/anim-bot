from aiogram import Dispatcher
from aiogram import types

from src.tgbot.handlers.users import user_start
from src.tgbot.handlers.handlers import photo_handler
from src.tgbot.handlers.message_wrappers import call_back_handler, reply_keybuttons_handler  # noqa


def register_commands(dp: Dispatcher):
    dp.register_message_handler(user_start, state="*", commands=["start"])


def register_content_type(dp: Dispatcher) -> None:
    dp.register_message_handler(photo_handler,
                                state='*',
                                content_types=['photo'])


def register_callback(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(call_back_handler,
                                       lambda callback_query: True)


def register_text(dp: Dispatcher) -> None:
    dp.register_message_handler(reply_keybuttons_handler,
                                state='*',
                                content_types=[types.ContentType.TEXT]
                                )
