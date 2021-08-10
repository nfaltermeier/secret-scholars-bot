# Based off of https://github.com/minimaxir/gpt-2-cloud-run/blob/master/Dockerfile
FROM python:3.7-slim-buster

RUN apt-get -y update && apt-get -y install gcc

WORKDIR /code

COPY checkpoint checkpoint

RUN pip3 --no-cache-dir install -U tensorflow==1.15.5 gpt-2-simple discord.py python-dotenv

COPY .env src/ secret-scholars-bot-config.json ./

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD [ "python", "./bot.py" ]
