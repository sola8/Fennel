import os
import json
import csv
from pathlib import Path

# CSV funcs
def isnumber(v):
    try:
        int(v)
    except ValueError:
        return False
    return True

def get_data_from(filename):
    path = Path(__name__).parent / "csv" / filename

    with open(path) as f:
        reader = csv.DictReader(f)
        data = list(
            {k: int(v) if isnumber(v) else v for k, v in row.items() if v != ""}
            for row in reader
        )

    return data

def get_pokemon():
    species = [None] + get_data_from("pokedex.csv")
    evolution = {}
    pokemon = {}

    def get_evolution_trigger():
        pass

def get_item():
    pass

def get_ability():
    pass

# Export funcs
def get_latest_export():
    pass

def get_player():
    pass

def get_team():
    pass
