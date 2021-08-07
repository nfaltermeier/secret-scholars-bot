FROM tensorflow/tensorflow:latest-gpu

WORKDIR /code

COPY checkpoint /checkpoint

RUN pip install -U discord.py python-dotenv gpt-2-simple

COPY .env .

COPY src/ .

CMD [ "python", "./bot.py" ] 