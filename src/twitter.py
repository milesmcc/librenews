import configuration
import tweepy
from userio import say

twitter_credentials = configuration.get_twitter_credentials()

auth = tweepy.OAuthHandler(twitter_credentials["consumer_key"],
                           twitter_credentials["consumer_secret"])
auth.set_access_token(twitter_credentials["access_token"],
                      twitter_credentials["access_token_secret"])

api = tweepy.API(auth)

id_cache = {}


def get_id(username):
    if username not in id_cache:
        id_cache[username] = api.get_user(username).id
    return id_cache[username]


def get_latest_statuses(username):
    say("Gathering latest statuses from " + username)
    return [status._json for status in api.user_timeline(username)]
