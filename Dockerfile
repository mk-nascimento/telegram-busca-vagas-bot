FROM python:3.11-alpine AS build
ENV POETRY_VIRTUALENVS_CREATE=0

COPY pyproject.toml .

RUN pip install --no-cache-dir -q poetry~=1.7
RUN poetry install -nq --no-ansi --no-dev

FROM python:3.11-alpine AS runtime
ENV PACKAGES=/usr/local/lib/python3.11/site-packages
WORKDIR /code

RUN mkdir env

COPY --from=build "$PACKAGES" "$PACKAGES"
COPY .env .
COPY app/ ./app

CMD python -m app.main

FROM python:3.11-slim-bookworm AS development

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
COPY . .

RUN <<EOF
apt-get update
apt-get install curl git nodejs pipx -qq --assume-yes
apt-get clean
EOF

RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
RUN sed -i 's/OSH_THEME=.*/OSH_THEME=vscode/' ~/.bashrc

RUN <<EOF
git config --global --add safe.directory /workspace
python3 -m pip install poetry~=1.7
mkdir -p env
EOF
