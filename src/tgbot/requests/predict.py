import os
import asyncio
import json
import time
import copy

from aiohttp import ClientSession
from aiogram import types

from src.tgbot.analysis import actions  # noqa
from src.settings import const
from src.settings.logger import logging


logger = logging.getLogger(__name__)


async def request(image: str,
                  mask: str,
                  message: types.Message) -> str | None:
    start = time.time()
    data = copy.deepcopy(const.body)
    data['init_image'] = image
    data['mask_image'] = mask
    async with ClientSession() as session:
        response = await session.post(const.req_url,
                                      headers=const.headers_stable,
                                      data=json.dumps(data))
        await actions.api_request(message)

        body = await response.json()
        logger.info(body)
        response.close()
    if body['status'] == 'processing':
        id_ = body['id']
        i = 30
        while body['status'] == 'processing' and i > 0:
            data = {'key': os.environ.get('STABLE_KEY'), 'request_id': id_}
            async with ClientSession() as session:
                response = await session.post(const.fetch_url,
                                              headers=const.headers_stable,
                                              data=json.dumps(data))
                body = await response.json()
                logger.info(body)
                response.close()
                await asyncio.sleep(3)
            i -= 1
    if body['status'] == 'error':  # noqa
        return await request(image, mask, message)
    if body['status'] == 'processing':
        return await request(image, mask, message)
    if body['status'] == 'failed':
        return await request(image, mask, message)
    logger.info(body)
    generation_time = body.get('generationTime', time.time() - start)
    await actions.api_resp(message, generation_time)

    result = body.get('output', [None])[0]
    return result
