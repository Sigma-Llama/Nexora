import asyncio
import websockets

connected = set()

async def server(websocket, path):
    connected.add(websocket)
    try:
        await asyncio.wait([ws.send("Hello!") for ws in connected])
        await asyncio.sleep(10)
    finally:
        connected.remove(websocket)
    async for message in websocket:
        await websocket.send(f'Got your msg its: {message}')

startServer = websockets.server(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(startServer)
asyncio.get_event_loop().run_forever()