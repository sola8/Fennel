from discord.ext import commands

class Base(commands.Cog):
    """"
    Base commands for the bot.
    """

def setup(bot):
    bot.add_cog(Base(bot))
