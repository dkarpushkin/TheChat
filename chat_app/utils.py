import json
import logging

import redis
from django.utils import dateformat


def room_channel_name(room):
    return "room_{0}_message".format(room.slug)


def send_message(payload, channel_name):
    r = redis.StrictRedis()

    r.publish(channel_name, json.dumps(payload))
