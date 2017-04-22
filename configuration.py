import json
import os
from userio import *

# There is no configuration caching because such a measure
# would be unnecessary -- it is unlikely that these methods
# are called very often, and therefore the performance
# trade-off is minimal. This also allows for configs
# to be changed in real-time without restarting the
# program.

# Get the directory (with trailing '/') of the database
def get_database_directory():
    with open("config.json") as config:
        json_data = json.load(config)
        return json_data["database_directory"]

# Get the twitter login credentials in the form of a dict
def get_twitter_credentials():
    with open("config.json") as config:
        json_data = json.load(config)
        return json_data["twitter"]

# Get an array of the user-meaningful handles of the news accounts
def get_accounts():
    with open("config.json") as config:
        json_data = json.load(config)
        return json_data["accounts"]

default_config = {
    "database_directory": "database/",
    "twitter": {
        "consumer_key": "XXXXX",
        "consumer_secret": "XXXXX",
        "access_token": "XXXXX",
        "access_token_secret": "XXXXX"
    },
    "accounts": ["BBCBreaking", "cnnbrk"]
}

def generate_config():
    warn("Generating default config...")
    with open("config.json", "w") as config:
        json.dump(default_config, config, indent=4, sort_keys=True)
        ok("Generated default config!")

if not os.path.exists("config.json"):
    warn("No configuration file found!")
    generate_config()
    say("Please edit the configuration file. LibreNews will now shutdown.")
    SystemExit
