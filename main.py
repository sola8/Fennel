import os
import urllib.request
import ujson as json
import logging

from config import *

import discord
from discord.ext import commands, tasks

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

if LATEST_EXPORT.lower().startswith('http'):
    req = urllib.request.Request(LATEST_EXPORT)
else:
    raise ValueError from None
pass

with urllib.request.urlopen(req) as f:
    ex = json.loads(f.read().decode('utf-8-sig'))

def get_season():
    season = ex['gameAttributes']['season']
    return season

def get_current_phase():
    phase = ex['gameAttributes']['phase'] 
    return phase
    
def get_teams():
    teams = ex['teams']
    return teams

def get_players():
    players = ex['players']
    return players

def get_schedule():
    schedule = ex['schedule']
    return schedule

def is_regseason(stat, season=get_season()):
        return (stat['playoffs'] is False 
                and stat['season'] == season 
                and stat['gp'] > 0)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print("-------------------")
    status_task.start()

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            # We need to capitalize because the command arguments have no capital letter in the code.
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error

@tasks.loop(minutes=1.0)
async def status_task():
    status = "Working on it..."
    await bot.change_presence(activity=discord.Game(status))

# Load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded extension 'cogs.{filename[:-3]}'")
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            print(f"Failed to load extension {filename[:-3]}\n{exception}")
            

bot.run(BOT_TOKEN)
