#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import os

SESSIONS_DIR = '/var/www/deepseek-chat/sessions'

def send_response(status_code, data):
    """Sendet HTTP-Response zurück."""
    print(f"Status: {status_code}")
    print("Content-Type: application/json")
    print("Access-Control-Allow-Origin: *")
    print("Access-Control-Allow-Methods: POST, OPTIONS")
    print("Access-Control-Allow-Headers: Content-Type")
    print()
    print(json.dumps(data, ensure_ascii=False))
    sys.stdout.flush()

def main():
    try:
        request_method = os.environ.get('REQUEST_METHOD', '')

        # OPTIONS Request
        if request_method == 'OPTIONS':
            send_response(200, {'status': 'ok'})
            return

        # Nur POST erlaubt
        if request_method != 'POST':
            send_response(405, {'error': f'Methode nicht erlaubt: {request_method}'})
            return

        # Content-Length lesen
        content_length = int(os.environ.get('CONTENT_LENGTH', 0))
        if content_length == 0:
            send_response(400, {'error': 'Leere Anfrage'})
            return

        # POST-Daten lesen
        post_data = sys.stdin.read(content_length)
        request_data = json.loads(post_data)
        session_id = request_data.get('sessionId')

        if not session_id:
            send_response(400, {'error': 'Keine Session-ID'})
            return

        # Session-Datei löschen
        session_file = os.path.join(SESSIONS_DIR, f'{session_id}.json')
        
        if not os.path.exists(session_file):
            send_response(404, {'error': 'Session nicht gefunden'})
            return

        os.remove(session_file)

        send_response(200, {
            'success': True,
            'message': 'Session erfolgreich gelöscht'
        })

    except json.JSONDecodeError as e:
        send_response(400, {'error': 'Ungültiges JSON', 'details': str(e)})
    except Exception as e:
        send_response(500, {'error': 'Interner Serverfehler', 'details': str(e)})

if __name__ == '__main__':
    main()

