import threading
import os
from typing import Optional, Callable

import importlib
import sys
import os

# Import the installed `websocket` package while avoiding local module name collisions
_local_dir = os.path.dirname(__file__)
_removed = False
if _local_dir in sys.path:
    try:
        sys.path.remove(_local_dir)
        _removed = True
    except ValueError:
        _removed = False
try:
    _ws_lib = importlib.import_module('websocket')
finally:
    if _removed:
        sys.path.insert(0, _local_dir)


_ws_app: Optional[object] = None
_thread: Optional[threading.Thread] = None
_on_message: Optional[Callable[[str], None]] = None


def set_on_message(cb: Callable[[str], None]):
    global _on_message
    _on_message = cb


def _on_ws_message(ws, message):
    if _on_message:
        try:
            _on_message(message)
        except Exception:
            pass
    else:
        print('WS RECV:', message)


def _on_ws_error(ws, err):
    print('WS ERROR:', err)


def _on_ws_close(ws, close_status_code, close_msg):
    print('WS CLOSED:', close_status_code, close_msg)


def _on_ws_open(ws):
    print('WS OPEN')


def connect(url: Optional[str] = None):
    """Connect to a ws:// or wss:// URL. Starts listener thread."""
    global _ws_app, _thread
    if url is None:
        host = os.getenv('NEXORA_WS_HOST', '127.0.0.1')
        port = os.getenv('NEXORA_WS_PORT', '8765')
        scheme = os.getenv('NEXORA_WS_SCHEME', 'ws')
        url = f"{scheme}://{host}:{port}"

    _ws_app = _ws_lib.WebSocketApp(url,
                                    on_open=_on_ws_open,
                                    on_message=_on_ws_message,
                                    on_error=_on_ws_error,
                                    on_close=_on_ws_close)

    def run():
        try:
            _ws_app.run_forever()
        except Exception as e:
            print('WS run_forever error:', e)

    _thread = threading.Thread(target=run, daemon=True)
    _thread.start()
    return _ws_app


def send(msg: str):
    if _ws_app and _ws_app.sock and _ws_app.sock.connected:
        _ws_app.send(msg)
    else:
        raise RuntimeError('WebSocket not connected')


def close():
    if _ws_app:
        try:
            _ws_app.close()
        except Exception:
            pass


def is_connected() -> bool:
    return bool(_ws_app and _ws_app.sock and _ws_app.sock.connected)


DISCONNECT_MESSAGE = "!DISCONNECT"
