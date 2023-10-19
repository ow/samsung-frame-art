#!/usr/bin/env bash

mkdir -p /share/samsung-frame-art/images
rm -rf /app/images
ln -s /share/samsung-frame-art/images /app/images
ls -la /app/images/

cd /app
/usr/local/bin/python download.py
/usr/local/bin/python art.py --force-show
