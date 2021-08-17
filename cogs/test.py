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

        season_stat = fetch.grab_season_stats(player['stats'])
        career_stat = fetch.grab_career_stats(player['stats'])        
        
        stats = player['stats'][-1]
        ratings = player['ratings'][-1]
    
        team = list(filter(lambda team: team['tid'] == player['tid'] or team['tid'] == stats['tid'], main.export['teams']))[0]

        if team is None:
            team['region'] = "N/A"
            team['name'] = None

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

        team_color = int(team['colors'][0].replace("#", ""),16)
        embedColor = int(hex(team_color), 0)

        embed = discord.Embed(title=f'{stats["jerseyNumber"]} | {utils.find_player_name(player)}', 
                              description=f"**{ratings['pos']}** | {team['region']} {team['name']}\n**OVR:** {ratings['ovr']} | **POT:** {ratings['pot']}",
                              color=embedColor)

        embed.set_thumbnail(url=player['imgURL'])

        embed.add_field(name="Physical", value="\n".join(physical_ratings))
        embed.add_field(name="Shooting", value="\n".join(shooting_ratings))
        embed.add_field(name="Skill", value="\n".join(skill_ratings))

        embed.add_field(name=f"{main.get_season()}:", 
                        value=f"{season_stat['pts']} pts, {season_stat['orb'] + season_stat['drb']} trb, {season_stat['ast']} ast, {season_stat['per']} PER")

        embed.add_field(name=f"Career:", 
                        value=f"{career_stat['pts']} pts, {career_stat['orb'] + career_stat['drb']} trb, {career_stat['ast']} ast, {career_stat['per']} PER, {career_stat['ws']} WS", 
                        inline=False)

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