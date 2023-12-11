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


def inline_at_end():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=const.BUTTON_ONEMORE, callback_data='onemore')) # noqa
    keyboard.add(types.InlineKeyboardButton(text=const.BUTTON_NEWONE, callback_data='newone')) # noqa
    return keyboard


def at_end():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(const.BUTTON_ONEMORE))
    keyboard.add(types.KeyboardButton(const.BUTTON_NEWONE))
    return keyboard


async def subscribe(txt: str, sub_url: str):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
            types.InlineKeyboardButton(text=txt,  # noqa
                                       url=sub_url))  # noqa
    return keyboard
