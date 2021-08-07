FROM python:3.9-slim

WORKDIR /code

RUN pip install -U discord.py python-dotenv

COPY .env .

COPY src/ .

CMD [ "python", "./bot.py" ] 