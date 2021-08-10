import discord
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timezone
import gptlib
import config

logging.basicConfig(level=logging.INFO)

total_generated = 0

conf = config.read_or_create_config()

client = discord.Client()

def allowed_channel(channel):
    return channel in conf['allowed-channels']

@client.event
async def on_ready():
    logging.info(f'{datetime.now(timezone.utc)} We have logged in as {client.user}')

@client.event
async def on_message(message):
    global total_generated

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    else:
        for cmd in conf['checkpoints'].keys():
            if message.content.startswith(f'${cmd}'):
                if allowed_channel(message.channel.name):
                    run_name = conf['checkpoints'][cmd]
                    prefix = message.content[len(cmd) + 2:]
                    logging.info(f'{datetime.now(timezone.utc)} Generating message with prefix "{prefix}" for model "{run_name}". Previously generated count: {total_generated}')
                    total_generated += 1
                    await gptlib.generate(run_name, prefix, message.channel.send)
                else:
                    await message.channel.send('Please use the right channel :slight_smile:')
        

load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
