from uuid import uuid1

from src.settings import const


def organic_url(inv_user_id: int) -> str:
    payload = str(uuid1())[:4]
    return f'https://t.me/{const.BOT_NAME}?start=organic_{payload}_{inv_user_id}' # noqa


def ref_url(inv_user_id: int) -> str:
    return f'https://t.me/{const.BOT_NAME}?start=ref__{inv_user_id}'
