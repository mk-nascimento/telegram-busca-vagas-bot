from os import getenv

from dotenv import load_dotenv

load_dotenv()


class EnvVars:
    TOKEN = getenv('TELEGRAM_BOT_TOKEN', '')
    DEV_ID = int(getenv('DEVELOPER_CHAT_ID', 000000000))
    API_URL = getenv('API_URL', 'https://example.com/')
    MARKDOWN_DEV_LINK = getenv('MARKDOWN_DEV_LINK', '[ref](https://example.com/)')
