import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CONFIG_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# Exports

LATEST_EXPORT = "https://raw.githubusercontent.com/nbsl-league/PCL-Exports/master/PCL-S27_ThirdCatch.json"
PREVIOUS_EXPORT = ""
OUTPUT_EXPORT_LOCATION = ""

# Bot Tokens
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Database Info
DB_URL = {}
DB_NAME = None
