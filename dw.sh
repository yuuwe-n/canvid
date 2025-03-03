#!/bin/sh

# $1 is the srt file

URL=$(pbpaste)

. myenv/bin/activate
python3 download.py "$URL" "$1"
