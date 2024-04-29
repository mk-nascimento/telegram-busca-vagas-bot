import html
import json
import logging
import traceback

import telegram
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app import settings
from app.utils import text_format

logger = logging.getLogger(__name__)


async def handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer.

    Parameters:
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert context.error
    err = context.error
    logger.error('Exception while handling an update:', exc_info=err)

    tb_list = traceback.format_exception(None, err, err.__traceback__)
    tb_string = ''.join(tb_list)

    upd = update.to_dict() if isinstance(update, telegram.Update) else str(update)
    text = text_format(
        f"""
        <code>An exception was raised while handling an update</code>
        <pre>update = {html.escape(json.dumps(upd, indent=2, ensure_ascii=False))}</pre>
        
        <pre>{html.escape(tb_string)}</pre>"""
    )

    await context.bot.send_message(settings.EnvVars.DEV_ID, text, ParseMode.HTML)
