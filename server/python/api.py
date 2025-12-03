from flask import Flask, request, jsonify
import os
import json
from threading import Lock
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
MSG_FILE = os.path.join(DATA_DIR, 'messages.json')
if not os.path.exists(MSG_FILE):
    with open(MSG_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

_lock = Lock()

app = Flask(__name__)


def load_messages():
    with _lock:
        with open(MSG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)


def save_messages(messages):
    with _lock:
        with open(MSG_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)


@app.route('/api/messages', methods=['GET'])
def get_messages():
    room = request.args.get('room')
    messages = load_messages()
    if room:
        messages = [m for m in messages if m.get('room') == room]
    return jsonify(messages), 200


@app.route('/api/messages', methods=['POST'])
def post_message():
    if not request.is_json:
        return jsonify({'error': 'expected application/json'}), 400
    payload = request.get_json()
    if 'text' not in payload:
        return jsonify({'error': 'missing field: text'}), 400
    message = {
        'text': payload.get('text'),
        'sender': payload.get('sender'),
        'room': payload.get('room'),
        'ts': datetime.utcnow().isoformat() + 'Z'
    }
    messages = load_messages()
    messages.append(message)
    save_messages(messages)
    return jsonify({'status': 'ok', 'message': message}), 201


@app.route('/api/clear', methods=['POST'])
def clear_messages():
    save_messages([])
    return jsonify({'status': 'cleared'}), 200


def run(host='0.0.0.0', port=5000):
    cert = os.path.join(BASE_DIR, 'cert.pem')
    key = os.path.join(BASE_DIR, 'key.pem')
    if os.path.exists(cert) and os.path.exists(key):
        ssl_context = (cert, key)
        print(f"[API] Running HTTPS on https://{host}:{port}")
        app.run(host=host, port=port, ssl_context=ssl_context)
    else:
        print('[API] Certificate or key not found; running HTTP. To enable HTTPS, place cert.pem and key.pem in this folder.')
        print(f"[API] Running HTTP on http://{host}:{port}")
        app.run(host=host, port=port)


if __name__ == '__main__':
    run()
