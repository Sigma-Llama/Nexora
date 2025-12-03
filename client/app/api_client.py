import requests
from typing import Optional

DEFAULT_BASE = 'https://127.0.0.1:5000'


def send_message(text: str, sender: Optional[str] = None, room: Optional[str] = None, base_url: str = DEFAULT_BASE, verify: bool = False):
    url = base_url.rstrip('/') + '/api/messages'
    payload = {'text': text}
    if sender:
        payload['sender'] = sender
    if room:
        payload['room'] = room
    r = requests.post(url, json=payload, verify=verify)
    r.raise_for_status()
    return r.json()


def get_messages(room: Optional[str] = None, base_url: str = DEFAULT_BASE, verify: bool = False):
    url = base_url.rstrip('/') + '/api/messages'
    params = {}
    if room:
        params['room'] = room
    r = requests.get(url, params=params, verify=verify)
    r.raise_for_status()
    return r.json()


def clear_messages(base_url: str = DEFAULT_BASE, verify: bool = False):
    url = base_url.rstrip('/') + '/api/clear'
    r = requests.post(url, verify=verify)
    r.raise_for_status()
    return r.json()


if __name__ == '__main__':
    try:
        print('Sending test message...')
        print(send_message('hello from client', sender='client-test', verify=False))
        print('Listing messages...')
        print(get_messages(verify=False))
    except Exception as e:
        print('API client error:', e)
