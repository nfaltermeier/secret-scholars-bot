# About
A discord bot that doesn't do all that much at the moment.

Designed to be ran in a Docker container. I would recomend removing the `.env` file from the image before pushing the image anywhere.

## Config
`.env`
```
DISCORD_TOKEN=<discord bot token>
```
`secret-scholars-bot-config.json`
```
{
  "donut-ids": [
    <integer discord id 1>
  ],
  "strict-donuts": false
}
```

## Build

Run
```sh
docker build -t secret-scholars-bot .
```

## Run
Run
```sh
docker run -d secret-scholars-bot
```
