import discord
import os
from dotenv import load_dotenv
import gpt_2_simple as gpt2
import logging

logging.basicConfig(level=logging.INFO)

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='secret_scholars')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$ss'):
        text = gpt2.generate(sess, 
              run_name='secret_scholars',
              top_k=20,
              nsamples=1,
              batch_size=1,
              temperature=1.4,
              length = 150,
              prefix = ""
                    )
        await message.channel.send(text)

load_dotenv()
print('starting bot')
client.run(os.getenv('DISCORD_TOKEN'))
