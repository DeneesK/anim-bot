from urllib.parse import quote

from aiogram import types
from src.database.service import SubListDB
from src.database.db import get_session

from src.settings import const


def action(url: str):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
            types.InlineKeyboardButton(text='Раздеть...',  # noqa
                                       web_app=types.WebAppInfo(url=url)))  # noqa
    return keyboard


def invite(url: str):
    keyboard = types.InlineKeyboardMarkup()
    text = str(const.INVITE_FRIEND)
    text = quote(text + url)
    keyboard.add(
            types.InlineKeyboardButton(text='🌐 Пригласить',  # noqa
                                       url=f'https://t.me/share/url?text={text}&url=', # noqa
                                       encoding=False
                                       )
    )
    return keyboard


def estimate():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='👍🏻', callback_data='estimate-like')) # noqa
    keyboard.insert(types.InlineKeyboardButton(text='👎🏻', callback_data='estimate-dislike')) # noqa
    return keyboard


async def subscribe():
    subDb = SubListDB(await get_session())
    r = await subDb.get_sublist()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
            types.InlineKeyboardButton(text='🌐 Подписаться',  # noqa
                                       url=str(r[1])))  # noqa
    return keyboard
