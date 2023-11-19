from urllib.parse import quote

from aiogram import types

from src.settings import const


def action(url: str):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
            types.InlineKeyboardButton(text='Ссылка на приложение',  # noqa
                                       web_app=types.WebAppInfo(url)))  # noqa
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
