import discord
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timezone
import donut
import config
import asyncio

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  logging.info(f'{datetime.now(timezone.utc)} We have logged in as {client.user}')

# API says this is called for thread creation and joining a thread...
@client.event
async def on_thread_join(thread):
  global joined_threads
  logging.info(f'{datetime.now(timezone.utc)} Joined thread {thread.name}')
  await thread.join()

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  await donut.on_message(message, config)

  if message.content.startswith('$hello'):
    bot_response = await message.channel.send('Hello!')
    await asyncio.sleep(300)
    logging.info(f'{datetime.now(timezone.utc)} Attempting to delete hello messages')
    await message.delete()
    await bot_response.delete()

load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
