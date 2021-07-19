import discord
import datetime
from discord.ext import commands

class Base(commands.Cog):
    """"
    General bot commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        pass

    @commands.Cog.listener()
    async def on_error(self, ctx, ex):
        pass
    
    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, *args):
        pass

def setup(bot):
    bot.add_cog(Base(bot))
