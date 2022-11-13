import discord
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timezone
import donut
import soup
import faces
import roll
import config
import asyncio
import minecraft
import excuse
import autogen_buildtime

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  logging.info(f'{datetime.now(timezone.utc)} Logged in as {client.user}')
  donut.add_emoji(client, config)
  minecraft.start(client, config)
  excuse.load_excuses(config)

# API says this is called for thread creation and joining a thread...
@client.event
async def on_thread_join(thread):
  global joined_threads
  logging.info(f'{datetime.now(timezone.utc)} Joined thread {thread.name}')
  await thread.join()

@client.event
async def on_message(message):
  try:
    # Ignore the bot's own messages
    if message.author == client.user:
      return

    # keep most bot functions restricted to the home server
    if message.guild is None or message.guild.id != config.homeserver_id:
      return

    await donut.on_message(message, config, client)
    await soup.on_message(message, client, config)
    await excuse.on_message(message)
    await faces.on_message(message, client, config)
    if await roll.on_message(message):
      return

    if message.content.startswith('$version'):
      time = datetime.fromisoformat(autogen_buildtime.build_time)
      await message.channel.send(f'Build time: {time.strftime("%b %d %Y %X %Z")}', delete_after=300)
      await asyncio.sleep(300)
      await message.delete()
    elif message.content.startswith('$hello'):
      await message.channel.send('Hello!', delete_after=300)
      await asyncio.sleep(300)
      await message.delete()
  except BaseException as error:
    logging.exception(f'{datetime.now(timezone.utc)} main on_message failed')
    await message.channel.send("Something went wrong :(")
    
load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
