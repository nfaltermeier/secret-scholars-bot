# About
A discord bot that randomly reacts to messages, can monitor a minecraft server, and post the top post from r/soup, and roll a random number.

Designed to be ran in a Docker container. I would recomend removing the `.env` file from the image before pushing the image anywhere.
Has x86 and ARM32v6 Docker configurations.

## Config
`.env`
```
DISCORD_TOKEN=<discord bot token>
```

Copy `src/config.py.example` to `src/config.py` and customize as desired.

## Build
### x86
Run
```sh
docker build -t secret-scholars-bot .
```

### ARM32v6
Run
```sh
docker build -f Dockerfile-arm32v6 -t secret-scholars-bot:arm32v6 --build-arg ARCH=arm32v6/ .
```

## Run
### x86
Run
```sh
docker run -d secret-scholars-bot
```

### ARM32v6
Run
```sh
docker run -d secret-scholars-bot secret-scholars-bot:arm32v6
```
