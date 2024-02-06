import logging

import telegram
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

MARKDOWN = ParseMode.MARKDOWN


async def start(
    update: telegram.Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Initial Messages and Commands

    Args:
        update (telegram.Update)
        context (ContextTypes.DEFAULT_TYPE)
    """
    if update.effective_chat:
        chat_id: int = update.effective_chat.id
        message: telegram.Message | None = update.message
        user_name: str = (
            f', *{message.from_user.first_name}*'
            if message and message.from_user
            else ''
        )

        text = f'Olá{user_name}! Bem vindo ao Bot de busca de empregos.\n\n'
        text += f'*Criado Por*: {settings.EnvVars.MARKDOWN_DEV_LINK}\n'

        keyboard = [[telegram.KeyboardButton('/cadastrar')]]
        keyboard += [[telegram.KeyboardButton('/remover')]]
        keyboard += [[telegram.KeyboardButton('/limpar')]]
        reply_markup = telegram.ReplyKeyboardMarkup(
            keyboard, True, True, is_persistent=True
        )
        await context.bot.send_message(
            chat_id, text, MARKDOWN, reply_markup=reply_markup
        )


def main() -> None:
    app = ApplicationBuilder().token(settings.EnvVars.TOKEN).build()
    start_handler = CommandHandler('start', start)
    app.add_handler(start_handler)

    app.run_polling()


if __name__ == '__main__':
    main()
