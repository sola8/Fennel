from discord.ext import commands

import main
from . import utils

# Should give pid instead?
class PlayerConverter(commands.Converter):
    async def convert(self, ctx, arg):
        arg = arg.strip().lower()

        if arg.isdigit():
            arg = int(arg)
            player = list(filter(lambda player: player['pid'] == arg, main.export['players']))[0]
                    
        elif type(arg) == str:
            player = list(filter(lambda player: utils.find_player_name(player).lower() == arg or
                                                utils.find_player_nickname(player).lower() == arg, main.export['players']))

        return player

# Return tid instead?
class TeamConverter(commands.Converter):
    async def convert(self, ctx, arg):
        arg = arg.strip().lower()

        if arg.isdigit():
            arg = int(arg)
            team = list(filter(lambda team: team['tid'] == arg, main.export['teams']))[0]
                    
        elif type(arg) == str:
            team = list(filter(lambda team: 
                                team['name'].lower() == arg or 
                                team['region'].lower() == arg or 
                                team['name'].lower() + " " + team['region'].lower() == arg, main.export['teams']))[0]

        return team


