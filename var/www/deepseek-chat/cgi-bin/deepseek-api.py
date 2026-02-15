#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import os
import traceback
import urllib.request
import urllib.error

def send_response(status_code, data):
    """Sendet HTTP-Response zurück"""
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
        # API-Key aus Umgebungsvariable laden
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        
        if not api_key:
            send_response(500, {
                'error': 'API-Key nicht konfiguriert. Bitte DEEPSEEK_API_KEY in /etc/apache2/envvars setzen.'
            })
            return
        
        # Request-Methode prüfen
        request_method = os.environ.get('REQUEST_METHOD', '')
        
        # OPTIONS Request (CORS Preflight)
        if request_method == 'OPTIONS':
            send_response(200, {'status': 'ok'})
            return
        
        # Nur POST erlaubt
        if request_method != 'POST':
            send_response(405, {
                'error': f'Methode nicht erlaubt: {request_method}. Nur POST ist erlaubt.'
            })
            return
        
        # Content-Length lesen
        content_length = int(os.environ.get('CONTENT_LENGTH', 0))
        
        if content_length == 0:
            send_response(400, {
                'error': 'Leere Anfrage. Bitte model, messages und max_tokens senden.'
            })
            return
        
        # POST-Daten lesen
        post_data = sys.stdin.read(content_length)
        request_data = json.loads(post_data)
        
        # Validierung
        model = request_data.get('model', 'deepseek-chat')
        messages = request_data.get('messages', [])
        max_tokens = request_data.get('max_tokens', 2000)
        
        if not messages or not isinstance(messages, list):
            send_response(400, {
                'error': 'Ungueltige Anfrage: messages Array erforderlich'
            })
            return
        
        # DeepSeek API Request vorbereiten
        api_url = 'https://api.deepseek.com/v1/chat/completions'
        
        api_request_data = {
            'model': model,
            'messages': messages,
            'max_tokens': max_tokens
        }
        
        # HTTP Request an DeepSeek API
        req = urllib.request.Request(
            api_url,
            data=json.dumps(api_request_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            },
            method='POST'
        )
        
        # API-Aufruf durchführen
        with urllib.request.urlopen(req, timeout=60) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            send_response(200, response_data)
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        send_response(e.code, {
            'error': f'DeepSeek API Fehler: {e.code}',
            'details': error_body
        })
    
    except urllib.error.URLError as e:
        send_response(500, {
            'error': 'Verbindung zur DeepSeek API fehlgeschlagen',
            'details': str(e.reason)
        })
    
    except json.JSONDecodeError as e:
        send_response(400, {
            'error': 'Ungültiges JSON',
            'details': str(e)
        })
    
    except Exception as e:
        error_details = traceback.format_exc()
        
        send_response(500, {
            'error': 'Interner Serverfehler',
            'message': str(e),
            'details': error_details
        })

if __name__ == '__main__':
    main()
