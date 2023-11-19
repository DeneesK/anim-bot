from src.settings import const


def organic_url(inv_user_id: int) -> str:
    return f'https://t.me/{const.BOT_NAME}?start=organic_{inv_user_id}' # noqa


def ref_url(inv_user_id: int) -> str:
    return f'https://t.me/{const.BOT_NAME}?start=ref_{inv_user_id}'
