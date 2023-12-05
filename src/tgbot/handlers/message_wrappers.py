from aiogram import types

from src.tgbot.analysis import actions
from src.settings import const


async def call_back_handler(message: types.CallbackQuery):
    if str(message.data).startswith('estimate'):  # noqa
        _, mark = str(message.data).split('-')
        await actions.send_estimate(message, mark)
        await message.bot.delete_message(message.from_user.id,
                                         message.message.message_id)
        await message.bot.send_message(message.from_user.id,
                                       text=const.THE_END)
