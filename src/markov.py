from markovchain.text import MarkovText, ReplyMode

markov = MarkovText()

with open('markov.txt') as fp:
  markov.data(fp.read())

def reply(input=''):
  return markov(reply_to=input, reply_mode=ReplyMode.END)

cmd = '$mk '

async def on_message(message):
  if message.content.startswith(cmd):
    prefix = message.clean_content[len(cmd):]
    await message.channel.send(reply(prefix))
