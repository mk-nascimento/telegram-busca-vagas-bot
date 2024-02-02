import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.settings import Settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a start message."""
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text='Start Message'
        )


def main() -> None:
    app = ApplicationBuilder().token(Settings.TOKEN).build()

    start_handler = CommandHandler('start', start)
    app.add_handler(start_handler)

    app.run_polling()


if __name__ == '__main__':
    main()
