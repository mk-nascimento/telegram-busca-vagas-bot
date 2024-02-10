from datetime import datetime, timedelta

import pytz

BR_UTC: str = next(time for time in pytz.all_timezones if 'Sao_Paulo' in time)
BR_TIMEZONE = pytz.timezone(BR_UTC)


def is_after_last_request(date: str) -> bool:

    now: datetime = datetime.now(BR_TIMEZONE)
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
