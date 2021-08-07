import discord
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

load_dotenv()
print('starting bot')
client.run(os.getenv('DISCORD_TOKEN'))
