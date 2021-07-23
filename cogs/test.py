import discord

from bot import export
from discord.ext import commands
from helpers.utils import *
from config import *

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx, *args):
        await ctx.send(", ".join(args))

    # Search for player using pid or name
    @commands.command(aliases=('p',))
    async def player(self, ctx, arg):

        arg = arg.strip()

        if arg.isdigit():
            pid = int(arg)
    
        pid = arg
        
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

        if teams is None:
            former_team = await fetch_team(stats["tid"])
            player_info = f'[RETIRED] {find_player(player)}'
            team_info = f'Last Team: {former_team["region"]} {former_team["name"]}'

        else:
            player_info = f'{stats["jerseyNumber"]} | {find_player(player)}'
            team_info = f'{teams["region"]} {teams["name"]}'

        embed = discord.Embed(title=player_info, description=f"**{ratings['pos']}** | {team_info}")

        if teams is not None:
            embed.set_thumbnail(url=teams['imgURL'])

        embed.add_field(name="__Physical__", value="\n".join(physical_ratings))
        embed.add_field(name="__Shooting__", value="\n".join(shooting_ratings))
        embed.add_field(name="__Skill__", value="\n".join(skill_ratings))
        embed.set_image(url=player['imgURL'])

        await ctx.channel.send(embed=embed)

    # Search for team using region, name, or tid
    # @commands.command(aliases=('t',))
    # async def team(self, ctx, team: str):
    #     data = dataa
    #     embed = discord.Embed()
    #     await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Test(bot))
    