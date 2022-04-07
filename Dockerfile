# Based off of https://github.com/minimaxir/gpt-2-cloud-run/blob/master/Dockerfile
FROM python:3.8-slim-buster

WORKDIR /code

RUN pip3 --no-cache-dir install -U py-cord==2.0.0b5 python-dotenv

COPY .env src/ secret-scholars-bot-config.json ./

CMD [ "python", "./bot.py" ]
