import textwrap
from datetime import datetime, timedelta
from typing import Callable
from urllib.parse import urlsplit

import pytz
from telegram import Message
from telegram.error import Forbidden
from telegram.ext import ExtBot

from app.constants import APP_TYPE, TZ
from app.models import Job


def is_after_last_request(date: str) -> bool:
    now: datetime = datetime.now(TZ)
    utc: datetime = now.astimezone(pytz.utc)
    utc = utc.replace(minute=0, second=0, microsecond=0, tzinfo=None)

    iso: datetime = datetime.fromisoformat(date[:-1])
    iso = iso.replace(minute=0, second=0, microsecond=0, tzinfo=None)

    days_before = 3 if now.isoweekday() == 1 else 1
    match now.hour:
        case _ if 10 <= now.hour < 18:
            return iso >= utc - timedelta(days_before) + timedelta(hours=8)
        case _ if now.hour >= 18 or now.hour < 10:
            return iso >= utc - timedelta(hours=8)
        case _:
            return False


def iso_to_br_datetime(date: str) -> str:
    iso = datetime.fromisoformat(date.replace('Z', '+00:00')).astimezone(pytz.utc)

    return iso.astimezone(TZ).strftime('%d/%m/%Y %H:%M:%S')


def text_format(text: str):
    return textwrap.dedent(text)


async def send_message_reply(msg: Message, text: str):
    await msg.reply_markdown(text_format(text), False)


def get_job_url(*, id: int, url: str):
    split_result = urlsplit(url)
    source_query = split_result.query.split('=')[0]
    _url = f'{split_result.scheme}://{split_result.netloc}'

    return f'{_url}/jobs/{id}?{source_query}=https://t.me/api_vagas_bot'


def formatted_job_message(job: Job):
    rep: Callable[[str], str] = lambda to_replace: '_'.join(to_replace.split())
    job_names = [f'`{rep(key)}`' for key in sorted(job.keywords)]

    return text_format(
        f"""

        *Título da Vaga*: _{job.name}_

        *Encontrada para*: {' • '.join(job_names)}

        *Publicada em*: `{iso_to_br_datetime(job.published_date)}`

        *Company*: [{job.career_page_name}]({job.career_page_url})

        [CADASTRE-SE]({get_job_url(id=job.id,url=job.job_url)})
        """
    )


async def send_job_messages(app: APP_TYPE, bot: ExtBot[None], id: int, text: str):
    try:
        await bot.send_message(id, text, disable_web_page_preview=True)
    except Forbidden as exc:
        if 'bot was blocked by the user' in exc.message.lower():
            app.drop_chat_data(id)
            app.drop_user_data(id)
            raise Forbidden(exc.message) from exc
