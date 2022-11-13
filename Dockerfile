# Based off of https://github.com/minimaxir/gpt-2-cloud-run/blob/master/Dockerfile
FROM python:3.10-slim-buster

WORKDIR /code

# opencv dependencies https://stackoverflow.com/a/63377623
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 --no-cache-dir install -U py-cord python-dotenv markovchain pillow opencv-python

COPY .env src/ secret-scholars-bot-config.json markov.txt ./

RUN printf "build_time=%s" "'`date -Iseconds`'" > autogen_buildtime.py

CMD [ "python", "./bot.py" ]
