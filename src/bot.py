import discord
import os
from dotenv import load_dotenv
import gpt_2_simple as gpt2
import logging
from datetime import datetime, timezone

# setup logging

logging.basicConfig(level=logging.INFO)

# setup gpt2
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='secret_scholars')

total_generated = 0

# discord bot
client = discord.Client()

@client.event
async def on_ready():
    logging.info(f'{datetime.now(timezone.utc)} We have logged in as {client.user}')

@client.event
async def on_message(message):
    global total_generated

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$sss'):
        if message.channel.name == 'bot-output' or message.channel.name == 'bot-testing':
            prefix = message.content[5:]
            logging.info(f'{datetime.now(timezone.utc)} Generating message with prefix "{prefix}". Previously generated count: {total_generated}')
            total_generated += 1
            text = gpt2.generate(sess, 
                run_name='secret_scholars',
                top_k=20,
                nsamples=1,
                batch_size=1,
                temperature=1.4,
                length = 150,
                prefix = prefix,
                return_as_list=True
                        )[0]
            # Replace code marks with a version with invisible spaces
            text = text.replace('```', '`​`​`')
            await message.channel.send(f'```{text}```')
        else:
            await message.channel.send('Please use the right channel :slight_smile:')
        

load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
