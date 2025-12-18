"""Server entrypoint to run API and/or TCP websocket.

Usage:
  python main.py --api --ws
"""
import threading
import time
import argparse

try:
	import db_def
except Exception:
	db_def = None
import api as api_module
import gmail_call
import os

# support both legacy TCP websocket server (server/python/websocket.py)
# and an RFC WebSocket server (server/python/ws_server.py). Prefer RFC by default.
try:
	from ws_server import start as ws_server_start
except Exception:
	ws_server_start = None
try:
	import websocket as tcp_websocket
except Exception:
	tcp_websocket = None


def run_api(host='0.0.0.0', port=6700):
	api_module.run(host=host, port=port)


def run_ws():
	proto = os.getenv('NEXORA_WS_PROTO', 'ws').lower()
	if proto in ('ws', 'websocket') and ws_server_start:
		ws_server_start()
	elif proto in ('tcp',) and tcp_websocket:
		tcp_websocket.start()
	else:
		raise RuntimeError('No websocket server available for protocol: ' + proto)


def main():
	parser = argparse.ArgumentParser(description='Run Nexora server components')
	parser.add_argument('--api', action='store_true', help='Run HTTP API (Flask)')
	parser.add_argument('--ws', action='store_true', help='Run TCP websocket server')
	parser.add_argument('--all', action='store_true', help='Run both API and websocket')
	args = parser.parse_args()

	run_api_flag = args.api or args.all
	run_ws_flag = args.ws or args.all

	threads = []
	if run_api_flag:
		t = threading.Thread(target=run_api, daemon=False)
		t.start()
		threads.append(t)
	if run_ws_flag:
		t = threading.Thread(target=run_ws, daemon=False)
		t.start()
		threads.append(t)

	if not threads:
		parser.print_help()
		return

	try:
		for t in threads:
			t.join()
	except KeyboardInterrupt:
		pass


if __name__ == '__main__':
	main()