import discord

async def on_message(message: discord.Message, conf):
  if conf.enforce_embeds:
    for base, replacement in conf.embeds.items():
      test = f'https://{base}'
      test_len = len(test)
      i = message.content.find(test)
      if i == -1:
        test = f'http://{base}'
        test_len = len(test)
        i = message.content.find(test)
      if i != -1:
        space = message.content.find(" ", i)
        if space == -1:
          space = len(message.content)
        url = f'https://{replacement}{message.content[i + test_len: space]}'
        if i == 0 and space == len(message.content):
          await message.channel.send(f'{message.author.mention} sent: {url}')
          await message.delete()
        else:
          await message.edit(suppress=True)
          await message.reply(url)
