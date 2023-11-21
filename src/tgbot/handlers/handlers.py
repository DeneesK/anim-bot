import os
import asyncio
import random

from aiogram import types
from aiogram.utils.markdown import hlink

from src.settings import const
from src.settings.logger import logging
from src.tgbot.utils import download
from src.database.service import PsgDB
from src.database.db import get_session
from src.tgbot.keyboards.inline import action, invite
from src.tgbot.requests.predict import request
from src.tgbot.utils.url_creator import ref_url, organic_url
from src.tgbot.analysis import actions as action_
from src.database.cache import get_redis


logger = logging.getLogger(__name__)


async def photo_handler(message: types.Message):
    try:
        if message.media_group_id:
            await message.bot.send_message(message.from_user.id,
                                           text=const.TOO_MUCH)
            return

        await action_.user_sent_photo(message)
        db = PsgDB(await get_session())
        user = await db.find_user(message.from_user.id)

        if user.tokens < 1:
            url = ref_url(message.from_user.id)
            await message.bot.send_message(message.from_user.id,
                                           text=const.END,
                                           reply_markup=invite(url))
            return
        cache = get_redis()
        photo = await message.bot.get_file(message.photo[-1].file_id)
        photo_url = await photo.get_url()
        sol_ = f'{message.from_user.id}{random.randint(0, 10_000_000)}'
        path = await download.download(photo_url, sol_)
        url = await cache.get('app')
        print(url)
        url = url.decode('utf-8')+f'?url={path}'
        print(f'{url}-------bot')
        await message.bot.send_message(message.from_user.id,
                                       text='Перейди по ссылке, что бы раздеть',  # noqa
                                       reply_markup=action(url))  # noqa

        i = 600

        while not await cache.get(sol_):
            await asyncio.sleep(0.2)

        sol_ = await cache.get(sol_)
        logger.info(f'SOL*****{sol_}')
        sol_ = sol_.decode('utf-8')

        while True:
            if os.path.exists(f'img/{sol_}-mask.png'):  # noqa
                logger.info(f'FIND--------->{sol_}')
                break
            i -= 1
            sol_ = await cache.get(sol_)
            logger.info(f'SOL*****{sol_}')
            sol_ = sol_.decode('utf-8')
            if i < 1:
                return
            await asyncio.sleep(0.2)

        sticker = await message.bot.send_sticker(chat_id=message.from_user.id, # noqa
                                                 sticker=const.STICKER_ID)
        path_ = f'img/{sol_}-mask.png'

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
