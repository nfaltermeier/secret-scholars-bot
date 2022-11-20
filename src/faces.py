import faces_util
import os
import discord
import logging
from datetime import datetime, timezone
import aiohttp
import asyncio

BYTES_IN_MEGABYTE = 1048576
MAX_SIZE = BYTES_IN_MEGABYTE * 8
class TooBigException(Exception):
  pass

allowable_attachment_types = ['image/png', 'image/jpeg']

lock = asyncio.Lock()

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
                await do_face(original_message, 'attachment_picture.png', conf, lambda : attachment.save('attachment_picture.png', use_cached=True))
                return
        if len(message.embeds) > 0:
          for embed in message.embeds:
            if embed.type == 'image':
              await do_face(original_message, 'attachment_picture.png', conf, lambda : download_file(embed.url, 'attachment_picture.png'))
              return
        if message.reference != None:
          message = await message.channel.fetch_message(message.reference.message_id)
          recursions += 1
        else:
          return
  except TooBigException:
    await message.reply('Your image is too big :(')

async def do_face(message: discord.Message, name, conf, do_download):
  logging.info('before lock')
  async with lock:
    logging.info('in lock')
    infile = name
    outfile = 'face_detected.png'
    try:
      logging.info(f'{datetime.now(timezone.utc)} Starting face processing for user {message.author.display_name} {message.author.id}')
      await do_download()

      proc = await asyncio.create_subprocess_shell(
        f'python3 faces_util.py --infile={infile} --outfile={outfile} --maxpixels={conf.face_max_pixels}',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

      stdout, stderr = await proc.communicate()
      if proc.returncode == 0:
        if stdout.decode().rstrip() == 'True':
          await message.reply(file=discord.File(outfile))
        else:
          await message.reply('No face found :(')
      else:
        errormessage = stderr.decode().rstrip()
        if errormessage.startswith('TooManyPixelsException'):
          pixels = int(errormessage.split(':')[1])
          await message.reply(f'Image has too many pixels. Image: {pixels:,} Max: {conf.face_max_pixels:,} :(')
        else:
          await message.reply('Something went wrong :(')
          logging.exception(f'{datetime.now(timezone.utc)} Face subprocess error {errormessage}')
    except discord.NotFound:
      logging.exception(f'{datetime.now(timezone.utc)} Face Attachment not found')
      await message.reply('Attachment not found :(')
    except discord.HTTPException:
      logging.exception(f'{datetime.now(timezone.utc)} Face HTTP error')
      await message.reply('Could not download attachment :(')
    finally:
      if os.path.exists(outfile):
        os.remove(outfile)
      if os.path.exists(infile):
        os.remove(infile)

async def download_file(url, out_filename):
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
      img = await resp.read()
      with open(out_filename, 'wb') as f:
        f.write(img)
        if f.tell() > MAX_SIZE:
          os.remove(out_filename)
          raise TooBigException
