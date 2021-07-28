import discord
import main
import config

from discord.ext import commands
from helpers.constants import TEAM_MAP, STATS_TO_AVERAGE


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx, *args):
        await ctx.send(", ".join(args))

    # Search for player using pid or name
    # Make a command group for this?
    # Player bios, awards, ratings, stats (basic/advanced)
    # Progressions and splits?
    # Use hex info in export to determine embed color for each player
    @commands.command(aliases=('p',))
    async def player(self, ctx, arg):

        season = main.get_season()

        def find_player_name(player):
            if len(player['lastName']) == 0:
                return player['firstName'].strip()
            if len(player['firstName']) == 0:
                return player['lastName'].strip()
            return player['firstName'].strip() + " " + player['lastName'].strip()

        arg = arg.strip()

        if arg.isdigit():
            arg = int(arg)
            player = list(filter(lambda player: player['pid'] == arg, main.export['players']))[0]
                
        else:
            player = list(filter(lambda player: find_player_name(player) == arg, main.export['players']))
            if len(player) > 1:
                duplicates = True
                if duplicates is True:

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel  

                    choices = "Multiple players found.\n"
                    indexed_players = list(enumerate(player, start=1))

                    for i_player in indexed_players:
                        choices += f"Type {i_player[0]} for {i_player[1]['firstName']} (born {i_player[1]['born']['year']})\n"
                    await ctx.send(choices)

                    msg = await self.bot.wait_for('message', check=check)

                    for index, i_player in indexed_players:
                        if int(msg.content) == index:
                            player = i_player

        stats = player['stats'][-1]
        ratings = player['ratings'][-1]    
        team = list(filter(lambda team: team['tid'] or stats['tid'] == player['tid'], main.export['teams']))[0]

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

        player_info = f'{stats["jerseyNumber"]} | {find_player_name(player)}'
        team_info = f'{team["region"]} {team["name"]}'

        embed = discord.Embed(title=player_info, description=f"**{ratings['pos']}** | {team_info}")

        if team is not None:
            embed.set_thumbnail(url=team['imgURL'])

        embed.add_field(name="__Physical__", value="\n".join(physical_ratings))
        embed.add_field(name="__Shooting__", value="\n".join(shooting_ratings))
        embed.add_field(name="__Skill__", value="\n".join(skill_ratings))
        embed.set_image(url=player['imgURL'])

        await ctx.channel.send(embed=embed)

    # Search for team using region, name, or tid
    # Make a command group for this?
    # Roster (Season, Team Name, Team Rating, W-L) 
    # SOS, Pyramid, Advanced Stats?
    # Use hex info in export to determine embed color for each team
    @commands.command(aliases=('t',))
    async def team(self, ctx, tid: int, year: int = main.get_season()):
        pass
        # Not sure if I need an embed for this (yet)

def setup(bot):
    bot.add_cog(Test(bot))
    