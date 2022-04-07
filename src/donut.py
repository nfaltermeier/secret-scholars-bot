import discord
import asyncio
import random
import logging

emoji = []
chance = 0

def add_emoji(client, conf):
  global emoji, chance
  emoji = conf.random_reaction_emoji
  for e in conf.random_reaction_custom_emote_ids:
    emoji.append(client.get_emoji(e))

  chance = conf.random_reaction_base_chance

async def on_message(message, conf, client):
  global chance

  if random.randint(0, 100) < chance:
    await message.add_reaction(emoji[random.randrange(0, len(emoji))])
    chance = random.uniform(0, conf.random_reaction_base_chance * 2)
  else:
    chance += conf.random_reaction_chance_increment
    if message.author.id in conf.donut_ids:
      try:
        if random.randint(1, 5) == 1:
          await message.add_reaction("🇱")
          await message.add_reaction("🇮")
          await message.add_reaction("🇬")
          await message.add_reaction("🇲")
          await message.add_reaction("🇦")
          await message.add_reaction("🇩")
          await message.add_reaction("🇴")
          await message.add_reaction("🇳")
          await message.add_reaction("🇺")
          await message.add_reaction("🇹")
          await message.add_reaction("🇸")
          await message.add_reaction("🍩")
          await message.add_reaction("👅")
        else:
          await message.add_reaction("🍩")
          await message.add_reaction("🇩")
          await message.add_reaction("🇴")
          await message.add_reaction("🇳")
          await message.add_reaction("🇺")
          await message.add_reaction("🇹")
          await message.add_reaction("🇸")
      except discord.HTTPException as result:
        if result.status == 403 and conf.strict_donuts:
          await message.delete()
          bot_response = await message.channel.send("Donut be naughty...", delete_after=10)
