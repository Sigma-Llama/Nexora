import importlib.util
import os
import json


def load_api_module():
    path = os.path.join(os.path.dirname(__file__), 'api.py')
    spec = importlib.util.spec_from_file_location('api_module', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_tests():
    mod = load_api_module()
    app = mod.app
    client = app.test_client()

    # Clear messages
    r = client.post('/api/clear')
    print('CLEAR status:', r.status_code, r.get_json())

    # Post a message
    payload = {'text': 'hello from local test', 'sender': 'local', 'room': 'room1'}
    r = client.post('/api/messages', json=payload)
    print('POST status:', r.status_code, r.get_json())

    # Get messages
    r = client.get('/api/messages')
    print('GET status:', r.status_code)
    print('GET body:', json.dumps(r.get_json(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    run_tests()
