import os

from redis import asyncio as aioredis
from dotenv import load_dotenv


load_dotenv()


cache: aioredis.Redis | None = None


async def setup():
    return aioredis.from_url(os.environ.get('REDIS_HOST'))


def get_redis() -> aioredis.Redis:
    return cache
