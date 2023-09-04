import discord
import asyncio
import random
import logging

async def on_message(message):
  if message.content.startswith('$roll'):
    result = random.randint(0, 100)
    comment = ''
    if result == 0:
      comment = " Critial failure!"
    elif result == 100:
      comment = " Critial success!"
    await message.channel.send(f'{message.author.mention} rolled {result}.{comment}')
    return True
  else:
    return False
