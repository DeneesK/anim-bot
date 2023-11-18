from aiogram import types


def action(url: str):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
            types.InlineKeyboardButton(text='ACTION',  # noqa
                                       url=url))  # noqa
    return keyboard
