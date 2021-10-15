import discord
import asyncio

async def on_message(message, conf):
  if message.author.id in conf['donut-ids']:
    try:
      await message.add_reaction("🍩")
      await message.add_reaction("🇩")
      await message.add_reaction("🇴")
      await message.add_reaction("🇳")
      await message.add_reaction("🇺")
      await message.add_reaction("🇹")
      await message.add_reaction("🇸")
    except discord.HTTPException as result:
      if result.status == 403 and conf['strict-donuts']:
        await message.delete()
        bot_response = await message.channel.send("Donut be naughty...")
        await asyncio.sleep(10)
        await bot_response.delete()