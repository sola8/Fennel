import discord
import datetime
from discord.ext import commands

class Mart(commands.Cog):
    """"
    Pokemart commands.
    """

def setup(bot):
    bot.add_cog(Mart(bot))