from aiogram import types

from src.tgbot.utils import download
from src.app.app import start
from src.tgbot.keyboards.inline import action


async def photo_handler(message: types.Message):
    photo = await message.bot.get_file(message.photo[-1].file_id)
    photo_url = await photo.get_url()
    path = await download.download(photo_url, message.from_user.id)
    url = start(path=path)
    await message.bot.send_message(message.from_user.id,
                                   text='Перейди по ссылке, что бы раздеть',
                                   reply_markup=action(url))
