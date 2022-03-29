import logging
from datetime import datetime, timezone
from discord.ext import tasks
import socket
from lib import mcping

server = None
client = None
channels = []

def start(bot, conf):
  global client, server, channels
  if not conf.minecraft_status_report_enabled:
    return
  server = mcping.StatusPing(conf.minecraft_status_report_ip, conf.minecraft_status_report_port)
  client = bot
  for channel in conf.minecraft_status_report_channels:
    channels.append(client.get_channel(channel))
  ping_minecraft.start()

@tasks.loop(minutes=5)
async def ping_minecraft():
  try:
    status = server.get_status()
    message = f"{status['description']['text']}: {status['players']['online']}/{status['players']['max']} players online"
    for channel in channels:
      await channel.send(message, delete_after=600)
  except socket.timeout as timeout:
    message = "Connection timed out (server offline)"
    for channel in channels:
      await channel.send(message, delete_after=600)
  except BaseException as error:
    message = "An error occurred while pinging the server"
    logging.exception(f'{datetime.now(timezone.utc)} minecraft ping failed')
    for channel in channels:
      await channel.send(message, delete_after=600)
