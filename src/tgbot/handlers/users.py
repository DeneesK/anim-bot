from aiogram import types

from src.tgbot.analysis import actions


async def registration(message: types.Message):
    try:
        new_user = True
        if new_user:
            await actions.amplitude_registration(message)
        return new_user
    except Exception as error:
        text_error = f'Ошибка при регистрации {message.from_user.id}:\n' \
                     f' >>> {error}'
        await actions.amplitude_error(message, text_error)
        return False


async def user_start(message: types.Message):
    await registration(message)
    await message.answer(text='Привет! Пришли фото')
