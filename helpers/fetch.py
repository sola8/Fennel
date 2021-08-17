import numpy as np
from decimal import Decimal as dec

import main

STATS_TO_AVERAGE = ['pts', 'orb', 'drb', 'ast']

# Checks and Counters
def is_playoff(stat):
    return (stat['playoffs'] is True 
            and stat['season'] == main.get_season() 
            and stat['gp'] > 0)

def is_regseason(stat):
    return (stat['playoffs'] is False 
            and stat['season'] == main.get_season() 
            and stat['gp'] > 0)

def regCount(stats):
    return sum(stat['playoffs'] is False
               and stat['gp'] > 0 
               for stat in stats)

def grab_season_stats(stats):

    season_stats = {

        'pts': 0.0,
        'orb': 0.0,
        'drb': 0.0,
        'ast': 0.0,
        'per': 0.0

    }

    games_played = sum([stat['gp'] for stat in stats if is_regseason(stat)])

    if games_played == 0:
        return season_stats
            
    for metric in STATS_TO_AVERAGE:
        season_stats[metric] = dec(sum([stat[metric] for stat in stats if is_regseason(stat)])/games_played)

    season_stats['per'] = np.mean([[stat['per'] for stat in stats if is_regseason(stat)]])

    # Round all values in dict
    season_stats = {key: round(value, 1) for key, value in season_stats.items()}
                            
    return season_stats

def grab_career_stats(stats):

    career_stats = {

        'pts': 0.0,
        'orb': 0.0,
        'drb': 0.0,
        'ast': 0.0,
        'per': 0.0,
        'ws': 0.0

    }

    game_total = sum([stat['gp'] for stat in stats if stat['playoffs'] is False])

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
