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
        await actions.user_start(message)
        await registration(message)
        await message.answer(text=const.WELCOME)
        db = PsgDB(await get_session())
        await db.add_user(message)
    except Exception as ex:
        logger.error(ex)
