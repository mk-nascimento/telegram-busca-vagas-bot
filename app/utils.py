import textwrap
from datetime import datetime, timedelta
from typing import Callable

import pytz
from telegram import Message

from app.constants import TZ
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


def formatted_job_message(job: Job):
    rep: Callable[[str], str] = lambda to_replace: '_'.join(to_replace.split())
    job_names = [f'`{rep(key)}`' for key in sorted(job['keywords'])]

    return text_format(
        f"""

        *Título da Vaga*: _{job["name"]}_

        *Encontrada para*: {' • '.join(job_names)}

        *Publicada em*: `{iso_to_br_datetime(job['publishedDate'])}`

        *Company*: [{job["careerPageName"]}]({job["careerPageUrl"]})

        [CADASTRE-SE]({job["jobUrl"]})"""
    )
