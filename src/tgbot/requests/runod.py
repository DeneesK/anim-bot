import asyncio
import json
import io
import base64

from aiohttp import ClientSession
from aiogram import types

from src.settings import const
from src.settings.logger import logging


logger = logging.getLogger(__name__)


async def request_processing(photo: str) -> types.InputFile:
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
            'service': 'runpod',
            'body': {
                'version': const.inpaint_ver,
                'input': {
                    'image': photo,
                    'negative_prompt': const.negative_prompt,
                    'strength': 0.65,
                    'num_inference_steps': 61
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
                      'version': const.inpaint_ver,
                      'id': status_id
                    }
            }
    await asyncio.sleep(1)
    async with ClientSession() as session:
        response = await session.post(const.API_GATEWAY_URL,
                                      headers=headers,
                                      data=json.dumps(data))

        body = await response.json()
        logger.info(body)
        status = body.get('status')

    while status != 'COMPLETED' or status != 'FAILED':
        await asyncio.sleep(1)
        async with ClientSession() as session:
            response = await session.post(const.API_GATEWAY_URL,
                                          headers=headers,
                                          data=json.dumps(data))

            body = await response.json()
        status = body.get('status')

        logger.info(f'STATUS ------> {status}')

        if status == 'COMPLETED' or status == 'FAILED':
            break

    if status == 'FAILED':
        return await request_processing(photo)
    if status == 'COMPLETED':
        output = body.get('output')
        image_data = output[len("data:image/png;base64,"):]  # 23
    try:
        image_bytes = base64.b64decode(image_data)
        image_io = io.BytesIO(image_bytes)
        photo = types.InputFile(image_io)
    except Exception as ex:
        logger.error(ex)
        return None
    return photo
