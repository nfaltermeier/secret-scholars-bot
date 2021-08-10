## Continue branch
Allows continuing a message, but the seed parameter does nothing so the bot produces the same message every time when given the same prompt.

## Build
Create `.env` file with the contents:
```
DISCORD_TOKEN=<discord bot token>
```
then put the model(s) in a new folder named `checkpoint`.

Next run
```sh
docker build -t secret-scholars-bot .
```

## Run
Run
```sh
docker run -d secret-scholars-bot
```
