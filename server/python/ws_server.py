import asyncio
import os
import ssl
from typing import Set

import websockets


CONNECTED: Set[websockets.WebSocketServerProtocol] = set()


async def handler(ws: websockets.WebSocketServerProtocol, path: str):
    CONNECTED.add(ws)
    try:
        async for message in ws:
            # broadcast to others
            await broadcast(message, sender=ws)
    finally:
        CONNECTED.remove(ws)


async def broadcast(message: str, sender=None):
    if not CONNECTED:
        return
    to_send = [ws for ws in CONNECTED if ws is not sender]
    if not to_send:
        return
    await asyncio.gather(*(ws.send(message) for ws in to_send), return_exceptions=True)


def _make_ssl_context():
    cert = os.path.join(os.path.dirname(__file__), 'cert.pem')
    key = os.path.join(os.path.dirname(__file__), 'key.pem')
    if os.path.exists(cert) and os.path.exists(key):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile=cert, keyfile=key)
        return ctx
    return None


def start(host: str = '0.0.0.0', port: int = 8765):
    """Start the asyncio websockets server. This blocks until cancelled."""
    ssl_ctx = _make_ssl_context()

    async def _serve_forever():
        async with websockets.serve(handler, host, port, ssl=ssl_ctx):
            await asyncio.Future()  # run forever

    # Use asyncio.run to create and manage the event loop in this thread
    asyncio.run(_serve_forever())


if __name__ == '__main__':
    start()
