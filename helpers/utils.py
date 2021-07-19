import json
from os import stat
import urllib.request

from config import LATEST_EXPORT

stats_to_average = ['pts', 'reb', 'ast', 'stl', 'blk']

async def fetch_export(filename):
    """
    Validates & loads a BBGM export.
    """

    if filename.lower().startswith('http'):
        req = urllib.request.Request(filename)
    else:
        raise ValueError from None
    pass

    with urllib.request.urlopen(req) as f:
        return json.loads(f.read().decode('utf-8-sig'))

async def fetch_stats(pid):
    data = await fetch_export(LATEST_EXPORT)
    for player in data['players']:
        if player['pid'] == pid:
            return player['stats'][-1]

async def fetch_ratings(pid):
    data = await fetch_export(LATEST_EXPORT)
    for player in data['players']:
        if player['pid'] == pid:
            return player['ratings'][-1]

async def fetch_player(pid):
    data = await fetch_export(LATEST_EXPORT)
    for player in data['players']:
        if player['pid'] == pid:
            return player

async def fetch_team(tid):
    data = await fetch_export(LATEST_EXPORT)
    for team in data['teams']:
        if team['tid'] == tid:
            return team

def find_player(player):
    if len(player['lastName']) == 0:
        return player['firstName'].strip()
    if len(player['firstName']) == 0:
        return player['lastName'].strip()
    return player['firstName'].strip() + " " + player['lastName'].strip()


