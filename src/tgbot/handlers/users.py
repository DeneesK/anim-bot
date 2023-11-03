from aiogram import types


async def registration(message: types.Message):
    try:
        new_user = db.add_user(message.from_user.id,
                               message.from_user.username,
                               message.from_user.first_name,
                               message.from_user.last_name)
        if new_user:
            await amplitude_registration(message)
        return new_user
    except Exception as error:
        text_error = f'Ошибка при регистрации {message.from_user.id}:\n' \
                     f' >>> {error}'
        await amplitude_error(message, text_error)
        return False
