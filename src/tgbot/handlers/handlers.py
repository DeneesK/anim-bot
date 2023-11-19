import os
import asyncio

from aiogram import types

from src.settings import const
from src.tgbot.utils import download
from src.app.app import start
from src.tgbot.keyboards.inline import action
from src.tgbot.requests.replicate import request


async def photo_handler(message: types.Message):
    if os.path.exists(f'img/{message.from_user.id}-mask.png'):
        os.remove(f'img/{message.from_user.id}-mask.png')
    photo = await message.bot.get_file(message.photo[-1].file_id)
    photo_url = await photo.get_url()
    path = await download.download(photo_url, message.from_user.id)
    url = start(path=path)
    await message.bot.send_message(message.from_user.id,
                                   text='Перейди по ссылке, что бы раздеть',
                                   reply_markup=action(url))
    not_ready = True
    while not_ready:
        not_ready = not os.path.exists(f'img/{message.from_user.id}-mask.png')
        await asyncio.sleep(1.5)

    msg = await message.bot.send_photo(
        chat_id=const.ADMIN_ID,
        photo=types.InputFile(
            f'img/{message.from_user.id}-mask.png'
        )
    )

    mask = await msg.photo[0].get_url()

    data = await request(photo_url, mask, message)

    result = data.get('output', None)

    if result:
        await message.bot.send_photo(message.from_user.id,
                                     photo=result)
