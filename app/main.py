import logging

from telegram import LinkPreviewOptions
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder as App
from telegram.ext import CommandHandler, Defaults, MessageHandler, PicklePersistence
from telegram.ext.filters import ALL

from app import handlers, settings
from app.constants import COMMANDS, FIRST_REQ, SECOND_REQ, TZ, WORKDAYS, AppType

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger(__name__)


async def post_init(app: AppType):
    """Perform post-initialization tasks for the application.

    Parameters:
    app (Application[ExtBot[None], CallbackContext, ADict, ADict, ADict, JobQueue]): `PTB Application object`

    Returns:
    None: no returns
    """

    assert app.job_queue

    for id in app.chat_data.keys():
        try:
            await app.bot.get_chat(id)
        except Exception:
            app.drop_chat_data(id)
            continue

        run = lambda q, cb, time, id: q.run_daily(cb, time, WORKDAYS, chat_id=id)
        [run(app.job_queue, handlers.search, T, id) for T in [FIRST_REQ, SECOND_REQ]]

    await app.bot.set_my_commands(COMMANDS)


def main():
    PERSISTENCE = PicklePersistence('app/PERSISTENCE')
    LPO = LinkPreviewOptions(False, prefer_small_media=True, show_above_text=True)
    DEFAULTS = Defaults(ParseMode.MARKDOWN, link_preview_options=LPO, tzinfo=TZ)
    APP: AppType = (
        App()
        .token(settings.EnvVars.TOKEN)
        .persistence(PERSISTENCE)
        .defaults(DEFAULTS)
        .post_init(post_init)
        .build()
    )

    APP.add_handler(CommandHandler('start', handlers.start))
    APP.add_handler(CommandHandler('cadastrar', handlers.add))
    APP.add_handler(CommandHandler('remover', handlers.remove))
    APP.add_handler(CommandHandler('listar', handlers.keywords_list))
    APP.add_handler(CommandHandler('limpar', handlers.clear))
    APP.add_handler(MessageHandler(ALL, handlers.unknown))

    APP.run_polling()


if __name__ == '__main__':
    main()
