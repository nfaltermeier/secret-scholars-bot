# Based off of https://github.com/minimaxir/gpt-2-cloud-run/blob/master/Dockerfile
FROM python:3.8-slim-buster

RUN apt-get -y update && apt-get -y install git

WORKDIR /code

RUN pip3 --no-cache-dir install -U git+https://github.com/Rapptz/discord.py python-dotenv

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY .env src/ secret-scholars-bot-config.json ./

CMD [ "python", "./bot.py" ]
