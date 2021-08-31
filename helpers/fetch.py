from discord import player
import numpy as np
from decimal import Decimal as dec

from main import get_teams, get_players, get_season, is_regseason
from . import utils

STATS_TO_AVERAGE = ['pts', 'orb', 'drb', 'ast']

# Checks and Counters
def regCount(stats):
    return sum(stat['playoffs'] is False
               and stat['gp'] > 0 
               for stat in stats)

def fetch_current_season_stats(stats, season=get_season()):

    season_stats = {
        
        'gp': 0.0,
        'min': 0.0,
        'pts': 0.0,
        'orb': 0.0,
        'drb': 0.0,
        'ast': 0.0,
        'per': 0.0

    }

    games_played = sum([stat['gp'] for stat in stats if is_regseason(stat, season)])

    if games_played == 0:
        return season_stats
            
    for metric in STATS_TO_AVERAGE:
        season_stats[metric] = dec(sum([stat[metric] for stat in stats if is_regseason(stat, season)])/games_played)

    season_stats['per'] = np.mean([[stat['per'] for stat in stats if is_regseason(stat, season)]])

    # Round all values in dict
    season_stats = {key: round(value, 1) for key, value in season_stats.items()}
                            
    return season_stats

def fetch_career_stats(stats, season=get_season()):

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

def fetch_player_data(pid, season=get_season()):
    # If on team,
    # Grab first name, last name, jersey number, season averages 
    playerDict = {
        
        'pid': None,
        'tid': None,
        'season': None,
        'jerseyNumber': "[-]",
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
    try:
        player = list(filter(lambda player: player["pid"] == pid, get_players()))[0]
    except IndexError:
        return playerDict

    # General
    playerDict['season'] = season
    playerDict['name'] = utils.find_player_name(player)
    playerDict['imgURL'] = player["imgURL"]

    if not player["college"]:
        pass
    else:
        playerDict['item'] = player["college"]

    playerDict['pid'] = player["pid"]
    playerDict['tid'] = player["tid"]

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

    if not playerDict['ratings']:

        playerDict['ratings'] = player['ratings'][-1]

        try:
            playerDict['jerseyNumber'] = player['stats'][-1]['jerseyNumber']
        except IndexError:
            pass

    # Born
    playerDict['age'] = season - player["born"]["year"]
    playerDict['type'] = player["born"]["loc"].split(' ')[0]

    playerDict['ability'] = utils.find_player_ability(player)

    return playerDict

def fetch_team_data(tid, season=get_season()):

    teamDict = {

        'name': None,
        'imgURL': None,
        'colors': [],

    }

    try: 
        team = list(filter(lambda team: team['tid'] == tid, get_teams()))[0]

    except IndexError:

        if tid == -1:
            teamDict['name'] = "Free Agent"

        if tid == -2:
            teamDict['name'] = "Undrafted"
        
        if tid == -3:
            teamDict['name'] = "Retired"

        return teamDict

    for year in team["seasons"]:
        if year["season"] == season:
            teamDict['name'] = team["region"] + " " + team["name"]
            teamDict['imgURL'] = team["imgURL"]
            teamDict['colors'] = team["colors"]

    return teamDict

def fetch_free_agents():
    player = list(filter(lambda player: player['tid'] == -1, get_players()))
    cleaned_players = [fetch_player_data(play['pid']) for play in player]
    sorted_pool = sorted(cleaned_players, key=lambda k: k['ovr'], reverse=True) 
    return sorted_pool