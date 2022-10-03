#!/usr/bin/env bash

echo "$PATH" > /dev/stdout
tail -F /var/log/error.log > /dev/stdout &

uwsgi --ini uwsgi.ini 
