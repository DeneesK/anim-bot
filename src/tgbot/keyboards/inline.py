from urllib.parse import quote

from aiogram import types

from src.settings import const


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


async def subscribe(txt: str, sub_url: str):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
            types.InlineKeyboardButton(text=txt,  # noqa
                                       url=sub_url))  # noqa
    return keyboard
