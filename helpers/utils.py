import math
from tabulate import tabulate
import re

def bound(num: int, min: int, max: int):
	if num < min:
		return min

	if num > max:
		return max

	return num

def find_player_name(player):

    if len(player['lastName']) == 0:
        return player['firstName'].strip()

    if len(player['firstName']) == 0:
        return player['lastName'].strip()

    return player['firstName'].strip() + " " + player['lastName'].strip()

def find_player_type(player):
    # Split
    type_ability = player["born"]["loc"].split(' ')

    return type_ability[0]

def find_player_ability(player):
    try:
        ability = player["born"]["loc"].split(' ')[1].replace('(', '').replace(')', '').strip() + " " +  player["born"]["loc"].split(' ')[2].replace('(', '').replace(')', '').strip()
    except IndexError:
        ability = None
    return ability

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


def create_roster_table(teamDict):
    
    roster = []
    fields = ['#', 'name', 'pos', 'age', 'ovr', 'pot', 'pts', 'reb', 'ast', 'per']
    teamDict['roster'] = sorted(teamDict['roster'], key=lambda k: k['ovr'], reverse=True)

    for player in teamDict['roster']:

        player_line = []
        
        # Find a better way to do this...

        player_line.append(player['jerseyNumber'])
        player_line.append(player['name'])
        player_line.append(player['pos'])
        player_line.append(player['age'])
        player_line.append(player['ovr'])
        player_line.append(player['pot'])
        
        player_line.append(player['current_stats']['pts'])
        player_line.append(player['current_stats']['drb'] + player['current_stats']['orb'])
        player_line.append(player['current_stats']['ast'])
        player_line.append(player['current_stats']['per'])

        roster.append(player_line)

    roster = tabulate(roster, headers=fields, floatfmt=".1f")
    return roster
