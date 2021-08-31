import math
import re

import discord

def bound(num: int, min: int, max: int):
	if num < min:
		return min

	if num > max:
		return max

	return num

def find_team_color(teamDict):
    if not teamDict['colors']:
        return discord.Color.dark_purple()
    else:
        team_color = int(teamDict['colors'][0].replace("#", ""),16)
        return int(hex(team_color), 0)

        
def find_player_name(player):

    if len(player['lastName']) == 0:
        return player['firstName'].strip()

    if len(player['firstName']) == 0:
        return player['lastName'].strip()

    return player['firstName'].strip() + " " + player['lastName'].strip()

def find_player_type(player):
    # Split
    type = player["born"]["loc"].split(' ')

    return type[0]

def find_player_ability(player):
    
    try:
        ability = player["born"]["loc"]
        ability = re.search('\(([^)]+)', ability).group(1)
    except (AttributeError, IndexError):
        ability = re.search('\(([^)]+)', ability)

    return ability

def find_player_rarity(player):
    
    try:
        rarity = find_player_name(player)
        rarity = re.search('\(([^)]+)', rarity).group(1)
    except (AttributeError, IndexError):
        rarity = re.search('\(([^)]+)', rarity)

    return rarity

def find_player_nickname(player):
    
    if "\"" in find_player_name(player): 
        nickname = re.findall(r'"([^"]*)"', find_player_name(player))

        if nickname is None:
            return

        return nickname

def calculate_team_rating(teamDict):

    ratings = []
    newlist = sorted(teamDict['roster'], key=lambda k: k['ovr'], reverse=True) 

    for i in range(10):
        try:
            ratings.append(newlist[i]['ovr'])
        except IndexError:
            ratings.append(0)

    predictedMOV = (-124.13 + 
                    0.4417 * math.exp(-0.1905 * 0) * ratings[0] + 
                    0.4417 * math.exp(-0.1905 * 1) * ratings[1] + 
                    0.4417 * math.exp(-0.1905 * 2) * ratings[2] + 
                    0.4417 * math.exp(-0.1905 * 3) * ratings[3] +
		            0.4417 * math.exp(-0.1905 * 4) * ratings[4] +
                    0.4417 * math.exp(-0.1905 * 5) * ratings[5] +
                    0.4417 * math.exp(-0.1905 * 6) * ratings[6] +
                    0.4417 * math.exp(-0.1905 * 7) * ratings[7] +
                    0.4417 * math.exp(-0.1905 * 8) * ratings[8] +
                    0.4417 * math.exp(-0.1905 * 9) * ratings[9])

    rawOVR = (predictedMOV * 50) / 20 + 50

    return bound(round(rawOVR), 0, math.inf)
