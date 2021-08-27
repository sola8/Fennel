import numpy as np
from decimal import Decimal as dec

import main
from . import utils

STATS_TO_AVERAGE = ['pts', 'orb', 'drb', 'ast']

# Checks and Counters
def regCount(stats):
    return sum(stat['playoffs'] is False
               and stat['gp'] > 0 
               for stat in stats)

def fetch_current_season_stats(stats, season=main.get_season()):

    season_stats = {
        
        'gp': 0.0,
        'min': 0.0,
        'pts': 0.0,
        'orb': 0.0,
        'drb': 0.0,
        'ast': 0.0,
        'per': 0.0

    }

    games_played = sum([stat['gp'] for stat in stats if main.is_regseason(stat, season)])

    if games_played == 0:
        return season_stats
            
    for metric in STATS_TO_AVERAGE:
        season_stats[metric] = dec(sum([stat[metric] for stat in stats if main.is_regseason(stat, season)])/games_played)

    season_stats['per'] = np.mean([[stat['per'] for stat in stats if main.is_regseason(stat, season)]])

    # Round all values in dict
    season_stats = {key: round(value, 1) for key, value in season_stats.items()}
                            
    return season_stats

def fetch_career_stats(stats, season=main.get_season()):

    career_stats = {
        
        'gp': 0.0,
        'min': 0.0,
        'pts': 0.0,
        'orb': 0.0,
        'drb': 0.0,
        'ast': 0.0,
        'per': 0.0,
        'ws': 0.0

    }

    game_total = sum([stat['gp'] for stat in stats if stat['playoffs'] is False and stat['season'] <= season])

    if game_total == 0:
        return career_stats

    for metric in STATS_TO_AVERAGE:
        stat_total = sum([stat[metric] for stat in stats if stat['playoffs'] is False])
        career_stats[metric] = dec(stat_total/game_total)

    career_stats['per'] = dec(sum([stat['per'] for stat in stats if stat['playoffs'] is False]))/regCount(stats)
    career_stats['ws'] = dec(sum([stat['ows'] + stat['dws'] for stat in stats if stat['playoffs'] is False]))

    # Round all values in dict
    career_stats = {key: round(value, 1) for key, value in career_stats.items()}
                
    return career_stats

def fetch_player_data(pid, season=main.get_season()):
    # If on team,
    # Grab first name, last name, jersey number, season averages 
    playerDict = {

        'season': None,
        'jerseyNumber': None,
        'name': None,
        'pos': None,
        'age': None,
        'ovr': None,
        'pot': None,
        'type': None,
        'ability': None,
        'item': None,
        'imgURL': None,
        'ratings': {},
        'current_stats': {},
        'career_stats': {}

    }

    # Slow -- need to improve on this for roster command
    player = list(filter(lambda player: player["pid"] == pid, main.get_players()))[0]

    # General
    playerDict['season'] = season
    playerDict['name'] = utils.find_player_name(player)
    playerDict['imgURL'] = player["imgURL"]
    playerDict['item'] = player["college"]

    # Stats
    for stat in player["stats"]:
        if stat["season"] == season:

            playerDict['gp'] = stat["gp"]
            playerDict['jerseyNumber'] = stat["jerseyNumber"]

    playerDict['current_stats'] = fetch_current_season_stats(player['stats'], season)
    playerDict['career_stats'] = fetch_career_stats(player['stats'], season)

    # Ratings
    for rating in player["ratings"]:
        if rating["season"] == season:
            playerDict['ratings'] = rating
            playerDict['ovr'] = rating["ovr"]
            playerDict['pot'] = rating["pot"]
            playerDict['pos'] = rating["pos"]

    # Born
    playerDict['age'] = season - player["born"]["year"]
    playerDict['type'] = player["born"]["loc"].split(' ')[0]

    try:
        playerDict['ability'] = utils.find_player_ability(player)
    except IndexError:
        pass

    return playerDict

def fetch_team_data(tid, season=main.get_season()):

    teamDict = {

        'name': None,
        'record': None,
        'teamRating': None,
        'imgURL': None,
        'roster': []

    }

    team = list(filter(lambda team: team['tid'] == tid, main.export['teams']))[0]

    teamDict['name'] = team['region'] + " " + team['name']
    teamDict['imgURL'] = team['imgURL']

    for player in main.get_players():
        tempTID = None
        for stat in player['stats']:
            if stat['season'] == season:
                tempTID = stat['tid']
        if tempTID == tid and player['tid'] > -1:
            teamDict['roster'].append(fetch_player_data(player['pid'], season))

    for year in team["seasons"]:
        if year["season"] == season:
            teamDict['record'] = str(year["won"]) + "-" + str(year["lost"])
            teamDict['teamRating'] = utils.calculate_team_rating(teamDict)

    return teamDict
    
def create_roster_table(teamDict):
    
    roster = []
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

    return roster