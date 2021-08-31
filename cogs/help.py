import discord
import datetime
from discord.ext import commands

class Help(commands.Cog):
    """"
    Help commands.
    """

def setup(bot):
    bot.add_cog(Help(bot))
