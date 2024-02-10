# Busca Vagas Bot usando [python-telegram-bot (v20+)](https://github.com/python-telegram-bot/python-telegram-bot)

[![Python](https://img.shields.io/badge/Python->=3.10-blue.svg?logo=python)](https://www.python.org/downloads/release/python-3100/)
[![Poetry](https://img.shields.io/badge/Poetry->=1.7-blue.svg?logo=poetry)](https://python-poetry.org/docs/)

## Introdução
Este é um simples bot Telegram desenvolvido em Python usando a biblioteca `python-telegram-bot` na versão 20.7. O bot foi construído com a intenção de facilitar busca em uma API com base em "palavras-chave" cadastradas.

## Configuração com Poetry
> Antes de prosseguir com a instalação, é recomendado verificar a versão do Python e Poetry recomendada no topo deste arquivo. Certifique-se de ter a versão correta instalada em seu sistema antes de continuar.
1. Clone este repositório.
2. Instale o Poetry seguindo o [manual de instalação](https://python-poetry.org/docs/#installation) para sua plataforma.
3. Após instalar o Poetry, navegue até o diretório do projeto e execute o comando abaixo para instalar as dependências.
    ```bash
        poetry install
    ```
4. Crie um bot no Telegram usando o BotFather e obtenha o token do bot.
5. Crie um arquivo `.env` na raiz do projeto e siga o modelo do arquivo `.env.example`. Adicione o token do bot no arquivo `.env`:
    ```.env
    TELEGRAM_BOT_TOKEN=<seu_token_aqui>
    ```

## Configuração com Pip
> Antes de prosseguir com a instalação, é recomendado verificar a versão do Python recomendada no topo deste arquivo. Certifique-se de ter a versão correta instalada em seu sistema antes de continuar.
1. Clone este repositório.
2. Instale o Pip seguindo o [manual de instalação](https://pip.pypa.io/en/stable/installation/) para sua plataforma.
3. Após instalar o Pip, navegue até o diretório do projeto e execute o comando abaixo para instalar as dependências.
    > É altamente recomendado criar um ambiente virtual antes de instalar as dependências:
    ```bash
        python -m venv <sua_venv>      # Cria um ambiente virtual <sua_venv>
        source <sua_venv>/bin/activate # Ativa o ambiente virtual no Linux/Mac
        <sua_venv>\Scripts\activate    # Ativa o ambiente virtual no Windows
    ```
    ```bash
        python -m pip install -r requirements.txt
    ```
4. Crie um bot no Telegram usando o BotFather e obtenha o token do bot.
5. Crie um arquivo `.env` na raiz do projeto e siga o modelo do arquivo `.env.example`. Adicione o token do bot no arquivo `.env`:
    ```.env
    TELEGRAM_BOT_TOKEN=<seu_token_aqui>
    ```

## Uso
Após instaladas as dependências, execute o script principal usando o comando:
```bash
    python -m app.main
```

## Funcionalidades
- Responder a comandos predefinidos.
- Cadastrar, remover e listar "palavras-chave" para busca na API.
- Busca agendada as 10h e 18h (horário de Brasília).
- Interagir com APIs externas para fornecer informações ou serviços adicionais.


## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias, correções de bugs ou novas funcionalidades.

## Autor
LinkedIn: [Maksuel Nascimento](https://www.linkedin.com/in/maksuel-nascimento/)

## Licença
Este projeto é licenciado sob a [Licença Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Consulte o arquivo [LICENSE](https://github.com/mk-nascimento/telegram-busca-vagas-bot/blob/develop/LICENSE.MD) para obter mais detalhes.
