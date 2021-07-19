from os import stat
import discord
from discord.ext import commands
from helpers.utils import *

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx, *args):
        await ctx.send(", ".join(args))

    @commands.command(aliases=('p',))
    async def player(self, ctx, pid: int):
        
        player = await fetch_player(pid)
        teams = await fetch_team(player["tid"])
        stats = await fetch_stats(pid)
        ratings = await fetch_ratings(pid)

        physical_ratings = (
            f"**Hgt:** {ratings['hgt']}",
            f"**Str:** {ratings['stre']}",
            f"**Spd:** {ratings['spd']}",
            f"**Jmp:** {ratings['jmp']}",
            f"**End:** {ratings['endu']}" 

        )

        shooting_ratings = (
            f"**Ins:** {ratings['ins']}",
            f"**Dnk:** {ratings['dnk']}",
            f"**FT:** {ratings['ft']}",
            f"**2PT:** {ratings['fg']}",
            f"**3PT:** {ratings['tp']}" 

        )

        skill_ratings = (
            f"**oIQ:** {ratings['oiq']}",
            f"**dIQ:** {ratings['diq']}",
            f"**Drb:** {ratings['drb']}",
            f"**Pss:** {ratings['pss']}",
            f"**Reb:** {ratings['reb']}" 

        )

        player_info = f'{stats["jerseyNumber"]} | {find_player(player)}'
        team_info = f'{teams["region"]} {teams["name"]}'

        embed = discord.Embed(title=player_info, description=f"**{ratings['pos']}** | {team_info}")
        embed.set_thumbnail(url=teams['imgURL'])
        embed.add_field(name="__Physical__", value="\n".join(physical_ratings))
        embed.add_field(name="__Shooting__", value="\n".join(shooting_ratings))
        embed.add_field(name="__Skill__", value="\n".join(skill_ratings))
        embed.set_image(url=player['imgURL'])

        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Test(bot))
    