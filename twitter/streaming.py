#!/usr/bin/env python2.7

import argparse
import codecs
import collections
import os
import sys
import time
import tweepy
import unicodecsv

from auth_common import auth

parser = argparse.ArgumentParser(
    description='Record tweets from the Twitter /filter Streaming API')
parser.add_argument(
    '-t', '--time',
    default=10,
    type=int,
    help='Amount of time (in seconds) to listen to the sample stream.')
parser.add_argument(
    '-of',
    '--output-file',
    default='tweets/tweets.csv',
    help='File in which to store the streaming tweets')
parser.add_argument(
    '-u', '--unlimited',
    action='store_true',
    help='Disregard the time limit and run forever.')
parser.add_argument(
    '--stdout',
    action='store_true',
    help='Print each tweet to STDOUT')
args = vars(parser.parse_args())

class StatusUtils:
    @classmethod
    def get_coords(self, status):
        if status.coordinates:
            return '{0},{1}'.format(*status.coordinates[u'coordinates'])
        else:
            return ''

    @classmethod
    def get_place_coords(self, status):
        if status.place:
            return str(status.place[u'bounding_box'])
        else:
            return ''

class StreamListener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        self.start_time = time.time()
        self.time_limit = kwargs.get('time_limit', True)
        if 'time_limit' in kwargs:
            del kwargs['time_limit']

        self.csv_writer = unicodecsv.writer(
            kwargs['outfile'],
            encoding='utf-8')
        del kwargs['outfile']

        header = ['TweetID', 'User', 'Tweet', 'Coordinates', 'Place']
        if kwargs['stdout']:
            print ','.join(header)
        del kwargs['stdout']

        super(StreamListener, self).__init__(*args, **kwargs)

    def on_status(self, status):
        tweet_row = [status.id_str,
                     status.user.screen_name.lower(),
                     status.text,
                     StatusUtils.get_coords(status),
                     StatusUtils.get_place_coords(status)]
        self.csv_writer.writerow(tweet_row)
        if args['stdout']:
            print ','.join(tuple(tweet_row))

        if self.time_limit and time.time() >= self.start_time + args['time']:
            return False

outfile = open(
    os.path.abspath(
        os.path.expandvars(
            os.path.expanduser(args['output_file']))),
    'ab')
stream = tweepy.streaming.Stream(
    auth,
    StreamListener(
        time_limit=not args['unlimited'],
        outfile=outfile,
        stdout=args['stdout']),
    timeout=60)

# Roughly a bounding box for Berkeley
stream.filter(locations=[-122.3197, 37.8426, -122.2291, 37.8993])
