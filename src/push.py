from pywebpush import webpush, WebPushException
import configuration
import thread
from pymongo import MongoClient
import userio
import json
client = MongoClient()

db = client.librenews

VAPID_CLAIMS = {
    "sub": "mailto:libre@rmrm.io"
}

def _is_valid_subscription(data):
    if ("endpoint" in data) and \
       ("keys" in data) and \
       ("auth" in data["keys"]) and \
       (len(json.dumps(data)) < 512):
        return True
    return False

# DO NOT CALL THIS FUNCTION FROM THE MAIN THREAD
# IT IS PRIVATE FOR A REASON
def _push_notification_to_subscribers(subscriptions, data):
    userio.say("Sending notification to " + str(subscriptions.count()) + " subscribers in a new thread...")
    for subscription in subscriptions:
        try:
            webpush(
                subscription_info=subscription,
                data=data,
                vapid_private_key=configuration.get_vapid_public_private_key_pair()[1],
                vapid_claims=VAPID_CLAIMS
            )
        except Exception as e:
            userio.error("    ...unable to send notification: " + str(e))
            db.subscriptions.remove(subscription)
            userio.say("    ...removed subscription!")
    userio.ok("Finished sending notification.")
    thread.exit()


def push_notification(flash):
    subscriptions = db.subscriptions.find()
    thread.start_new_thread(_push_notification_to_subscribers, (subscriptions, json.dumps(flash)))

def register_new_receiver(subscription_info):
    if _is_valid_subscription(subscription_info):
        db.subscriptions.insert_one(subscription_info)
        return True
    else:
        return False

def get_total_recipients():
    return db.subscriptions.find().count()

def get_application_server_key():
    return configuration.get_vapid_public_private_key_pair()[0]
