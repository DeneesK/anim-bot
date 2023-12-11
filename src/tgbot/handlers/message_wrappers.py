from aiogram import types

from src.tgbot.handlers.handlers import one_more
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
        msg = await message.bot.send_message(message.from_user.id,
                                             text=const.THE_END)

        await cache.set(message.from_user.id, msg.message_id)
    if str(message.data).startswith('newone'):
        await message.bot.send_message(message.from_user.id,
                                       text=const.ONE_MORE)
    if str(message.data).startswith('onemore'):
        await one_more(message)


async def reply_keybuttons_handler(message: types.Message):
    if str(message.data).startswith(const.BUTTON_NEWONE):
        await message.bot.send_message(message.from_user.id,
                                       text=const.ONE_MORE)
    if str(message.data).startswith(const.BUTTON_ONEMORE):
        await one_more(message)
