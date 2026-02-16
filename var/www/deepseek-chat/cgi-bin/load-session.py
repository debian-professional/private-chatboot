#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import os
import datetime

SESSIONS_DIR = '/var/www/deepseek-chat/sessions'

def send_response(status_code, data):
    """Sendet HTTP-Response zurück."""
    print(f"Status: {status_code}")
    print("Content-Type: application/json")
    print("Access-Control-Allow-Origin: *")
    print("Access-Control-Allow-Methods: GET, POST, OPTIONS")
    print("Access-Control-Allow-Headers: Content-Type")
    print()
    print(json.dumps(data, ensure_ascii=False))
    sys.stdout.flush()

def get_session_preview(session_file):
    """Liest Session-Datei und erstellt Vorschau."""
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = data.get('messages', [])
        first_user_msg = next((msg['content'][:50] for msg in messages if msg['role'] == 'user'), 'Keine Nachricht')
        
        return {
            'sessionId': os.path.basename(session_file).replace('.json', ''),
            'timestamp': data.get('timestamp', ''),
            'messageCount': len(messages),
            'preview': first_user_msg,
            'settings': data.get('settings', {})
        }
    except:
        return None

def main():
    try:
        request_method = os.environ.get('REQUEST_METHOD', '')

        # OPTIONS Request
        if request_method == 'OPTIONS':
            send_response(200, {'status': 'ok'})
            return

        # GET = Liste aller Sessions, POST = Spezifische Session laden
        if request_method == 'GET':
            # Liste aller Sessions zurückgeben
            if not os.path.exists(SESSIONS_DIR):
                send_response(200, {'sessions': []})
                return

            sessions = []
            for filename in sorted(os.listdir(SESSIONS_DIR), reverse=True):
                if filename.endswith('.json'):
                    session_file = os.path.join(SESSIONS_DIR, filename)
                    preview = get_session_preview(session_file)
                    if preview:
                        sessions.append(preview)

            send_response(200, {'sessions': sessions})

        elif request_method == 'POST':
            # Spezifische Session laden
            content_length = int(os.environ.get('CONTENT_LENGTH', 0))
            if content_length == 0:
                send_response(400, {'error': 'Leere Anfrage'})
                return

            post_data = sys.stdin.read(content_length)
            request_data = json.loads(post_data)
            session_id = request_data.get('sessionId')

            if not session_id:
                send_response(400, {'error': 'Keine Session-ID'})
                return

            session_file = os.path.join(SESSIONS_DIR, f'{session_id}.json')
            if not os.path.exists(session_file):
                send_response(404, {'error': 'Session nicht gefunden'})
                return

            with open(session_file, 'r', encoding='utf-8') as f:
                chat_data = json.load(f)

            send_response(200, {
                'success': True,
                'chatData': chat_data
            })

        else:
            send_response(405, {'error': f'Methode nicht erlaubt: {request_method}'})

    except json.JSONDecodeError as e:
        send_response(400, {'error': 'Ungültiges JSON', 'details': str(e)})
    except Exception as e:
        send_response(500, {'error': 'Interner Serverfehler', 'details': str(e)})

if __name__ == '__main__':
    main()
