import os
import urllib.request
import ujson as json

from config import *
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

if LATEST_EXPORT.lower().startswith('http'):
    req = urllib.request.Request(LATEST_EXPORT)
else:
    raise ValueError from None
pass

with urllib.request.urlopen(req) as f:
    export = json.loads(f.read().decode('utf-8-sig'))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(BOT_TOKEN)
