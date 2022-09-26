import lib.faces_util as faces_util
import os
import discord

BYTES_IN_MEGABYTE = 1048576

allowable_attachment_types = ['image/png', 'image/jpeg']

async def on_message(message, client, conf):
  if message.content.startswith("$face"):
    if len(message.attachments) > 0:
      for attachment in message.attachments:
        # check if attachment is a picture and is smaller than 8mb
        if attachment.content_type in allowable_attachment_types and attachment.size < (8 * BYTES_IN_MEGABYTE):
          if attachment.proxy_url != '404':
            try:
              await attachment.save('attachment_picture.png', use_cached=True)
              found, path = faces_util.get_face_replace('attachment_picture.png')
              if found:
                await message.channel.send(file=discord.File(path))
              else:
                await message.channel.send('No face found :(')
              if os.path.exists('face_detected.png'): 
                os.remove('face_detected.png')
            except discord.HTTPException as error:
              logging.exception(f'{datetime.now(timezone.utc)} Face on_message')
              await message.channel.send('Could not download attachment :(')
            except discord.NotFound as error:
              logging.exception(f'{datetime.now(timezone.utc)} Face on_message')
              await message.channel.send('Attachment not found :(')
  