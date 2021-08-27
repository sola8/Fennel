import discord
from discord.ext import commands

import main
from helpers import fetch, converters, utils

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
    async def player(self, ctx, *, arg):

        # Check if argument is int/str
        player = await converters.PlayerConverter().convert(ctx, arg)

        if len(player) > 1:

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

        player = fetch.fetch_player_data(player['pid'])
        team = fetch.fetch_team_data(player['tid'])

        # Replace everything w/ fetch_team and fetch_player functions

        if not player['current_stats']:
            embedColor = discord.Colour.dark_purple()
        else:
            stats = player['stats'][-1]
            team = list(filter(lambda team: team['tid'] == player['tid'] or team['tid'] == stats['tid'], main.export['teams']))[0]
            team_color = int(team['colors'][0].replace("#", ""),16)
            embedColor = int(hex(team_color), 0)

        physical_ratings = (
            f"**Hgt:** {player['ratings']['hgt']}",
            f"**Str:** {player['ratings']['str']}",
            f"**Spd:** {player['ratings']['spd']}",
            f"**Jmp:** {player['ratings']['jmp']}",
            f"**End:** {player['ratings']['end']}" 

        )

        shooting_ratings = (
            f"**Ins:** {player['ratings']['ins']}",
            f"**Dnk:** {player['ratings']['dnk']}",
            f"**FT:** {player['ratings']['ft']}",
            f"**2PT:** {player['ratings']['fg']}",
            f"**3PT:** {player['ratings']['']}" 

        )

        skill_ratings = (
            f"**oIQ:** {player['ratings']['oiq']}",
            f"**dIQ:** {player['ratings']['diq']}",
            f"**Drb:** {player['ratings']['drb']}",
            f"**Pss:** {player['ratings']['pss']}",
            f"**Reb:** {player['ratings']['reb']}" 

        )

        embed = discord.Embed(title=f'{player["jerseyNumber"]} | {utils.find_player_name(player)}', 
                              description=f"**{player['ratings']['pos']}** | {team['name']}\n**OVR:** {player['ratings']['ovr']} | **POT:** {player['ratings']['pot']}",
                              color=embedColor)

        embed.set_thumbnail(url=player['imgURL'])

        embed.add_field(name="Physical", value="\n".join(physical_ratings))
        embed.add_field(name="Shooting", value="\n".join(shooting_ratings))
        embed.add_field(name="Skill", value="\n".join(skill_ratings))

        embed.add_field(name=f"{main.get_season()}:", 
                        value=f"{player['current_stats']['pts']} pts, {player['current_stats']['orb'] + player['current_stats']['drb']} trb, {player['current_stats']['ast']} ast, {player['current_stats']['per']} PER")

        embed.add_field(name=f"Career:", 
                        value=f"{player['career_stats']['pts']} pts, {player['career_stats']['orb'] + player['career_stats']['drb']} trb, {player['career_stats']['ast']} ast, {player['career_stats']['per']} PER, {player['career_stats']['ws']} WS", 
                        inline=False)

        embed.set_footer(text=f"Displaying {player['name']}\nPID: {player['pid']}")

        await ctx.channel.send(embed=embed)

    # Search for team using region, name, or tid
    # Make a command group for this?
    # Roster (Season, Team Name, Team Rating, W-L) 
    # SOS, Pyramid, Advanced Stats?
    # Use hex info in export to determine embed color for each team
    @commands.command(aliases=('t',))
    async def team(self, ctx, arg, year=main.get_season()):

        team = await converters.TeamConverter().convert(ctx, arg)
        roster = fetch.fetch_team_data(team['tid'], year)
        roster_table = utils.create_roster_table(roster)

        await ctx.channel.send(f'```{roster_table}```')
        # Not sure if I need an embed for this (yet)

def setup(bot):
    bot.add_cog(Test(bot))