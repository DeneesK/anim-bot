from aiogram import types
from aiogram.utils.markdown import hlink
from PIL import Image

from src.settings import const
from src.settings.logger import logging
from src.database.service import PsgDB
from src.database.db import get_session
from src.tgbot.keyboards.inline import invite
from src.tgbot.requests import runod
from src.tgbot.utils.download import download
from src.tgbot.utils.url_creator import ref_url, organic_url
from src.tgbot.analysis import actions as action_


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
        photo = await message.bot.get_file(message.photo[-1].file_id)
        photo_url = await photo.get_url()

        sticker = await message.bot.send_sticker(chat_id=message.from_user.id, # noqa
                                                 sticker=const.STICKER_ID)

        mask = await runod.request_mask(photo_url)
        # path = await download(photo_url, message.from_user.id)
        if not mask:
            logger.error('NO MASK')
        msg = await message.bot.send_photo(
            chat_id=const.ADMIN_ID,
            photo=mask
        )
        mask = await msg.photo[0].get_url()
        if user.tokens < 1:
            url = ref_url(message.from_user.id)
            await message.bot.send_message(message.from_user.id,
                                           text=const.END,
                                           reply_markup=invite(url))
            return
        path = await download(mask, message.from_user.id)
        w, h = resize(path)
        logger.info(f'SIZE---->{(w, h)}')
        path = download(photo_url, message.from_user.id)
        Image.open(path).resize(w, h).save(path)

        photo = await message.bot.send_photo(
            chat_id=const.ADMIN_ID,
            photo=types.InputFile(path)
        )
        photo_url = photo.photo[0].get_url()
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
            origin = photo.file_id
            mask = msg.photo[0].file_id
            result = r.photo[0].file_id
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
