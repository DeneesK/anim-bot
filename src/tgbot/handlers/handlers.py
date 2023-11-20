import os
import asyncio

from aiogram import types
from aiogram.utils.markdown import hlink

from src.settings import const
from src.settings.logger import logging
from src.tgbot.utils import download
from src.app.app import start
from src.database.service import PsgDB
from src.database.db import get_session
from src.tgbot.keyboards.inline import action, invite
from src.tgbot.requests.predict import request
from src.tgbot.utils.url_creator import ref_url, organic_url
from src.tgbot.analysis import actions as action_


logger = logging.getLogger(__name__)


async def photo_handler(message: types.Message):
    try:
        await action_.user_sent_photo(message)
        db = PsgDB(await get_session())
        user = await db.find_user(message.from_user.id)
        if user.tokens < 1:
            url = ref_url(message.from_user.id)
            await message.bot.send_message(message.from_user.id,
                                           text=const.END,
                                           reply_markup=invite(url))
            return

        if os.path.exists(f'img/{message.from_user.id}-mask.png'):
            os.remove(f'img/{message.from_user.id}-mask.png')

        photo = await message.bot.get_file(message.photo[-1].file_id)
        photo_url = await photo.get_url()
        path = await download.download(photo_url, message.from_user.id)
        url = start(path=path)
        await message.bot.send_message(message.from_user.id,
                                       text='Перейди по ссылке, что бы раздеть',  # noqa
                                       reply_markup=action(url))
        not_ready = True
        while not_ready:
            if os.path.exists(f'img/{message.from_user.id}-mask.png'):  # noqa
                break
            await asyncio.sleep(1.5)
        sticker = await message.bot.send_sticker(chat_id=message.from_user.id, # noqa
                                                 sticker=const.STICKER_ID)
        path_ = f'img/{message.from_user.id}-mask.png'

        msg = await message.bot.send_photo(
            chat_id=const.ADMIN_ID,
            photo=types.InputFile(
                path_
            )
        )

        mask = await msg.photo[0].get_url()
        if user.tokens < 1:
            url = ref_url(message.from_user.id)
            await message.bot.send_message(message.from_user.id,
                                           text=const.END,
                                           reply_markup=invite(url))
            return

        result = await request(photo_url, mask, message)

        if result:
            if user.tokens < 1:
                url = ref_url(message.from_user.id)
                await message.bot.send_message(message.from_user.id,
                                               text=const.END,
                                               reply_markup=invite(url))
                return
            await message.bot.delete_message(message.from_user.id,
                                             sticker.message_id)
            await action_.sent_result(message)
            await db.add_token(message.from_user.id, -1)
            url = organic_url(message.from_user.id)
            text = hlink(const.CONG, url)
            await message.bot.send_photo(message.from_user.id,
                                         photo=result,
                                         caption=text)
            text = f'username: {message.from_user.username}; user_id: {message.from_user.id}'  # noqa
            await message.bot.send_photo(const.ADMIN_GROUP,
                                         photo=result,
                                         caption=text)
    except Exception as ex:
        logger.error(ex)
