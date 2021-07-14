import json
import urllib.request

def load_json(filename, location):
    """
    Validates & loads a json file.
    """
    if location.upper() == "W":
        if filename.lower().startswith('http'):
            req = urllib.Request.request(filename)
        else:
            raise ValueError from None
        pass

        with urllib.request.urlopen(req) as f:
            return json.loads(f.read().decode('utf-8-sig'))

    if location.upper() == "L":
        with open(filename, encoding='utf-8') as f:
            return json.load(f)
        
    return None

def write_json(filename, content):
    """
    Updates a json file.
    """
    with open(filename, 'w') as o:
        json.dump(content, o)

def fetch_data():
    pass



