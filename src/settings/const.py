import os
from dotenv import load_dotenv

load_dotenv()

# DB:
DEFAULT_TOKENS = 10
POSTGRES_DSN = os.getenv('POSTGRES_DSN')

# BOT:
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = 'TeleCharacterAI'
ADMIN_ID = -4095118494
ADMIN_GROUP = -1002104627479
WELCOME = '🔞📸 Привет!\n\nС помощью этого бота ты сможешь раздеть любую девушку. Чтобы начать, отправь мне ее фото, где четко видно ее лицо\n\nОтправляя фото, вы принимаете пользовательское соглашение гипперссылка на пользовательское соглашение - https://telegra.ph/Polzovatelskoe-soglashenie-08-25-6'  # noqa
INVITE_FRIEND = 'Нашел бота, который может раздеть любую девушку 😳\n\nПо моей ссылке получишь 10 бесплатных фоток 👉🏻'  # noqa
END = '🔞📸 У тебя закончились все бесплатные попытки на сегодня.\n\n👇🏻 Нажми на кнопку ниже, чтобы пригласить друга и получишь +10 попыток как только твой друг создаст хоть одно фото в этом боте!'  # noqa
GOT_TOKEN = f'🔞📸 Ура! Тебе зачислены +{DEFAULT_TOKENS} попыток.\n\nЖду от тебя фото 😉'  # noqa
CONG = '🔞📸 Телеграм бот, который разденет твою подругу за 15 секунд'
TOO_MUCH = '❌ Отправляй по одной фотке за раз, пожалуйста.'
STICKER_ID = 'CAACAgIAAxkBAALVtWTmObbto5xMq3bIpP4-WEB6EfeMAAI2MgACGn8oS_JRDDF-gq41MAQ'  # noqa

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

# STABLE
headers_stable = {
  'Content-Type': 'application/json'
}
req_url = 'https://stablediffusionapi.com/api/v3/inpaint'
fetch_url = 'https://stablediffusionapi.com/api/v4/dreambooth/fetch'


body = {
  'key': os.environ.get('STABLE_KEY'),
  'prompt': 'nudify, nude photo of a naked woman, beautiful breast, seductive, flirting',  # noqa
  'negative_prompt': None,
  'init_image': '',
  'mask_image': '',
  'width': '',
  'height': '',
  'samples': '1',
  'num_inference_steps': '30',
  'safety_checker': 'no',
  'enhance_prompt': 'no',
  'guidance_scale': 7.5,
  'strength': 0.8,
  'seed': 3090185627,
  'webhook': None,
  'track_id': None
}
