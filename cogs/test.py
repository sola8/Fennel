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
    # Need to handle retired pokemon and free agents
    # Also handle nicknames
    # Player bios, awards, ratings, stats (basic/advanced)
    # Progressions and splits?
    # Use hex info in export to determine embed color for each player
    @commands.command(aliases=('p',))
    async def player(self, ctx, arg):

        def find_player_name(player):
            if len(player['lastName']) == 0:
                return player['firstName'].strip()
            if len(player['firstName']) == 0:
                return player['lastName'].strip()
            return player['firstName'].strip() + " " + player['lastName'].strip()

        def grab_season_averages(stats):
            average_stats = []

            for metric in STATS_TO_AVERAGE:
                for stat in stats:
                    if stat['playoffs'] is False and stat['season'] == main.get_season():

                        if stat['gp'] != 0:
                            average = round(stat[metric]/stat['gp'], 1)
                            average_stats.append(average)
                        else:
                            average_stats.append(0)
                            
            return average_stats

        def grab_career_averages(stats):
            average_career_stats = []

            average_games = float(sum(
                                [stat['gp'] for stat in stats if stat['gp'] > 0 and stat['playoffs'] is False]))

            for metric in STATS_TO_AVERAGE:
                average = float(sum(
                                [stat[metric] for stat in stats if stat['gp'] > 0 and stat['playoffs'] is False]))

                # Find a more elegant way to handle players who haven't played
                if average_games == 0:
                    total = average/1
                else:
                    total = average/average_games

                average_career_stats.append(round(total, 1))
                
            return average_career_stats

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
            else:
                player = player[0]

        statline = grab_season_averages(player['stats'])
        statline_2 = grab_career_averages(player['stats'])        
        
        stats = player['stats'][-1]
        ratings = player['ratings'][-1]    
        team = list(filter(lambda team: team['tid'] == player['tid'] or team['tid'] == stats['tid'], main.export['teams']))[0]

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

        if not statline:
            season_statline = "N/A"
        else:
            season_statline = f"{statline[0]} pts - {statline[1]} ast - {statline[3] + statline[4]} trb - {statline[2]} stl"

        if not statline_2:
            career_statline = "N/A"
        else:
            career_statline = f"{statline_2[0]} pts - {statline_2[1]} ast - {statline_2[3] + statline_2[4]} trb - {statline_2[2]} stl"

        player_info = f'{stats["jerseyNumber"]} | {find_player_name(player)}'
        team_info = f'{team["region"]} {team["name"]}'

        team_color = int(team['colors'][0].replace("#", ""),16)
        embedColor = int(hex(team_color), 0)

        embed = discord.Embed(title=player_info, 
                              description=f"**{ratings['pos']}** | {team_info}",
                              color=embedColor)

        # if team is not None:
        embed.set_thumbnail(url=player['imgURL'])

        embed.add_field(name="Physical", value="\n".join(physical_ratings))
        embed.add_field(name="Shooting", value="\n".join(shooting_ratings))
        embed.add_field(name="Skill", value="\n".join(skill_ratings))
        embed.add_field(name=f"{main.get_season()}:", value=season_statline)
        embed.add_field(name=f"Career:", value=f"{career_statline}", inline=False)
        # embed.set_image(url=player['imgURL'])

        embed.set_footer(text=f"Displaying {player['firstName']}\nPID: {player['pid']}")

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