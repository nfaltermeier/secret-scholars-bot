import lib.faces_util as faces_util
import os
import discord
import logging
from datetime import datetime, timezone
import aiohttp
from asyncio import run

BYTES_IN_MEGABYTE = 1048576
MAX_SIZE = BYTES_IN_MEGABYTE * 8
class TooBigException(Exception):
  pass

allowable_attachment_types = ['image/png', 'image/jpeg']

async def on_message(message: discord.Message, client, conf):
  try:
    if message.content.startswith("$face"):
      recursions = 0
      original_message = message
      while recursions < 2:
        if len(message.attachments) > 0:
          for attachment in message.attachments:
            # check if attachment is a picture and is smaller than 8mb
            if attachment.content_type in allowable_attachment_types:
              if attachment.size > MAX_SIZE:
                raise TooBigException
              if attachment.proxy_url != '404':
                await do_face(original_message, 'attachment_picture.png', lambda : attachment.save('attachment_picture.png', use_cached=True))
                return
        if len(message.embeds) > 0:
          for embed in message.embeds:
            if embed.type == 'image':
              await do_face(original_message, 'attachment_picture.png', lambda : download_file(embed.url, 'attachment_picture.png'))
              return
        if message.reference != None:
          message = await message.channel.fetch_message(message.reference.message_id)
          recursions += 1
        else:
          return
  except TooBigException:
    await message.channel.send('Your image is too big :(')

async def do_face(message: discord.Message, name, do_download):
  try:
    logging.info(f'{datetime.now(timezone.utc)} Starting face processing for user {message.author.display_name} {message.author.id}')
    await do_download()
    found, path = faces_util.get_face_replace(name)
    if found:
      await message.channel.send(file=discord.File(path))
    else:
      await message.channel.send('No face found :(')
    if os.path.exists('face_detected.png'): 
      os.remove('face_detected.png')
    if os.path.exists(name): 
      os.remove(name)
  except discord.NotFound:
    logging.exception(f'{datetime.now(timezone.utc)} Face on_message')
    await message.channel.send('Attachment not found :(')
  except discord.HTTPException:
    logging.exception(f'{datetime.now(timezone.utc)} Face on_message')
    await message.channel.send('Could not download attachment :(')

async def download_file(url, out_filename):
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
      img = await resp.read()
      with open(out_filename, 'wb') as f:
        f.write(img)
        if f.tell() > MAX_SIZE:
          os.remove(out_filename)
          raise TooBigException
