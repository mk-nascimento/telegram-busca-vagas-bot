from os import getenv

from dotenv import load_dotenv

load_dotenv()


class EnvVars:
    TOKEN = getenv('TELEGRAM_BOT_TOKEN', '')
    API_URL = getenv('API_URL', 'https://example.com/')
    MARKDOWN_DEV_LINK = getenv('MARKDOWN_DEV_LINK', '[ref](https://example.com/)')
    PERSISTENCE = getenv('PERSISTENCE', 'chat_persistence')
