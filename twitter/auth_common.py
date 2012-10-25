import tweepy

from twitter_keys import *

'''
Sourced from https://github.com/tweepy/tweepy/blob/master/examples/oauth.py
'''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
