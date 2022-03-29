import discord
import asyncio
import random
import logging

async def on_message(message):
  if message.content.startswith('$roll'):
    await message.channel.send(f'{message.author.mention} rolled {random.randint(0, 100)}')
    return True
  else:
    return False
