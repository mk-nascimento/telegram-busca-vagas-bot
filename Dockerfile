FROM python:3.10-alpine AS build

ENV POETRY_VIRTUALENVS_CREATE=0
WORKDIR /code


RUN pip install poetry --quiet

COPY pyproject.toml .

RUN poetry install --no-interaction --no-ansi --quiet --no-dev


FROM build AS runtime


COPY .env app/ /


CMD python -m app.main
