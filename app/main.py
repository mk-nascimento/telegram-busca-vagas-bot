import logging

from telegram import LinkPreviewOptions
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder as App
from telegram.ext import CommandHandler, Defaults, MessageHandler, PicklePersistence
from telegram.ext.filters import ALL

from app import error_handler, handlers, settings
from app.constants import APP_TYPE, COMMANDS, TIME_REQUESTS, TZ, WORKDAYS

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger(__name__)


async def post_init(app: APP_TYPE):
    """Perform post-initialization tasks for the application.

    Parameters:
    .. (Application[ExtBot[None], CallbackContext, ADict, ADict, ADict, JobQueue])::
        `PTB Application object`

    Returns:
    None: no returns
    """

    assert app.job_queue

    drops: set[int] = set()
    for id in app.chat_data.keys():
        try:
            await app.bot.get_chat(id)
            keys = app.chat_data[id].get('keywords')
        except Exception:
            drops.add(id)
            continue

        drops.add(id) if not keys else None
        run = lambda q, cb, time, id: q.run_daily(cb, time, WORKDAYS, chat_id=id)
        [run(app.job_queue, handlers.search, T, id) for T in TIME_REQUESTS if keys]

    [(app.drop_chat_data(id), app.drop_user_data(id)) for id in drops]
    await app.bot.set_my_commands(COMMANDS)


def main():
    PERSISTENCE = PicklePersistence('app/PERSISTENCE')
    LPO = LinkPreviewOptions(False, prefer_small_media=True, show_above_text=True)
    DEFAULTS = Defaults(ParseMode.MARKDOWN, link_preview_options=LPO, tzinfo=TZ)
    APP: APP_TYPE = (
        App()
        .defaults(DEFAULTS)
        .persistence(PERSISTENCE)
        .post_init(post_init)
        .token(settings.EnvVars.TOKEN)
        .build()
    )

    APP.add_handler(CommandHandler('start', handlers.start))
    APP.add_handler(CommandHandler('cadastrar', handlers.add))
    APP.add_handler(CommandHandler('remover', handlers.remove))
    APP.add_handler(CommandHandler('listar', handlers.keywords_list))
    APP.add_handler(CommandHandler('limpar', handlers.clear))
    APP.add_handler(MessageHandler(ALL, handlers.unknown))

    APP.add_error_handler(error_handler.handler)

    APP.run_polling()


if __name__ == '__main__':
    main()
