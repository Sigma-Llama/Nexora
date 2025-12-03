import importlib.util
import os
import json


def load_api_client():
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'api_client.py')
    spec = importlib.util.spec_from_file_location('api_client', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_tests():
    c = load_api_client()
    try:
        cleared = c.clear_messages(base_url='http://127.0.0.1:5000')
        print('CLEAR:', json.dumps(cleared, ensure_ascii=False))
    except Exception as e:
        print('CLEAR ERROR:', e)
    try:
        sent = c.send_message('hello from test', sender='tester', room='room1', base_url='http://127.0.0.1:5000')
        print('SEND:', json.dumps(sent, ensure_ascii=False))
    except Exception as e:
        print('SEND ERROR:', e)
    try:
        msgs = c.get_messages(base_url='http://127.0.0.1:5000')
        print('GET:', json.dumps(msgs, ensure_ascii=False))
    except Exception as e:
        print('GET ERROR:', e)


if __name__ == '__main__':
    run_tests()
