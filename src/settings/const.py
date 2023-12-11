import os

from dotenv import load_dotenv
from aiogram.utils.markdown import hlink

load_dotenv()

# DB:
DEFAULT_TOKENS = 5
POSTGRES_DSN = os.getenv('POSTGRES_DSN')

# BOT:
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = 'i2animebot'
ADMIN_ID = -4087102275
ADMIN_GROUP = -4087102275
APPLY = hlink('принимаете пользовательское соглашение', 'https://telegra.ph/Polzovatelskoe-soglashenie-08-25-6') # noqa
WELCOME = f'📸 Привет!\n\n Отправь фото!'  # noqa
INVITE_FRIEND = 'Нашел бота, который создаст аниме портрет\n\nПо моей ссылке получишь 10 бесплатных фоток 👉🏻'  # noqa
END = '🔞📸 У тебя закончились все бесплатные попытки на сегодня.\n\n👇🏻 Нажми на кнопку ниже, чтобы пригласить друга и получишь +10 попыток как только твой друг создаст хоть одно фото в этом боте!'  # noqa
GOT_TOKEN = f'📸 Ура! Тебе зачислены +{DEFAULT_TOKENS} попыток.\n\nЖду от тебя фото 😉'  # noqa
CONG = '📸 Телеграм бот, который создаст аниме портрет за 15 секунд'
TOO_MUCH = '❌ Отправляй по одной фотке за раз, пожалуйста.'
STICKER_ID = 'CAACAgQAAxkBAAECTx5lcB3ZVZXSSE_CuRFNKuo8V48vhgAC_g8AAlxuMVMBfH8BURLP7zME'  # noqa
NEW_ONE = 'Отправь мне новое свое фото, где четко видно лицо'
IN_THE_END = 'Оцени качество фото 👇🏻'
THE_END = 'Жду от тебя следующее фото!'
SUB_TEXT = 'Фото готовво! Осталось лишь подписаться, чтобы получить фото 😈!\n\n⬇️⬇️⬇️'  # noqa
ONE_MORE = 'Жду от тебя следующее фото!'

BUTTON_ONEMORE = 'Создать еще'
BUTTON_NEWONE = 'Отправить новое фото'

# AMPLITUDE:
AMPLITUDE_KEY = os.getenv('AMPLITUDE_KEY')
AMPLITUDE_PLATFORM = os.getenv('AMPLITUDE_PLATFORM')
EVENTS = {
    'start': 'User sent /start',
    'singup': 'User registered and saved to db',
    'ref_reg': 'referral registration',
    'organic_reg': 'organic registration',
    'save_to_db': 'User registered and saved to db',
    'reg_error': 'Registration error',
    'req_': 'Photo sent to  API',
    'resp_': 'Successful generation through API',
    'sent_to_admin': 'Result sent to admin',
    'sent_result': 'Result sent to user',
    'no_tries': 'User has no tries left',
    'invite': 'User invited a new user',
    'wrong_invite': 'User invited existing use',
    'wrong_cont': 'User sent wrong content type'
}

# AWS:
API_GATEWAY_URL = os.environ.get('API_GATEWAY_URL')

# Runpod
prompt = 'A photo of a person, (anime style, colourful), cartoon'
negative_prompt = '((3D)), render, ((watercolour, blurry)), ((((ugly)))), (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), (fused fingers), (too many fingers), (((long neck))), (fat, obese, overweight, plump)'  # noqa
inpaint_ver = 'w7se8q0ntroudg'
