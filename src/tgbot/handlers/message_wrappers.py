from aiogram import types

from src.tgbot.analysis import actions


async def call_back_handler(message: types.CallbackQuery):
    if str(message.data).startswith('estimate'):  # noqa
        _, mark = str(message.data).split('-')
        await actions.send_estimate(message, mark)
        await message.bot.delete_message(message.from_user.id, message.id)
