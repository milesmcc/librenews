import json
import os
import sys

from userio import ok, say, warn

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
    if accounts is None:
        with open("config.json") as config:
            json_data = json.load(config)
            accounts = json_data["accounts"]
    return accounts

def get_vapid_public_private_key_pair():
    with open("config.json") as config:
        json_data = json.load(config)
        return (json_data["vapid"]["public_key"], json_data["vapid"]["private_key"])

# key = None
#
# def get_gcm_key():
#     global key
#     if key is None:
#         with open("config.json") as config:
#             json_data = json.load(config)
#             key = json_data["gcm_key"]

def is_following(username):
    for account in get_accounts():
        if username == account[0] or '@' + username == account[0]:
            return True
    return False


default_config = {
    "twitter": {
        "consumer_key": "XXXXX",
        "consumer_secret": "XXXXX",
        "access_token": "XXXXX",
        "access_token_secret": "XXXXX"
    },
    "accounts": [
        ["@BBCBreaking", "BBC", "Breaking News"],
        ["@LibreNewsApp", "LibreNews", "Announcements"]
    ],
    "vapid": {
        "private_key": "XXXXX",
        "public_key": "XXXXX",
    }
}

names = None

def get_name(handle):
    global names
    if names is None:
        names = {}
        for account in get_accounts():
            names[account[0]] = account[1]
            names[account[0][1:]] = account[1]
            # so that @names defined in config still match
    return names[handle]


channels = None


def get_channel(handle):
    global channels
    if channels is None:
        channels = {}
        for account in get_accounts():
            channels[account[0]] = account[2]
            channels[account[0][1:]] = account[2]
            # so that @names defined in config still match
    return channels[handle]


# Generate the default config. Will override existing config.
def generate_config():
    warn("Generating default config...")
    with open("config.json", "w") as config:
        json.dump(default_config, config, indent=4, sort_keys=True)
        ok("Generated default config!")


if not os.path.exists("config.json"):
    warn("No configuration file found!")
    generate_config()
    say("Please edit the configuration file. LibreNews Server will now shutdown.")
    sys.exit(1)
