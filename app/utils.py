from datetime import datetime, timedelta

import pytz
from telegram import Message

from app.constants import TZ


def is_after_last_request(date: str) -> bool:
    now: datetime = datetime.now(TZ)
    utc: datetime = now.astimezone(pytz.utc)
    utc = utc.replace(minute=0, second=0, microsecond=0, tzinfo=None)

    iso: datetime = datetime.fromisoformat(date[:-1])
    iso = iso.replace(minute=0, second=0, microsecond=0, tzinfo=None)

    boolean: bool = False
    match now.hour:
        case _ if 10 <= now.hour < 18:
            boolean = iso >= utc - timedelta(days=1) + timedelta(hours=8)
        case _ if now.hour >= 18 or now.hour < 10:
            boolean = iso >= utc - timedelta(hours=8)

    return boolean


def iso_to_br_datetime(date: str) -> str:
    iso = datetime.fromisoformat(date.replace('Z', '+00:00')).astimezone(pytz.utc)

    return iso.astimezone(TZ).strftime('%d/%m/%Y %H:%M:%S')


async def send_message_reply(msg: Message, text: str):
    await msg.reply_markdown(text, False)
