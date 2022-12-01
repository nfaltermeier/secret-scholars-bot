import discord

async def on_message(message: discord.Message, conf):
  if conf.enforce_vxtwitter:
    base_len = 19
    i = message.content.find('https://twitter.com')
    if i == -1:
      base_len = 18
      i = message.content.find('http://twitter.com')
    if i != -1:
      space = message.content.find(" ", i)
      if space == -1:
        space = len(message.content)
      url = f'https://vxtwitter.com{message.content[i + base_len: space]}'
      if i == 0 and space == len(message.content):
        await message.channel.send(f'{message.author.mention} (🤡) sent: {url}')
        await message.delete()
      else:
        await message.edit(suppress=True)
        await message.reply(url)
