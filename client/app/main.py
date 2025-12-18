"""Client entrypoint.

Default: run the GUI. Use `--test-api` or `--test-ws` for simple tests.
"""

import argparse
import time
import threading
import os

import ws_client as ws_client
from api_client import send_message, get_messages


def test_api(base_url: str):
	print(f'Testing API (to {base_url}, verify=False)')
	try:
		send_message('hello from client main', sender='gui-test', room='test', base_url=base_url, verify=False)
		msgs = get_messages(base_url=base_url, verify=False)
		print('Messages:', msgs)
	except Exception as e:
		print('API test error:', e)


def test_ws(ws_host: str, ws_port: int):
	print(f'Testing WebSocket (connect/send/disconnect) -> {ws_host}:{ws_port}')
	try:
		url = f"ws://{ws_host}:{ws_port}"
		ws_client.set_on_message(lambda m: print('WS RECV TEST:', m))
		ws_client.connect(url)
		# wait for connection
		import time
		time.sleep(0.5)
		if ws_client.is_connected():
			ws_client.send('hello from client main')
			ws_client.send(ws_client.DISCONNECT_MESSAGE)
		else:
			print('WebSocket not connected')
	except Exception as e:
		print('Websocket test error:', e)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--test-api', action='store_true')
	parser.add_argument('--test-ws', action='store_true')
	parser.add_argument('--nogui', action='store_true')
	parser.add_argument('--base-url', default=os.getenv('NEXORA_BASE_URL', 'http://127.0.0.1:6700'))
	parser.add_argument('--ws-host', default=os.getenv('NEXORA_WS_HOST', '127.0.0.1'))
	parser.add_argument('--ws-port', type=int, default=int(os.getenv('NEXORA_WS_PORT', '8765')))
	args = parser.parse_args()

	if args.test_api:
		test_api(args.base_url)
		return
	if args.test_ws:
		test_ws(args.ws_host, args.ws_port)
		return
	if args.nogui:
		print('No-GUI mode: running API test')
		test_api(args.base_url)
		return

	# Default: run single-file Discord-like GUI
	from window import run_discord_like
	run_discord_like(base_url=args.base_url)


if __name__ == '__main__':
	main()