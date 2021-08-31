from discord.ext import commands

from main import get_players, get_teams
from . import utils

# Should give pid instead?
class PlayerConverter(commands.Converter):
    async def convert(self, ctx, arg):
        arg = arg.strip().lower()

        if arg.isdigit():
            arg = int(arg)
            player = list(filter(lambda player: player['pid'] == arg, get_players()))
                    
        elif type(arg) == str:
            player = list(filter(lambda player: utils.find_player_name(player).lower() == arg or
                                                utils.find_player_nickname(player) == arg, get_players()))

        return player

# Return tid instead?
# For later, not doing rosters anymore
class TeamConverter(commands.Converter):
    async def convert(self, ctx, arg):
        arg = arg.strip().lower()

        if arg.isdigit():
            arg = int(arg)
            team = list(filter(lambda team: team['tid'] == arg, get_teams()))[0]
                    
        elif type(arg) == str:
            team = list(filter(lambda team: 
                                team['name'].lower() == arg or 
                                team['region'].lower() == arg or 
                                team['name'].lower() + " " + team['region'].lower() == arg, get_teams()))[0]

        return team


