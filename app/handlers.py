import logging
from collections import defaultdict

import telegram
from telegram.ext import ContextTypes

from app import api_integration, settings
from app.utils import formatted_job_message, send_message_reply

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
    from_user, message = update.message.from_user, update.message
    user_name: str = f', _{from_user.first_name}_' if from_user else ''

    text = f"""
        Olá{user_name}! Bem vindo ao Bot de busca de empregos.

        _este bot utiliza o_ [_Portal de Vagas da Gupy_](https://portal.gupy.io/)
        Clique no ícone do `☰ Menu` para ver os comandos disponíveis
        Ou digite `/` para sugestão automática

        *Criado Por*: {settings.EnvVars.MARKDOWN_DEV_LINK}"""

    await send_message_reply(message, text)


async def search(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Searches for jobs based on the provided keyword list.

    Parameters:
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert context.chat_data and context.job
    api = api_integration.RequestAPI(settings.EnvVars.API_URL)
    chat_data, chat_id = context.chat_data, int(context.job.chat_id or 000000000)
    keywords: set[str] = chat_data.setdefault('keywords', set())

    line, no_results, split = '\n', set(), defaultdict(list)

    for job_name in keywords:
        jobs = await api.search_jobs(job_name)
        for job in jobs:
            found_on: list[str] = job.setdefault('keywords', list())
            work = 'workplaceType'

            ids = {item['id'] for item in split[job[work]]}
            if job['id'] not in ids:
                found_on.append(job_name)
                split[job[work]].append(job)
            else:
                job = next((o for o in split[job[work]] if o['id'] == job['id']), {})
                job['keywords'].append(job_name)

        if not jobs:
            no_results.add(job_name)

    for work in split.keys():
        rep = lambda to_replace: to_replace.replace(' ', '_')
        formatted_jobs = [formatted_job_message(job) for job in split[work]]
        group_by = {'hybrid': 'vagas híbridas', 'remote': 'vagas remotas'}
        text = f'*#{rep(group_by[work].upper())}* {"".join(formatted_jobs)}'

        await context.bot.send_message(chat_id, text, disable_web_page_preview=True)

    if no_results:
        text = 'Não foram encontradas novas vagas para:***'
        text += f'`{line.join(f"• {n.upper()}" for n in no_results)}`'
        await context.bot.send_message(chat_id, text.replace('***', line * 2))


async def add(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command to add new keyword to search

    Parameters:
    update (telegram.Update): `PTB Update object`
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert context.chat_data is not None and update.message
    chat_data, message = context.chat_data, update.message
    value = str(message.text).partition(' ')[2]

    if value:
        keywords: set[str] = chat_data.setdefault('keywords', set())
        keywords_len: int = len(keywords)
        value = value.strip()

        if keywords_len == 15:
            text = f"""
                Máximo de palavras-chave ({keywords_len}) já cadastrado!
                remova uma ou mais palavras-chave para poder adicionar novas

                *ex*: `/remover {list(keywords)[0]}`"""

            await send_message_reply(message, text)
        elif value in keywords:
            await send_message_reply(message, f'{value.upper()} já está cadastrada!')
        else:
            keywords.add(value.lower())
            text = f'Busca cadastrada com sucesso para `{value.upper()}`!'

            await send_message_reply(message, text)
    else:
        text = """
            Valor para busca não fornecido.
            Envie `/cadastrar + sua busca` para cadastrar um nova busca

            *ex*: `/cadastrar python`."""

        await send_message_reply(message, text)


async def remove(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command to remove a keyword to search

    Parameters:
    update (telegram.Update): `PTB Update object`
    context (ContextTypes.DEFAULT_TYPE): `PTB Context object`

    Returns:
    None: no returns
    """

    assert context.chat_data is not None and update.message
    chat_data, message = context.chat_data, update.message
    keywords: set[str] = chat_data.setdefault('keywords', set())
    value = str(message.text).partition(' ')[2]

    if value:
        try:
            keywords.remove(value.strip().lower())
            await send_message_reply(message, f'`{value.upper()}` removido!')
        except KeyError:
            text = f"""
                `{value.upper()}` não consta em suas buscas!
                Use `/listar` para verificar as buscas cadastradas."""

            await send_message_reply(message, text)
    else:
        text = """
            Valor para remoção não fornecido.
            Envie `/remover + sua busca` para remover um busca

            *ex*: `/remover python`."""

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
        text = """
            Não há buscas cadastradas!
            Para cadastrar novas buscas digite `/cadastrar`."""

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
        text = """
            Não há buscas cadastradas!
            Para cadastrar novas buscas digite `/cadastrar`."""

        await send_message_reply(message, text)
    else:
        app.drop_chat_data(message.chat_id)
        [q.schedule_removal() for q in queue.jobs()]
        text = """
            Sua lista de buscas foi limpa!
            Para cadastrar novas buscas digite `/cadastrar`."""

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

    text = """
        Este comando não é válido.
        Clique no ícone do `☰ Menu` para ver os comandos disponíveis
        Ou digite `/` para sugestão automática"""

    await send_message_reply(update.message, text)
