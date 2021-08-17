def find_player_name(player):

    if len(player['lastName']) == 0:
        return player['firstName'].strip()

    if len(player['firstName']) == 0:
        return player['lastName'].strip()

    return player['firstName'].strip() + " " + player['lastName'].strip()