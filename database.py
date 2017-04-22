import os
import json
import uuid
import config

# A flash is a 'breaking news' notification.
def get_flash(text, source, time, link):
    return {
        "text": text,
        "source": source,
        "time": time,
        "link": link,
        "uuid": str(uuid.uuid1())
    }


def archive_flash(flash):
    with open(config.get_database_directory() + "flashes/" +
              flash["uuid"] + ".json", 'w') as flashfile:
        json.dump(flash, flashfile)

# add the flash as the latest in the cache and in the database
def push_flash(flash):
    pass

if not os.path.exists(config.get_database_directory() + "latest.json"):
    with open(config.get_database_directory() + "latest.json",
              'w') as latest_flashes_file:
        json.dump([], latest_flashes)

latest_flashes = []
with open(config.get_database_directory() + "latest.json",
          'r') as latest_flashes_file:
    latest_flashes = json.load(latest_flashes_file)
