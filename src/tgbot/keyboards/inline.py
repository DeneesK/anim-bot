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
    # keyboard.add(types.InlineKeyboardButton(text=const.BUTTON_NEWONE, callback_data='newone')) # noqa
    return keyboard


def out_bot_sub(sublist: list):
    keyboard = types.InlineKeyboardMarkup()
    c = 0
    if len(sublist) % 2 != 0:
        c = 1
    mid = len(sublist) // 2
    i = 0
    n = 0
    # 1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟
    numbers = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣',
               5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'}
    for sub in sublist[0:(mid+c)]:
        n += 1
        number = numbers.get(n, '')
        button = f'{number} ' + sub['name']
        keyboard.add(
                types.InlineKeyboardButton(text=button,  # noqa
                                            url=sub['group_url']))  # noqa

        if (mid + c + i) < len(sublist):
            n += 1
            sub2 = sublist[mid + i + c]
            number = numbers.get(n, '')
            button = f'{number} ' + sub2['name']
            keyboard.insert(
                    types.InlineKeyboardButton(text=button,  # noqa
                                                url=sub2['group_url']))  # noqa            
        i += 1
    keyboard.add(types.InlineKeyboardButton(text='✅ Я подписался', callback_data='done'))  # noqa
    return keyboard


def at_end():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         is_persistent=True)
    keyboard.add(types.KeyboardButton(const.BUTTON_ONEMORE))
    # keyboard.insert(types.KeyboardButton(const.BUTTON_NEWONE))
    return keyboard


async def subscribe(txt: str, sub_url: str):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
            types.InlineKeyboardButton(text=txt,  # noqa
                                       url=sub_url))  # noqa
    return keyboard
