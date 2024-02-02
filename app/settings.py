from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Settings:
    TOKEN = getenv('TELEGRAM_BOT_TOKEN', '')
    API_URL = getenv('API_URL', 'https://example.com/')
