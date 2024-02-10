import logging

from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder as App
from telegram.ext import (
    CommandHandler,
    Defaults,
    MessageHandler,
    PicklePersistence,
    filters,
)

from app import handlers, settings
from app.utils import BR_TIMEZONE

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TOKEN = settings.EnvVars.TOKEN
PERSISTENCE_FILE = settings.EnvVars.PERSISTENCE


def main():
    persistence = PicklePersistence(PERSISTENCE_FILE)
    defaults = Defaults(ParseMode.MARKDOWN, False, False, None, BR_TIMEZONE)
    app = App().token(TOKEN).persistence(persistence).defaults(defaults).build()

    app.add_handler(CommandHandler('start', handlers.start))
    app.add_handler(CommandHandler('cadastrar', handlers.add))
    app.add_handler(CommandHandler('remover', handlers.remove))
    app.add_handler(CommandHandler('limpar', handlers.clear))
    app.add_handler(MessageHandler(filters.ALL, handlers.unknown))

    app.run_polling()


if __name__ == '__main__':
    main()
