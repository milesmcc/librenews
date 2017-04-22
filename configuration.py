import json
import os
from userio import *

database_directory = None
# Get the directory (with trailing '/') of the database
def get_database_directory():
    global database_directory
    if database_directory is None:
        with open("config.json") as config:
            json_data = json.load(config)
            database_directory = json_data["database_directory"]
    return database_directory

twitter_credentials = None
# Get the twitter login credentials in the form of a dict
def get_twitter_credentials():
    global twitter_credentials
    if twitter_credentials is None:
        with open("config.json") as config:
            json_data = json.load(config)
            twitter_credentials = json_data["twitter"]
    return twitter_credentials

accounts = None
# Get an array of the user-meaningful handles of the news accounts
def get_accounts():
    global accounts
    if accounts = None:
        with open("config.json") as config:
            json_data = json.load(config)
            accounts = json_data["accounts"]
    return accounts

default_config = {
    "database_directory": "database/",
    "twitter": {
        "consumer_key": "XXXXX",
        "consumer_secret": "XXXXX",
        "access_token": "XXXXX",
        "access_token_secret": "XXXXX"
    },
    "accounts": [
        ["@BBCBreaking", "BBC"],
        ["@cnnbrk", "CNN"]
    ]
}

# Generate the default config. Will override existing config.
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
