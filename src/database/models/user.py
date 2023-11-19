from datetime import datetime

from sqlalchemy import Column, String, DateTime, BigInteger

from ...database.db import Base
from src.settings.const import DEFAULT_TOKENS


class User(Base):
    __tablename__ = 'user_baby_pic'

    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(length=255), unique=True)
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    created_at = Column(DateTime, default=datetime.now)
    tokens = Column(BigInteger, default=DEFAULT_TOKENS)
    invites = Column(BigInteger, default=0)

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return "User(telegram_id='%s', username='%s)" % (self.user_id,
                                                         self.username)
