# Based off of https://github.com/minimaxir/gpt-2-cloud-run/blob/master/Dockerfile
FROM python:3.7.3-slim-stretch

RUN apt-get -y update && apt-get -y install gcc

WORKDIR /code

COPY checkpoint /code/checkpoint

RUN pip3 --no-cache-dir install -U tensorflow==1.15.2 gpt-2-simple discord.py python-dotenv

COPY .env .

COPY src/ .

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD [ "python", "./bot.py" ]