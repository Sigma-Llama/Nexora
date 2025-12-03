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
import websocket as tcp_websocket
import api as api_module
import gmail_call


def run_api(host='0.0.0.0', port=5000):
	api_module.run(host=host, port=port)


def run_ws():
	tcp_websocket.start()


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