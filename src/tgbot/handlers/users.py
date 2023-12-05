from aiogram import types

from src.settings import const
from src.settings.logger import logging
from src.tgbot.analysis import actions
from src.database.service import PsgDB
from src.database.db import get_session


logger = logging.getLogger(__name__)


async def registration(message: types.Message):
    try:
        db = PsgDB(await get_session())
        await db.add_user(message)
        await actions.amplitude_registration(message)
    except Exception as error:
        text_error = f'Ошибка при регистрации {message.from_user.id}:\n' \
                     f' >>> {error}'
        await actions.amplitude_error(message, text_error)
        logger.error(error)
        return False


async def user_start(message: types.Message):
    try:
        db = PsgDB(await get_session())
        payload = message.get_args()
        if payload != '':
            user_id = message.from_user.id
            if payload.startswith('ref_') and not await db.find_user(user_id):
                ref_user_id = int(payload[4:])
                await db.add_token(ref_user_id, 10)
                await actions.ref_reg(message,
                                      userid_referral=ref_user_id)
                await message.bot.send_message(user_id, text=const.GOT_TOKEN)
            if payload.startswith('organic_'):
                user_id = int(payload[8:])
                await actions.organic_reg(message, user_id)
        await actions.user_start(message)
        await registration(message)
        await message.bot.send_photo(
            message.from_user.id,
            caption=const.WELCOME,
            photo=types.InputFile('src/imgs/start.jpg')
            )
    except Exception as ex:
        logger.error(ex)
