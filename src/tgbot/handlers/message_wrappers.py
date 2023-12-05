from aiogram import types

from src.tgbot.analysis import actions
from src.settings import const
from src.database.cache import get_redis


async def call_back_handler(message: types.CallbackQuery):
    if str(message.data).startswith('estimate'):  # noqa
        cache = get_redis()
        to_delete = await cache.get(message.from_user.id)
        to_delete = int(to_delete.decode('utf-8'))
        _, mark = str(message.data).split('-')
        await actions.send_estimate(message, mark)
        await message.bot.delete_message(message.from_user.id,
                                         to_delete)
        await message.bot.send_message(message.from_user.id,
                                       text=const.THE_END)
