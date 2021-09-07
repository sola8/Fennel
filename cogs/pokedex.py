from discord.ext import commands

class Pokedex(commands.Cog):
    """"
    Pokedex commands.
    """
    @commands.command()
    async def info(self, ctx, *, arg):
        pass

def setup(bot):
    bot.add_cog(Pokedex(bot))