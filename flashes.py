#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configuration
import twitter
from userio import *
import tweepy
import tweepy
import re
from threading import Thread
import json

latest_flashes = []
link_regex = re.compile(r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»\"\"'']))")

def generate_flash(text, link, source, identifier, time):
    text = re.sub(link_regex, "", text)
    text = text.strip()
    return {
        "text": text,
        "link": link,
        "source": source,
        "id": identifier,
        "time": time
    }

is_sorted = False

def push_flash(flash):
    global is_sorted
    latest_flashes.append(flash)
    is_sorted = False

def sort_flashes():
    global latest_flashes
    latest_flashes = sorted(latest_flashes, key=lambda k: k["id"], reverse=True)
    is_sorted = True

def get_latest_flashes(num):
    global latest_flashes, is_sorted
    if not is_sorted:
        sort_flashes()
    return latest_flashes[:num]

def load_flashes():
    say("Loading latest flashes...")
    for accountPair in configuration.get_accounts():
        say("Loading flashes from Twitter account " + accountPair[0] + " (" + accountPair[1] + ")")
        latest_tweets = twitter.get_latest_statuses(accountPair[0][1:])
        for tweet in latest_tweets:
            url = None
            if "entities" in tweet:
                if "urls" in tweet['entities']:
                    if len(tweet['entities']['urls']) > 0:
                        url = tweet['entities']["urls"][0]['expanded_url']
            push_flash(
                generate_flash(tweet["text"], url, accountPair[1], tweet["id"], tweet["created_at"])
                )
        say("Loaded " + str(len(latest_tweets)) + " flashes from " + accountPair[0])
    ok("Loaded " + str(len(latest_flashes)) + " flashes")

class AccountListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            say("Detected flash...")
            if configuration.is_following(status.user.screen_name):
                say("...from a relevant source!")
                url = None
                if 'urls' in status.entities and len(status.entities['urls']) > 0:
                    url = status.entities['urls'][0]["expanded_url"]
                flash = generate_flash(status.text,
                                       url,
                                       configuration.get_name(status.user.screen_name),
                                       status.id,
                                       status.created_at)
                push_flash(flash)
                ok("Detected and pushed flash: " + str(flash))
            else:
                say("...from an irrelevant source.")
        except Exception as e:
            error("Encountered an exception while processing a flash: " + str(e))
        return True

    def on_error(self, status):
        error("Encountered an error while processing a status: " + str(status))
        if status == 420:
            #returning False in on_data disconnects the stream
            return False
        return True

def streamer_entrypoint():
    twitter_stream = tweepy.Stream(twitter.auth, AccountListener())
    twitter_stream.filter(follow=[str(twitter.get_id(k[0])) for k in configuration.get_accounts()], async=False)

def start_streamer():
    ok("Starting streamer...")
    thread = Thread(target = streamer_entrypoint)
    thread.setDaemon(True)
    thread.start()
    ok("Streamer started!")
