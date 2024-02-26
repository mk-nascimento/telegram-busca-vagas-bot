FROM python:3.10-alpine AS build

ENV POETRY_VIRTUALENVS_CREATE=0 \
    PACKAGES=/usr/local/lib/python3.10/site-packages
WORKDIR /code


RUN pip install poetry~=1.7 --quiet

COPY pyproject.toml .

RUN poetry install --no-interaction --no-ansi --quiet --no-dev


FROM python:3.10-alpine AS runtime

ENV PACKAGES=/usr/local/lib/python3.10/site-packages
WORKDIR /code


RUN mkdir env

COPY --from=build ${PACKAGES} ${PACKAGES}
COPY .env .
COPY app/ ./app


CMD python -m app.main
