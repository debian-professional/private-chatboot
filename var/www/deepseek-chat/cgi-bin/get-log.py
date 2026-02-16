#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

# Korrekter Pfad zur Log-Datei (gleiches Verzeichnis wie die Python-Skripte)
LOG_FILE_PATH = '/var/www/deepseek-chat/cgi-bin/deepseek-chat.log'

# Content-Type Header für Plain-Text
print("Content-Type: text/plain; charset=utf-8")
print() # Leerzeile, um Header zu beenden

try:
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            if content:
                print(content, end='')
            else:
                print("Keine Log-Einträge vorhanden.")
    else:
        print(f"Log-Datei nicht gefunden unter: {LOG_FILE_PATH}")
except Exception as e:
    print(f"Fehler beim Lesen der Log-Datei: {str(e)}")
