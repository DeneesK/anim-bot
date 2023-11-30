import random

import aiohttp
import aiofiles

from src.settings.logger import logging


logger = logging.getLogger(__name__)


async def download(url: str, name: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(
                    f'img/{str(name)+str(random.randint(0, 100))}.jpeg',
                    mode='wb'
                    )
                await f.write(await resp.read())
                await f.close()
    return f'img/{name}.jpeg'
