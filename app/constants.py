from datetime import time
from typing import Any, Dict

import pytz
from telegram.ext import Application, CallbackContext, ExtBot, JobQueue

ADict = Dict[Any, Any]
AppType = Application[ExtBot[None], CallbackContext, ADict, ADict, ADict, JobQueue]


# List of bot commands with descriptions.
COMMANDS: list[tuple[str, str]] = [
    ('listar', 'Este comando LISTA todas as "palavras-chave" já cadastradas'),
    ('cadastrar', 'Este comando ADICIONA uma "palavra-chave" especificada'),
    ('remover', 'Este comando REMOVE a "palavra-chave" especificada'),
    ('limpar', 'Este comando REMOVE todas as "palavras-chave" cadastradas'),
]


# Find the Brazil time zone and set it to `TZ`.
BR_UTC: str = next(time for time in pytz.all_timezones if 'Sao_Paulo' in time)
TZ = pytz.timezone(BR_UTC)


# 10 AM and 6 PM in Brasilia time zone.
FIRST_REQ, SECOND_REQ = time(10, tzinfo=TZ), time(18, tzinfo=TZ)
# Define the days for requests, considering Monday to Friday.
WORKDAYS = tuple(range(1, 6))
