import discord
import asyncio
import aiohttp
import random
import logging
from datetime import datetime, timezone

session = aiohttp.ClientSession()
async def on_message(message, client, conf):
  if message.content.startswith("$soup"):
    if not message.channel.name in conf.soup_channels:
      await message.channel.send('Please use the right channel :slight_smile:', delete_after=300)
      await asyncio.sleep(300)
      await message.delete()
      return
    args = message.content.split()
    cat = 'top'
    if len(args) > 1:
      options = ['hour', 'day', 'week', 'month', 'year', 'all']
      if args[1] in options:
        cat = args[1]
      else:
        await message.channel.send(f"expected first argument to be one of {', '.join(options)}")
        return

    try:
      url = f'https://api.reddit.com/r/soup/top?t={cat}&limit=1&raw_json=1'
      result = None
      async with session.get(url) as resp:
        soup_data = await resp.json()
        soups = soup_data['data']['children']
        if len(soups) > 0:
          soup = soups[0]['data']
          if 'is_gallery' in soup and soup['is_gallery']:
            result = f"https://i.redd.it/{soup['gallery_data']['items'][0]['media_id']}.jpg"
          elif 'is_video' in soup and soup['is_video']:
            if 'secure_media' in soup and 'reddit_video' in soup['secure_media']:
              result = soup['secure_media']['reddit_video']['fallback_url']
            else:
              logging.info(f'{datetime.now(timezone.utc)} Soup got non reddit_video video for url: {url}')
              result = soup['url']
          else:
            result = soup['url']
        else:
          result = "No soup found :("
      await message.channel.send(result)
    except BaseException as error:
      logging.exception(f'{datetime.now(timezone.utc)} Soup on_message')
      await message.channel.send("Something went wrong :(")
