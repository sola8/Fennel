import discord
from discord.ext import commands
from helpers import utils

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setchannel(self, ctx, channel = discord.Channel):
        pass

    @commands.command()
    async def stats(self, ctx, data):
        pass

    @commands.command()
    async def progs(self, ctx, data):
        pass

    @commands.command()
    async def freeagents(self, ctx, data):
        pass

    @commands.command()
    async def loadexport(self, ctx, data):
        pass

    @commands.command()
    async def ratings(self, ctx, data):
        pass

    @commands.command()
    async def awards(self, ctx, data):
        pass
    
    @commands.command()
    async def team(self, ctx, data):
        pass

    @commands.command()
    async def powerrankings(self, ctx, data):
        pass

    @commands.command()
    async def player(self, ctx, data):
        pass

    @commands.command()
    async def compare(self, ctx, link: str):
        pass

    @commands.command()
    async def top(self, ctx, data):
        pass

    @commands.command()
    async def roster(self, ctx, data):
        pass

    @commands.command()
    async def sos(self, ctx, data):
        pass

    @commands.command()
    async def hello(self, ctx, *args):
        await ctx.send(", ".join(args))
        
def setup(bot):
    bot.add_cog(Test(bot))