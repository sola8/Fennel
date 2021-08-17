from discord.ext import commands

import main
from . import utils

class PlayerConverter(commands.Converter):
    async def convert(self, ctx, arg):
        arg = arg.strip().lower()

        if arg.isdigit():
            arg = int(arg)
            player = list(filter(lambda player: player['pid'] == arg, main.export['players']))[0]
                    
        elif type(arg) == str:
            player = list(filter(lambda player: utils.find_player_name(player).lower() == arg, main.export['players']))

        return player

class TeamConverter(commands.Converter):
    pass


