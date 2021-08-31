import discord
from discord.ext import commands
from discord.ext.menus.views import ViewMenuPages

from main import get_season
from helpers import fetch, converters, utils, pagination

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("No Pokemon found!") 

    @commands.command(aliases=('p',))
    async def player(self, ctx, *, arg):

        # Check if argument is int/str
        player = await converters.PlayerConverter().convert(ctx, arg)

        # Put this in fetch player data function?
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


        playerDict = fetch.fetch_player_data(player['pid'])
        teamDict = fetch.fetch_team_data(playerDict['tid'])
        embedColor = utils.find_team_color(teamDict)

        physical_ratings = (
            f"**Hgt:** {playerDict['ratings']['hgt']}",
            f"**Str:** {playerDict['ratings']['stre']}",
            f"**Spd:** {playerDict['ratings']['spd']}",
            f"**Jmp:** {playerDict['ratings']['jmp']}",
            f"**End:** {playerDict['ratings']['endu']}" 

        )

        shooting_ratings = (
            f"**Ins:** {playerDict['ratings']['ins']}",
            f"**Dnk:** {playerDict['ratings']['dnk']}",
            f"**FT:** {playerDict['ratings']['ft']}",
            f"**2PT:** {playerDict['ratings']['fg']}",
            f"**3PT:** {playerDict['ratings']['tp']}" 

        )

        skill_ratings = (
            f"**oIQ:** {playerDict['ratings']['oiq']}",
            f"**dIQ:** {playerDict['ratings']['diq']}",
            f"**Drb:** {playerDict['ratings']['drb']}",
            f"**Pss:** {playerDict['ratings']['pss']}",
            f"**Reb:** {playerDict['ratings']['reb']}" 

        )

        embed = discord.Embed(title=f'{playerDict["jerseyNumber"]} | {playerDict["name"]}', 
                              description=f"**{playerDict['ratings']['pos']}** | {teamDict['name']}\n**OVR:** {playerDict['ratings']['ovr']} | **POT:** {playerDict['ratings']['pot']}",
                              color=embedColor)

        embed.set_thumbnail(url=playerDict['imgURL'])

        embed.add_field(name=f"Item | Ability:", 
                        value=f"{playerDict['item']} | {playerDict['ability']}", 
                        inline=False)

        # embed.add_field(name=f"Silly Champ:", 
        #                 value=f"<:type_flying:881731291819679814> | <:type_flying:881731291819679814>", 
        #                 inline=False)

        embed.add_field(name="Physical", value="\n".join(physical_ratings))
        embed.add_field(name="Shooting", value="\n".join(shooting_ratings))
        embed.add_field(name="Skill", value="\n".join(skill_ratings))

        embed.add_field(name=f"{get_season()}:", 
                        value=f"{playerDict['current_stats']['pts']} pts, {playerDict['current_stats']['orb'] + playerDict['current_stats']['drb']} trb, {playerDict['current_stats']['ast']} ast, {playerDict['current_stats']['per']} PER")

        embed.add_field(name=f"Career:", 
                        value=f"{playerDict['career_stats']['pts']} pts, {playerDict['career_stats']['orb'] + playerDict['career_stats']['drb']} trb, {playerDict['career_stats']['ast']} ast, {playerDict['career_stats']['per']} PER, {playerDict['career_stats']['ws']} WS", 
                        inline=False)

        embed.set_footer(text=f"Viewing {playerDict['name']}\nPID: {playerDict['pid']}")

        await ctx.channel.send(embed=embed)

    @commands.command(aliases=('fa',))
    async def freeagents(self, ctx):
        
        free_agents = fetch.fetch_free_agents()

        pages = ViewMenuPages(source=pagination.WildGrassPages(free_agents))

        try:
            await pages.start(ctx)
        except IndexError:
            await ctx.send("No pokémon found.")



def setup(bot):
    bot.add_cog(Player(bot))