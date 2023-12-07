from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update
from sqlalchemy.sql import text

from .models.user import User
from src.settings.logger import logging


logger = logging.getLogger(__name__)


class PsgDB:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_user(self, data: Message) -> User:
        try:
            async with self.session() as conn:
                new_user = User(user_id=data.from_user.id,
                                username=data.from_user.username,
                                first_name=data.from_user.first_name,
                                last_name=data.from_user.last_name)
                conn.add(new_user)
                await conn.commit()
                await conn.close()
        except SQLAlchemyError as ex:
            logger.error(ex)
        return new_user

    async def find_user(self, user_id: int) -> User | None:
        async with self.session() as conn:
            user = await conn.execute(
                select(User).where(User.user_id == user_id)
            )
            user = user.first()
        if user:
            return user[0]
        return None

    async def add_token(self, user_id: int, amount: int) -> None:
        async with self.session() as conn:
            await conn.execute(
                update(User).values(
                        tokens=User.tokens+amount
                        ).where(
                    User.user_id == user_id)
                    )
            await conn.commit()
            await conn.close()


class SubListDB:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_sublist(self) -> User | None:
        async with self.session() as conn:
            sub = await conn.execute(
                text("SELECT * FROM sublist")
            )
            sub = sub.mappings().all()
        if sub:
            print(sub)
            return sub
        return None
