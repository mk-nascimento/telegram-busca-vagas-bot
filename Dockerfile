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

FROM python:3.11-slim-bookworm AS development

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

RUN <<EOF
apt-get update
apt-get install -qqy curl git nodejs pipx
apt-get clean
EOF

RUN <<EOF
useradd -s "$SHELL" -m vscode
groupadd docker
usermod -aG docker vscode
EOF

RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
RUN sed -i 's/OSH_THEME=.*/OSH_THEME=vscode/' ~/.bashrc

RUN git config --global --add safe.directory /workspace
RUN python3 -m pip install --no-cache-dir --quiet poetry~=1.7
