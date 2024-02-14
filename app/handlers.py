import logging

import telegram
from telegram.ext import ContextTypes

from app import api_integration, settings
from app.constants import FIRST_REQ, SECOND_REQ, WORKDAYS
from app.utils import send_message_reply

logger = logging.getLogger(__name__)


async def start(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initial Messages and Commands

    Parameters:
    update (telegram.Update): `PTB Update object`
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert update.message
    chat_id, from_user = update.message.chat_id, update.message.from_user
    user_name: str = f', _{from_user.first_name}_' if from_user else ''

    text = (
        f'Olá{user_name}! Bem vindo ao Bot de busca de empregos.\n\n'
        f'*Criado Por*: {settings.EnvVars.MARKDOWN_DEV_LINK}\n\n'
        '_este bot utiliza o_ [Portal de Vagas da Gupy](https://portal.gupy.io/)\n'
    )

    await context.bot.send_message(chat_id, text)


async def search(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Searches for jobs based on the provided keyword list.

    Parameters:
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert context.job
    api = api_integration.RequestAPI(settings.EnvVars.API_URL)
    chat_id, name = int(context.job.chat_id or 000000000), str(context.job.name)

    jobs = await api.search_jobs(name)
    if not jobs:
        text = f'Não foram encontradas novas vagas para `{name.upper()}`'
        await context.bot.send_message(chat_id, text)

    keyword = '_'.join(name.split()).replace('_', r'\_')
    for job in jobs:
        text = (
            f'#{keyword}\n\n'
            f'*Título da Vaga*: _{job["name"]}_\n\n'
            f'*Company*: [{job["careerPageName"]}]({job["careerPageUrl"]})\n\n'
            f'[CADASTRE-SE]({job["jobUrl"]})'
        )
        await context.bot.send_message(chat_id, text, disable_web_page_preview=False)


async def add(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command to add new keyword to search

    Parameters:
    update (telegram.Update): `PTB Update object`
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert context.chat_data is not None and context.application.job_queue
    assert update.message
    chat_data, queue = context.chat_data, context.application.job_queue
    chat_id, message = update.message.chat_id, update.message
    value = str(message.text).partition(' ')[2]

    if value:
        keywords: set[str] = chat_data.setdefault('keywords', set())
        keywords_len: int = len(keywords)
        value = value.strip()

        if keywords_len == 10:
            text = (
                f'Máximo de palavras-chave ({keywords_len}) já cadastrado!\n'
                'remova uma ou mais palavras-chave para poder adicionar novas\n\n'
                f'*ex*: `/remover {list(keywords)[0]}`'
            )

            await send_message_reply(message, text)
        elif value in keywords:
            await send_message_reply(message, f'{value.upper()} já está cadastrada!')
        else:
            keywords.add(value.lower())

            text = (
                f'Busca cadastrada com sucesso para `{value.upper()}`!\n\n'
                f'Uma agenda de busca para `{value.upper()}` foi configurada'
            )
            await send_message_reply(message, text)
            [
                queue.run_daily(search, R, WORKDAYS, None, value, chat_id)
                for R in [FIRST_REQ, SECOND_REQ]
            ]
    else:
        text = (
            'Valor para busca não fornecido.\n'
            'Envie `/cadastrar + sua busca` para cadastrar um nova busca\n\n'
            '*ex*: `/cadastrar python`.'
        )
        await send_message_reply(message, text)


async def remove(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command to remove a keyword to search

    Parameters:
    update (telegram.Update): `PTB Update object`
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert context.chat_data is not None and context.job_queue
    assert update.message
    chat_data, queue, message = context.chat_data, context.job_queue, update.message
    keywords: set[str] = chat_data.setdefault('keywords', set())
    value = str(message.text).partition(' ')[2]

    if value:
        try:
            keywords.remove(value.strip().lower())
            await send_message_reply(message, f'`{value.upper()}` removido!')
            queues = queue.get_jobs_by_name(value)
            [q.schedule_removal() for q in queues]
        except KeyError:
            text = (
                f'`{value.upper()}` não consta em suas buscas!\n'
                'Use `/listar` para verificar as buscas cadastradas.'
            )

            await send_message_reply(message, text)
    else:
        text = (
            'Valor para remoção não fornecido.\n'
            'Envie `/remover + sua busca` para remover um busca\n\n'
            '*ex*: `/remover python`.'
        )

        await send_message_reply(message, text)


async def keywords_list(
    update: telegram.Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """List available keywords.

    Parameters:
    update (telegram.Update): `PTB Update object`
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert context.chat_data is not None and update.message
    chat_data, message = context.chat_data, update.message
    keywords: set[str] = chat_data.setdefault('keywords', set())

    if not keywords:
        text = (
            'Não há buscas cadastradas!\n'
            'Para cadastrar novas buscas digite `/cadastrar`.'
        )
        await send_message_reply(message, text)
    else:
        text = '\n'.join(f'•\t{k.upper()}' for k in keywords)
        await send_message_reply(message, text)


async def clear(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command to clear keyword list

    Parameters:
    update (telegram.Update): `PTB Update object`
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert context.chat_data is not None and context.job_queue
    assert update.message
    app, chat_data, queue = context.application, context.chat_data, context.job_queue
    message = update.message
    keywords: set[str] = chat_data.setdefault('keywords', set())

    if not keywords:
        text = (
            'Não há buscas cadastradas!\n'
            'Para cadastrar novas buscas digite `/cadastrar`.'
        )
        await send_message_reply(message, text)
    else:
        app.drop_chat_data(message.chat_id)
        [q.schedule_removal() for q in queue.jobs()]
        text = (
            'Sua lista de buscas foi limpa!\n'
            'Para cadastrar novas buscas digite `/cadastrar`.'
        )

        await send_message_reply(message, text)


async def unknown(update: telegram.Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle with unknown commands

    Parameters:
    update (telegram.Update): `PTB Update object`
    _ (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """
    assert update.message

    text = (
        'Este comando não é válido.\n'
        'Clique no ícone do `☰ Menu` para ver os comandos disponíveis\n'
        'Ou digite `/` para sugestão automática'
    )
    await send_message_reply(update.message, text)
