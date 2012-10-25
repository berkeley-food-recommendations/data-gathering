#!/usr/bin/env python2.7

import argparse
import codecs
import collections
import sys
import time
import tweepy

from auth_common import auth

parser = argparse.ArgumentParser(
    description='Record tweets from the Twitter /filter Streaming API')
parser.add_argument(
    '-t', '--time',
    default=10,
    type=int,
    help='Amount of time (in seconds) to listen to the sample stream')
args = vars(parser.parse_args())

class StatusUtils:
    @classmethod
    def get_coords(self, status):
        if status.coordinates:
            return '"{0},{1}"'.format(*status.coordinates[u'coordinates'])
        else:
            return ''

    @classmethod
    def get_place_coords(self, status):
        if status.place:
            return '"' + str(status.place[u'bounding_box']) + '"'
        else:
            return ''

class StreamListener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        self.start_time = time.time()
        super(StreamListener, self).__init__(*args, **kwargs)

    def on_status(self, status):
        print ','.join([status.id_str,
                        status.user.screen_name.lower(),
                        status.text,
                        StatusUtils.get_coords(status),
                        StatusUtils.get_place_coords(status)])
        if time.time() >= self.start_time + args['time']:
            return False

stream = tweepy.streaming.Stream(auth, StreamListener(), timeout=60)
print 'TweetID,User,Tweet,Coordinates,Place'
# Roughly a bounding box for Berkeley
stream.filter(locations=[-122.3197, 37.8426, -122.2291, 37.8993])
