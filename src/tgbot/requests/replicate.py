import asyncio
import json

from aiohttp import ClientSession
from aiogram import types

from src.tgbot.analysis import actions  # noqa
from src.settings import const
from src.settings.logger import logging


logger = logging.getLogger(__name__)


async def request(image: str,
                  mask: str,
                  message: types.Message) -> dict:
    try:
        logger.info('REPLICATE STARTING....')
        # await actions.replicate_request(message)
        data = const.body
        data['input']['image'] = image
        data['input']['mask'] = mask
        async with ClientSession() as session:
            response = await session.post(const.rep_url,
                                          headers=const.rep_headers,
                                          data=json.dumps(data))
            body = await response.json()
            logger.info(body)
            response.close()
            id_ = body['id']

        if body['status'] != 'succeeded':
            while body['status'] != 'succeeded':
                await asyncio.sleep(1.5)
                if body.get('error', None):
                    return {}
                async with ClientSession() as session:
                    response = await session.get(const.rep_url+'/'+id_,
                                                 headers=const.rep_headers)
                    body = await response.json()
                    logger.info(body)
                    response.close()
        if body.get('error', None):
            return await request(image, mask, message)
    except Exception as ex:
        logger.error(ex)
    logger.debug(body)
    return body
