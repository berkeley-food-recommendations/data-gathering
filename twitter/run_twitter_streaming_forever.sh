#!/usr/bin/env bash

while true
do
    python streaming.py -u -of /var/log/twitter/tweets.json 2>> /var/log/twitter/error.log
    sleep 1
done
