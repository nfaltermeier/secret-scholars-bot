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
