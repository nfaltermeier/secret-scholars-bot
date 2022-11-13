import random
import re

w = 0
excuses = {}

def load_excuses(config):
  global w, excuses
  w = 0
  excuses = {}
  for e in config.excuses:
    if isinstance(e, str):
      w += 1
      excuses[w] = e
    else:
      w += e[1]
      excuses[w] = e[0]

def roll():
  r = random.uniform(0, w)
  for e in excuses:
    if (e >= r):
      return excuses[e]

trigger = re.compile(r"(^|\s)\$excuse($|\s)", re.MULTILINE)
async def on_message(message):
  pos = 0
  m = trigger.search(message.clean_content, pos)
  if m is None:
    return
  result = message.clean_content
  while m is not None:
    r = roll()
    # Include capture group 1 and 2 in the result to include possible spaces around $excuse
    result = result[0:m.end(1)] + r + result[m.start(2):]
    pos = m.start() + len(r)
    m = trigger.search(result, pos)
  await message.channel.send(result)
