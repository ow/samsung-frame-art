#!/usr/bin/env bash

cd /app
/usr/local/bin/python download.py
/usr/local/bin/python art.py --force-show
