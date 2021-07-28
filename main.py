import os
import urllib.request
import ujson as json

from config import *
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

# Load export, define basic export functions
# Launcher.py?
if LATEST_EXPORT.lower().startswith('http'):
    req = urllib.request.Request(LATEST_EXPORT)
else:
    raise ValueError from None
pass

with urllib.request.urlopen(req) as f:
    export = json.loads(f.read().decode('utf-8-sig'))

    def get_season():
        season = export['gameAttributes']['season']
        return season

    def get_current_phase():
        phase = export['gameAttributes']['phase'] 
        return phase
    
    def get_teams():
        teams = export['teams']
        return teams

    def get_players():
        players = export['players']
        return players

    def get_schedule():
        schedule = export['schedule']
        return schedule

# Load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(BOT_TOKEN)
