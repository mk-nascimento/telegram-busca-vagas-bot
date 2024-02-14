import logging

from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder as App
from telegram.ext import CommandHandler, Defaults, MessageHandler, PicklePersistence
from telegram.ext.filters import ALL

from app import handlers, settings
from app.constants import COMMANDS, FIRST_REQ, SECOND_REQ, TZ, WORKDAYS, AppType

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def post_init(app: AppType):
    """Perform post-initialization tasks for the application.

    Parameters:
    app (Application[ExtBot[None], CallbackContext, ADict, ADict, ADict, JobQueue]): `PTB Application object`

    Returns:
    None: no returns
    """

    assert app.job_queue

    chats_to_delete: set[int] = set()
    for id in app.chat_data.keys():
        try:
            await app.bot.get_chat(id)
        except Exception as e:
            logger.error(f'{e=}')
            chats_to_delete.add(id)
            continue

        chat_data = app.chat_data[id]
        keywords: set[str] = chat_data.setdefault('keywords', set())

        [
            [
                app.job_queue.run_daily(handlers.search, TIME, WORKDAYS, None, key, id)
                for key in keywords
            ]
            for TIME in [FIRST_REQ, SECOND_REQ]
        ]

    [app.drop_chat_data(id) for id in chats_to_delete]
    await app.bot.set_my_commands(COMMANDS)


def main():
    persistence = PicklePersistence(settings.EnvVars.PERSISTENCE)
    defaults = Defaults(ParseMode.MARKDOWN, False, False, None, TZ)
    app: AppType = (
        App()
        .token(settings.EnvVars.TOKEN)
        .persistence(persistence)
        .defaults(defaults)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler('start', handlers.start))
    app.add_handler(CommandHandler('cadastrar', handlers.add))
    app.add_handler(CommandHandler('remover', handlers.remove))
    app.add_handler(CommandHandler('listar', handlers.keywords_list))
    app.add_handler(CommandHandler('limpar', handlers.clear))
    app.add_handler(MessageHandler(ALL, handlers.unknown))

    app.run_polling()


if __name__ == '__main__':
    main()
