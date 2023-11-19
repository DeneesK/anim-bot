from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.settings.logger import logging


logger = logging.getLogger(__name__)


Base = declarative_base()

async_session: AsyncSession | None = None


async def get_session() -> AsyncSession:
    return async_session


async def setup(dns: str):
    try:
        engine = create_async_engine(dns, echo=False, future=True)
        session = sessionmaker(engine,
                               class_=AsyncSession,
                               expire_on_commit=False)
    except Exception as ex:
        logger.error(ex)
        return
    return session
