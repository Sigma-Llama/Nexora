domain_gui.domain()
"""Client entrypoint. By default it runs the GUI; for testing use --test-api or --test-ws."""
import argparse
import time
import threading

import login_sigin_gui
import app_gui
import domain_gui
import websocket as ws_client
from api_client import send_message, get_messages


def run_gui():
	domain_gui.domain()
	login_sigin_gui.loginSignup()


def test_api():
	print('Testing API (via HTTPS to https://127.0.0.1:5000, verify=False)')
	try:
		send_message('hello from client main', sender='gui-test', room='test', base_url='https://127.0.0.1:5000', verify=False)
		msgs = get_messages(base_url='https://127.0.0.1:5000', verify=False)
		print('Messages:', msgs)
	except Exception as e:
		print('API test error:', e)


def test_ws():
	print('Testing TCP websocket (connect/send/disconnect)')
	try:
		ws_client.connect()
		ws_client.send_msg(ws_client.client, 'hello from client main')
		ws_client.send_msg(ws_client.client, '!DISCONNECT')
	except Exception as e:
		print('Websocket test error:', e)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--test-api', action='store_true')
	parser.add_argument('--test-ws', action='store_true')
	parser.add_argument('--nogui', action='store_true')
	args = parser.parse_args()

	if args.test_api:
		test_api()
		return
	if args.test_ws:
		test_ws()
		return
	if args.nogui:
		print('No-GUI mode: running API test')
		test_api()
		return

	# Default: run single-file Discord-like GUI
	from window import run_discord_like
	run_discord_like()


if __name__ == '__main__':
	main()