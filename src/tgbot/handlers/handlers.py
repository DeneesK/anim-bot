import asyncio

from aiogram import types, Bot
from aiogram.utils.markdown import hlink

from src.settings import const
from src.settings.logger import logging
from src.database.service import PsgDB, SubListDB
from src.database.cache import get_redis
from src.database.db import get_session
from src.tgbot.keyboards.inline import invite, estimate, subscribe, at_end, inline_at_end  # noqa
from src.tgbot.requests import runod
from src.tgbot.utils.url_creator import ref_url, organic_url
from src.tgbot.analysis import actions as action_
from src.tgbot.utils.blur import blur_it


logger = logging.getLogger(__name__)


async def photo_handler(message: types.Message):
    try:
        if message.media_group_id:
            await message.bot.send_message(message.from_user.id,
                                           text=const.TOO_MUCH)
            return

        await del_msg(message)

        subDb = SubListDB(await get_session())
        sublist = await subDb.get_sublist()

        if sublist:
            amount = await to_sub(message, sublist)
            await action_.user_sub_all(message, amount)

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
        cache = get_redis()
        await cache.set(f'photo-{message.from_user.id}', str(message.photo[-1].file_id)) # noqa
        sticker = await message.bot.send_sticker(chat_id=message.from_user.id, # noqa
                                                 sticker=const.STICKER_ID)

        if user.tokens < 1:
            url = ref_url(message.from_user.id)
            await message.bot.send_message(message.from_user.id,
                                           text=const.END,
                                           reply_markup=invite(url))

        result = await runod.request_processing(photo_url)

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
                                             caption=text,
                                             reply_markup=inline_at_end())
            to_delete = await message.bot.send_message(message.from_user.id,
                                                       text=const.IN_THE_END,
                                                       reply_markup=estimate())  # noqa
            await cache.set(message.from_user.id, to_delete.message_id)
            origin = photo.file_id
            result = r.photo[-1].file_id
            await admin_notify(message, origin, result)
    except Exception as ex:
        logger.error(ex)


async def one_more(message: types.Message):
    try:

        subDb = SubListDB(await get_session())
        sublist = await subDb.get_sublist()

        if sublist:
            amount = await to_sub(message, sublist)
            await action_.user_sub_all(message, amount)

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
        photo_id = await cache.get(f'photo-{message.from_user.id}')
        photo_id = str(photo_id.decode('utf-8'))
        photo = await message.bot.get_file(photo_id)
        photo_url = await photo.get_url()
        await cache.set(f'photo-{message.from_user.id}', photo_id)
        sticker = await message.bot.send_sticker(chat_id=message.from_user.id, # noqa
                                                 sticker=const.STICKER_ID)

        if user.tokens < 1:
            url = ref_url(message.from_user.id)
            await message.bot.send_message(message.from_user.id,
                                           text=const.END,
                                           reply_markup=invite(url))

        result = await runod.request_processing(photo_url)

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
                                             caption=text,
                                             reply_markup=inline_at_end())
            to_delete = await message.bot.send_message(message.from_user.id,
                                                       text=const.IN_THE_END,
                                                       reply_markup=estimate())  # noqa
            cache = get_redis()
            await cache.set(message.from_user.id, to_delete.message_id)
            origin = photo.file_id
            result = r.photo[-1].file_id
            await admin_notify(message, origin, result)
    except Exception as ex:
        logger.error(ex)


async def admin_notify(message: types.Message,
                       origin: str,
                       result: str
                       ):
    media = types.MediaGroup()
    text = f'username: {message.from_user.username}; user_id: {message.from_user.id}'  # noqa
    media.attach_photo(origin, text)
    media.attach_photo(result)
    await message.bot.send_media_group(chat_id=const.ADMIN_GROUP,
                                       media=media)


async def del_msg(message: types.Message):
    try:
        cache = get_redis()
        to_delete = await cache.get(message.from_user.id)
        to_delete = int(to_delete.decode('utf-8'))
        await message.bot.delete_message(message.from_user.id,
                                         to_delete)
    except Exception as ex:
        logger.error(ex)


async def sub_check(message: types.Message, sub_id: int) -> bool:
    try:
        status = await message.bot.get_chat_member(int(sub_id),
                                                    message.from_user.id)  # noqa
        if status["status"] != 'left':
            return True
        return False
    except Exception as ex:
        logger.error(ex)


async def sub_bot(message: types.Message, sub: dict, blur: str) -> None:
    if sub['token']:
        bot = Bot(sub['token'], parse_mode='HTML')
        try:
            msg: types.Message = await bot.send_message(message.from_user.id, text='👋👋👋')  # noqa
            await bot.delete_message(message.from_user.id, msg.message_id)  # noqa
            is_sub = True
        except Exception as ex:
            logger.info(ex)
            is_sub = False
            keyboard = await subscribe(sub['name'], sub['group_url']),  # noqa
            msg_sub = await message.bot.send_photo(message.from_user.id,  # noqa
                            photo=types.InputFile(blur),  # noqa
                            caption=const.SUB_TEXT,  # noqa
                            reply_markup=keyboard)  # noqa
            while not is_sub:
                try:
                    msg = await bot.send_message(message.from_user.id, text='👋👋👋')  # noqa
                    await bot.delete_message(message.from_user.id, msg.message_id)  # noqa
                    is_sub = True
                    await bot.delete_message(message.from_user.id, msg_sub.message_id)  # noqa
                except Exception as ex:
                    logger.info(ex)
                    await asyncio.sleep(1)
        return True
    return True


async def to_sub(message: types.Message, sublist: list) -> int:
    photo = await message.bot.get_file(message.photo[-1].file_id)  # noqa
    photo_url = await photo.get_url()
    blur = await blur_it(photo_url, message.from_user.id)

    one = [r for r in sublist if r['type'] == 'chat']
    two = [r for r in sublist if r['type'] == 'channel']
    three = [r for r in sublist if r['type'] == 'bot']

    if one and two and not three:
        sublist = [result for x in zip(one, two) for result in x]
    if one and two and three:
        sublist = [result for x in zip(one, two, three) for result in x]  # noqa

    amount = 0
    for sub in sublist:
        amount += 1
        if sub['type'] == 'bot':
            r = await sub_bot(message, sub, blur)
            if r:
                continue
        else:
            if not await sub_check(message, sub['group_id']):
                keyboard = await subscribe(sub['name'], sub['group_url'])  # noqa
                msg_sub = await message.bot.send_photo(message.from_user.id,  # noqa
                                                    photo=types.InputFile(blur),  # noqa
                                                    caption=const.SUB_TEXT,  # noqa
                                                    reply_markup=keyboard)  # noqa
                is_sub = False

                while not is_sub:
                    is_sub = await sub_check(message, sub['group_id'])
                    if is_sub:
                        await action_.user_sub(message, sub['group_id'])  # noqa
                        await message.bot.delete_message(message.from_user.id, msg_sub.message_id)  # noqa
                    await asyncio.sleep(1)
    return amount
