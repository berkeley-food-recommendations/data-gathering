#!/usr/bin/env python2.7

'''
Storing tweets as JSON:
  https://groups.google.com/forum/#!msg/tweepy/sFzCYVoGT68/EOg9xshgSM0J
'''

import argparse
import codecs
import collections
import os
import sys
import time
import tweepy
import unicodecsv

from auth_common import auth
from tweepy.utils import import_simplejson

json = import_simplejson()

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
    default='tweets/tweets.json',
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

class StreamListener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        self.start_time = time.time()
        self.time_limit = kwargs.get('time_limit', True)
        if 'time_limit' in kwargs:
            del kwargs['time_limit']

        self.outfile = kwargs['outfile']

        self.csv_writer = unicodecsv.writer(
            kwargs['outfile'],
            encoding='utf-8')
        del kwargs['outfile']

        self.stdout = kwargs['stdout']
        del kwargs['stdout']

        self.time = kwargs['time']
        del kwargs['time']

        self.unflushed_counter = 0

        super(StreamListener, self).__init__(*args, **kwargs)

    def on_data(self, data):
        json_data = json.loads(data)
        if 'disconnect' in json_data:
            print >>sys.stderr, data
            return False

        print >>self.outfile, data
        self.outfile.flush()

        if self.stdout:
            print data

        if self.time_limit and time.time() >= self.start_time + self.time:
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
        stdout=args['stdout'],
        time=args['time']),
    timeout=60)

# Roughly a bounding box for Berkeley
stream.filter(locations=[-122.3197, 37.8426, -122.2291, 37.8993])
