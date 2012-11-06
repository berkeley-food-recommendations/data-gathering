#!/usr/bin/env bash

while true
do
    python streaming.py -u -of /var/log/twitter/tweets.csv 2>> /var/log/twitter/error.log
done
