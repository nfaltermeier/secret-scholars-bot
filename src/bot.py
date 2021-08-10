import discord
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timezone
import gptlib

# setup logging

logging.basicConfig(level=logging.INFO)

# setup gpt2
gptlib.start_sess('secret_scholars')

total_generated = 0

# discord bot
client = discord.Client()

def allowed_channel(channel):
    return channel == 'bot-output' or channel == 'bot-testing'

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
    elif message.content.startswith('$sss'):
        if allowed_channel(message.channel.name):
            prefix = message.content[5:]
            logging.info(f'{datetime.now(timezone.utc)} Generating message with prefix "{prefix}". Previously generated count: {total_generated}')
            total_generated += 1
            await gptlib.generate(prefix, message.channel.send, message.channel.id)
        else:
            await message.channel.send('Please use the right channel :slight_smile:')
    elif message.content.startswith('$continue'):
        if allowed_channel(message.channel.name):
            logging.info(f'{datetime.now(timezone.utc)} Continuing message. Previously generated count: {total_generated}')
            total_generated += 1
            await gptlib.continue_last(message.channel.send, message.channel.id)
        else:
            await message.channel.send('Please use the right channel :kakyoin:')
        
load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
