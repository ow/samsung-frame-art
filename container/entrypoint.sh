#!/bin/bash

# Funktion, um das Python-Skript auszuführen
run_script() {
    python3 download_artwork.py
    sleep 30
    python3 art.py
}

# Endlosschleife, die alle 12 Stunden das Skript ausführt
while true; do
    run_script
    sleep 43200  # 12 Stunden warten
done
