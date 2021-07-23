from bot import export

def find_player(player):
    if len(player['lastName']) == 0:
        return player['firstName'].strip()
    if len(player['firstName']) == 0:
        return player['lastName'].strip()
    return player['firstName'].strip() + " " + player['lastName'].strip()

async def fetch_player(inp1):
    for player in export['players']:
        if player['pid'] == inp1 or player['firstName'] == inp1:
            return player

async def fetch_stats(inp1):
    for player in export['players']:
        if player['pid'] == inp1 or player['firstName'] == inp1:
            return player['stats'][-1]
        
async def fetch_ratings(inp1):
    for player in export['players']:
        if player['pid'] == inp1 or player['firstName'] == inp1:
            return player['ratings'][-1]
  
async def fetch_team(tid):
    for team in export['teams']:
        if team['tid'] == tid:
            return team



