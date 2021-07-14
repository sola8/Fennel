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
        guild = ctx.guild

        no_voice_channels = len(guild.voice_channels)
        no_text_channels = len(guild.text_channels)

        embed = discord.Embed(description="Server Status",
                              colour=discord.Colour.dark_purple())

        embed.set_thumbnail(
            url="")

        embed.set_image(
            url="")

        embed.add_field(name="Server Name", value=guild.name, inline=False)

        embed.add_field(name="# Voice Channels", value=no_voice_channels)

        embed.add_field(name="# Text Channels", value=no_text_channels)
        embed.set_author(name=self.bot.user.name)
        embed.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=embed)
