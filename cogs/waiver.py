import discord
import datetime
from discord.ext import commands

class Waiver(commands.Cog):
    """"
    Waiver lis commands.
    """

def setup(bot):
    bot.add_cog(Waiver(bot))
