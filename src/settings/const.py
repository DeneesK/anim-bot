import os
from dotenv import load_dotenv

load_dotenv()

# BOT:
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = 'TeleCharacterAI'
ADMIN_ID = 775221255
ADMIN_GROUP = 775221255
WELCOME = 'Привет! Пришли фото'
INVITE_FRIEND = 'Приглашаю'
END = 'Эх! Твои попытки закончились. Пригласи друга и получи еще попытку бесплатно. 👇🏻'  # noqa
GOT_TOKEN = 'По тввоей ссылке перешли и тебе зачисленв бесплатная попытка, отправь фото'  # noqa
CONG = 'Поздравляю вот твое фото\n\n'
STICKER_ID = 'CAACAgIAAxkBAALVtWTmObbto5xMq3bIpP4-WEB6EfeMAAI2MgACGn8oS_JRDDF-gq41MAQ'  # noqa

# DB:
DEFAULT_TOKENS = 1
POSTGRES_DSN = os.getenv('POSTGRES_DSN')


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
fetch_url = 'https://stablediffusionapi.com/api/v3/fetch/'


body = {
  'key': os.environ.get('STABLE_KEY'),
  'prompt': 'NUDIFY PERSON',
  'negative_prompt': None,
  'init_image': '',
  'mask_image': '',
  'width': '1024',
  'height': '1024',
  'samples': '1',
  'num_inference_steps': '30',
  'safety_checker': 'no',
  'enhance_prompt': 'yes',
  'guidance_scale': 7.5,
  'strength': 0.7,
  'seed': None,
  'webhook': None,
  'track_id': None
}
