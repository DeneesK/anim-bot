import os
import asyncio

from aiogram import types
from aiogram.utils.markdown import hlink
from PIL import Image

from src.settings import const
from src.settings.logger import logging
from src.database.service import PsgDB, SubListDB
from src.database.cache import get_redis
from src.database.db import get_session
from src.tgbot.keyboards.inline import invite, estimate, subscribe
from src.tgbot.requests import runod
from src.tgbot.utils.url_creator import ref_url, organic_url
from src.tgbot.analysis import actions as action_
from src.tgbot.utils.blur import blur_it


logger = logging.getLogger(__name__)


async def sub_check(message: types.Message) -> bool:
    try:
        subDb = SubListDB(await get_session())
        r = await subDb.get_sublist()
        print(r)
        status = await message.bot.get_chat_member(int(os.environ.get('SUB_ID')),  # noqa
                                                    message.from_user.id)  # noqa
        if status["status"] != 'left':
            return True
        return False
    except Exception as ex:
        logger.error(ex)


async def photo_handler(message: types.Message):
    try:
        if message.media_group_id:
            await message.bot.send_message(message.from_user.id,
                                           text=const.TOO_MUCH)
            return

        if not await sub_check(message):
            photo = await message.bot.get_file(message.photo[-1].file_id)
            photo_url = await photo.get_url()
            blur = await blur_it(photo_url, message.from_user.id)
            msg_sub = await message.bot.send_photo(message.from_user.id,
                                                   photo=types.InputFile(blur),
                                                   caption=const.SUB_TEXT,
                                                   reply_markup=subscribe())
            is_sub = False

            while not is_sub:
                is_sub = await sub_check(message)
                if is_sub:
                    await message.bot.delete_message(message.from_user.id, msg_sub.message_id)  # noqa
                await asyncio.sleep(1)

        await action_.user_sent_photo(message)
        db = PsgDB(await get_session())
        user = await db.find_user(message.from_user.id)

        if user.tokens < 1:
            url = ref_url(message.from_user.id)
            await message.bot.send_message(message.from_user.id,
                                           text=const.END,
                                           reply_markup=invite(url))
            return
        photo = await message.bot.get_file(message.photo[-1].file_id)
        photo_url = await photo.get_url()

        sticker = await message.bot.send_sticker(chat_id=message.from_user.id, # noqa
                                                 sticker=const.STICKER_ID)

        mask = await runod.request_mask(photo_url)

        if not mask:
            logger.error('NO MASK')
        msg = await message.bot.send_photo(
            chat_id=const.ADMIN_ID,
            photo=mask
        )
        mask = await msg.photo[-1].get_url()
        if user.tokens < 1:
            url = ref_url(message.from_user.id)
            await message.bot.send_message(message.from_user.id,
                                           text=const.END,
                                           reply_markup=invite(url))

        result = await runod.request_processing(photo_url, mask)

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
            r = await message.bot.send_photo(message.from_user.id,
                                             photo=result,
                                             caption=text)
            to_delete = await message.bot.send_message(message.from_user.id,
                                                       text=const.IN_THE_END,
                                                       reply_markup=estimate())  # noqa
            cache = get_redis()
            await cache.set(message.from_user.id, to_delete.message_id)
            origin = photo.file_id
            mask = msg.photo[-1].file_id
            result = r.photo[-1].file_id
            await admin_notify(message, origin, result, mask)
    except Exception as ex:
        logger.error(ex)


async def admin_notify(message: types.Message,
                       origin: str,
                       result: str,
                       mask: str,
                       ):
    media = types.MediaGroup()
    text = f'username: {message.from_user.username}; user_id: {message.from_user.id}'  # noqa
    media.attach_photo(origin, text)
    media.attach_photo(result)
    media.attach_photo(mask)
    await message.bot.send_media_group(chat_id=const.ADMIN_GROUP,
                                       media=media)


def resize(path: str) -> tuple[int, int]:
    image = Image.open(path)
    w = image.width
    h = image.height

    if h < 1024 and w < 1024:
        if h % 8 == 0 and w % 8 == 0:
            return w, h
        w = w - (w % 8)
        h = h - (h % 8)
        return w, h

    while True:
        if h < 1024 and w < 1024:
            if h % 8 == 0 and w % 8 == 0:
                return w, h
            w = w - (w % 8)
            h = h - (h % 8)
            return w, h
        h = int(h / 2)
        w = int(w / 2)
