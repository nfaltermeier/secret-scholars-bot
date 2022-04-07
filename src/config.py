import io
import os
import json
import logging
from datetime import datetime, timezone

def read_or_create_config():
  filename = 'secret-scholars-bot-config.json'

  if os.path.isfile(filename):
    with open(filename, 'r') as f:
      conf = json.load(f)

      if not 'donut-ids' in conf:
        conf['donut-ids'] = []
      elif not type(conf['donut-ids']) is list:
        raise Exception('config file key \'donut-ids\' should be an array with discord user IDs to donut')
      if not 'strict-donuts' in conf:
        conf['strict-donuts'] = false
      elif not type(conf['strict-donuts']) is bool:
        raise Exception('config file key \'strict-donuts\' should be an bool to delete messages from donut users that block the bot')
      return conf
  else:
    with open(filename, 'w') as f:
      conf = {
        'donut-ids': [],
        'strict-donuts': False
      }
      json.dump(conf, f)
      logging.info(f'{datetime.now(timezone.utc)} Created default config file at \'{filename}\'')
      return conf
