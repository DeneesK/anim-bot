import os
from dotenv import load_dotenv

load_dotenv()

# BOT:
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 775221255

# DB:
DEFAULT_TOKENS = 1
POSTGRES_DSN = os.getenv('POSTGRES_DSN')


# AMPLITUDE:
AMPLITUDE_KEY = os.getenv('AMPLITUDE_KEY')
AMPLITUDE_PLATFORM = os.getenv('AMPLITUDE_PLATFORM')
EVENTS = {}

# Replicate:
rep_url = 'https://api.replicate.com/v1/predictions'
rep_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + os.environ.get('REPLICATE_TOKEN')
}
body = {
    'version':
    'aca001c8b137114d5e594c68f7084ae6d82f364758aab8d997b233e8ef3c4d93',
    'input':
        {
            'mask': '',
            'image': '',
            'prompt': 'undress, do naked',
            'guidance_scale': 7.5,
            'negative_prompt': '',
            'prompt_strength': 0.8,
            'num_inference_steps': 50
            }
}
