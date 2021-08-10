# About
A discord bot to produce gpt-2 messages on command. The bot can be prompted by including a text after the command name in the discord message.

Designed to be ran in a Docker container.

## Config
`.env`
```
DISCORD_TOKEN=<discord bot token>
```
`secret-scholars-bot-config.json`
```
{
  "allowed-channels": [
    "<channel name 1>"
  ],
  "checkpoints": {
    "<command name>": "<checkpoint model name>"
  }
}
```
Command names must be prefixed with a `$` when used in discord for the bot to recognize the command.

## Build

Put the model(s) in a new folder named `checkpoint`.

Run
```sh
docker build -t secret-scholars-bot .
```

## Run
Run
```sh
docker run -d secret-scholars-bot
```