#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deepseek-api.py - Proxy fuer DeepSeek API mit STREAMING Support
/var/www/deepseek-chat/cgi-bin/deepseek-api.py
"""

import sys
import json
import os
import requests
from datetime import datetime

API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
API_URL = 'https://api.deepseek.com/v1/chat/completions'
LOG_PATH = '/var/www/deepseek-chat/cgi-bin/deepseek-chat.log'

def log_to_file(message):
    """Schreibt eine Nachricht ins Log"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} | {message}\n")
    except Exception as e:
        print(f"Log-Fehler: {e}", file=sys.stderr)

def send_error(status_code, message):
    """Sendet Fehlerantwort"""
    print(f"Status: {status_code}")
    print("Content-Type: application/json")
    print("Access-Control-Allow-Origin: *")
    print()
    print(json.dumps({"error": message}, ensure_ascii=False))
    sys.stdout.flush()

def main():
    """Hauptfunktion - handhabt Streaming von DeepSeek API"""
    try:
        # CORS Preflight
        if os.environ.get('REQUEST_METHOD') == 'OPTIONS':
            print("Status: 200 OK")
            print("Access-Control-Allow-Origin: *")
            print("Access-Control-Allow-Methods: POST, OPTIONS")
            print("Access-Control-Allow-Headers: Content-Type")
            print()
            sys.stdout.flush()
            return

        # Nur POST erlaubt
        if os.environ.get('REQUEST_METHOD') != 'POST':
            send_error(405, "Nur POST erlaubt")
            return

        # Request-Daten lesen
        content_length = int(os.environ.get('CONTENT_LENGTH', 0))
        if content_length == 0:
            send_error(400, "Keine Daten empfangen")
            return

        raw_data = sys.stdin.buffer.read(content_length)
        request_data = json.loads(raw_data.decode('utf-8'))

        # API-Key pruefen
        if not API_KEY:
            log_to_file("ERROR | API-Key fehlt in Umgebungsvariablen")
            send_error(500, "Server-Konfigurationsfehler")
            return

        # No-Training Option lesen (Standard: True = Daten NICHT fuer Training verwenden)
        no_training = request_data.get("no_training", True)

        # Request-Body vorbereiten
        api_request = {
            "model": request_data.get("model", "deepseek-chat"),
            "messages": request_data.get("messages", []),
            "max_tokens": request_data.get("max_tokens", 2000),
            "stream": True  # STREAMING AKTIVIEREN
        }

        # Logging
        ip = os.environ.get('REMOTE_ADDR', 'unknown')
        msg_count = len(api_request["messages"])
        log_to_file(f"IP: {ip} | REQUEST | {msg_count} messages | STREAMING | no_training: {no_training}")

        # HTTP Headers fuer Streaming senden
        print("Status: 200 OK")
        print("Content-Type: text/event-stream")
        print("Cache-Control: no-cache")
        print("Connection: keep-alive")
        print("Access-Control-Allow-Origin: *")
        print()
        sys.stdout.flush()

        # API-Headers vorbereiten
        api_headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # No-Training Header setzen (soweit von der API unterstuetzt)
        if no_training:
            api_headers["X-No-Training"] = "true"

        # DeepSeek API aufrufen mit Streaming
        response = requests.post(
            API_URL,
            headers=api_headers,
            json=api_request,
            stream=True  # WICHTIG: Stream aktivieren
        )

        if response.status_code != 200:
            error_text = response.text
            log_to_file(f"ERROR | DeepSeek API | Status {response.status_code} | {error_text}")
            # Fehler als Stream senden
            print(f"data: {json.dumps({'error': f'API-Fehler {response.status_code}'})}\n\n")
            sys.stdout.flush()
            return

        # Tokens streamen
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')

                # DeepSeek sendet: "data: {...}"
                if line_text.startswith('data: '):
                    # Direkt weiterleiten an Client
                    print(line_text)
                    sys.stdout.flush()

                    # Bei [DONE] ist Stream fertig
                    if '[DONE]' in line_text:
                        break

        # Stream abschliessen
        log_to_file(f"IP: {ip} | RESPONSE | Stream completed")

    except json.JSONDecodeError:
        log_to_file("ERROR | Ungueltige JSON-Daten empfangen")
        send_error(400, "Ungueltige JSON-Daten")
    except Exception as e:
        log_to_file(f"ERROR | {str(e)}")
        send_error(500, f"Interner Fehler: {str(e)}")

if __name__ == '__main__':
    main()

