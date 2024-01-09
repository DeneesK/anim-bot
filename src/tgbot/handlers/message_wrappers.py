from aiogram import types

from src.tgbot.handlers.handlers import one_more
from src.tgbot.analysis import actions
from src.settings import const
from src.database.cache import get_redis
from src.database.service import SubListDB
from src.database.db import get_session


async def call_back_handler(message: types.CallbackQuery):
    if str(message.data).startswith('estimate'):  # noqa
        cache = get_redis()
        to_delete = await cache.get(message.from_user.id)
        to_delete = int(to_delete.decode('utf-8'))
        _, mark = str(message.data).split('-')
        await message.bot.delete_message(message.from_user.id,
                                         to_delete)
        msg = await message.bot.send_message(message.from_user.id,
                                             text=const.THE_END)
        await actions.send_estimate(message, mark)

        await cache.set(message.from_user.id, msg.message_id)
    if str(message.data).startswith('onemore'):
        await one_more(message)
    if str(message.data).startswith('done'):
        subDb = SubListDB(await get_session())
        await subDb.done(message.from_user.id)
        cache = get_redis()
        if await cache.get(f'{message.from_user.id}-all'):
            await cache.set(f'{message.from_user.id}-all-1', 1)
            return
        check = await cache.get(f'{message.from_user.id}-check')
        if check:
            try:
                to_delete = await cache.get(f'{message.from_user.id}-wait')
                to_delete = int(to_delete)
                await message.bot.delete_message(message.from_user.id,
                                                 to_delete)
            except Exception as ex:
                print(ex)
            msg = await message.bot.send_message(message.from_user.id,
                                                 text="📝 Что бы продолжить необходимо подписаться")
            await cache.set(f'{message.from_user.id}-wait', msg.message_id)



async def reply_keybuttons_handler(message: types.Message):
    if str(message.text).startswith(const.BUTTON_ONEMORE):
        await one_more(message)
