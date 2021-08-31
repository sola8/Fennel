import discord
import datetime
from discord.ext import commands

class Abilities(commands.Cog):
    """"
    Ability commands.
    """

def setup(bot):
    bot.add_cog(Abilities(bot))
