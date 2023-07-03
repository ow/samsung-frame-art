#!/usr/bin/env bash

while true; do
  python download.py
  python art.py
  /bin/sleep $SLEEP_SECONDS
done
