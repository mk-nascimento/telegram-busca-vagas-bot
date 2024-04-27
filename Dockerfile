FROM python:3.11-alpine AS build
ENV POETRY_VIRTUALENVS_CREATE=0

COPY pyproject.toml .

RUN pip install --no-cache-dir -q poetry~=1.7
RUN poetry install -nq --no-ansi --no-dev

FROM python:3.11-alpine AS runtime
ENV PACKAGES=/usr/local/lib/python3.11/site-packages

COPY --from=build "$PACKAGES" "$PACKAGES"
COPY .env .
COPY app/ /app

CMD python -m app.main
