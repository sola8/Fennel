import discord
import datetime
from discord.ext import commands

class Pokedex(commands.Cog):
    """"
    Pokedex commands.
    """

def setup(bot):
    bot.add_cog(Pokedex(bot))