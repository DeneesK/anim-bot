import json
import io
import base64

from aiohttp import ClientSession
from aiogram import types

from src.settings import const
from src.settings.logger import logging


logger = logging.getLogger(__name__)


async def request(photo: str) -> types.InputFile:
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
            'service': 'runpod',
            'body': {
                'version': 'mulm1y2ddu4ehb',
                'input': {
                    'image': photo
                }
            }
    }
    async with ClientSession() as session:
        response = await session.post(const.API_GATEWAY_URL,
                                      headers=headers,
                                      data=json.dumps(data))
        body = await response.json()
        logger.info(body)
        response.close()

    status_id = body.get('id')

    data = {'service': 'runpod',
            'body': {
                      'version': 'mulm1y2ddu4ehb',
                      'id': status_id
                    }
            }

    async with ClientSession() as session:
        response = await session.post(const.API_GATEWAY_URL,
                                      headers=headers,
                                      data=json.dumps(data))

        body = await response.json()
        logger.info(body)
        status = body.get('status')

    while status != 'COMPLETED' or status != 'FAILED':
        async with ClientSession() as session:
            response = await session.post(const.API_GATEWAY_URL,
                                          headers=headers,
                                          data=json.dumps(data))

            body = await response.json()
            logger.info(body)
        status = body.get('status')

        logger.info(f'STATUS ------> {status}')

        if status == 'COMPLETED' or status == 'FAILED':
            break

    if status == 'FAILED':
        return await request(photo)
    if status == 'COMPLETED':
        image_bytes = body.get('output')
    try:
        image_bytes = base64.b64decode(image_bytes)
        image_io = io.BytesIO(image_bytes)
        photo = types.InputFile(image_io)
    except Exception as ex:
        logger.error(ex)
        return None
    return photo
