import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

AMPLITUDE_KEY = os.getenv('AMPLITUDE_KEY')
AMPLITUDE_PLATFORM = os.getenv('AMPLITUDE_PLATFORM')
