import socket
import threading
from typing import Optional


HEADER = 64
PORT = 8765
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.2"
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_listener_thread: Optional[threading.Thread] = None


def recv_exact(conn, n):
	data = bytearray()
	while len(data) < n:
		packet = conn.recv(n - len(data))
		if not packet:
			return None
		data.extend(packet)
	return bytes(data)


def recv_msg(conn):
	header = recv_exact(conn, HEADER)
	if not header:
		return None
	try:
		msg_len = int(header.decode(FORMAT).strip())
	except ValueError:
		return None
	if msg_len == 0:
		return ""
	payload = recv_exact(conn, msg_len)
	if payload is None:
		return None
	return payload.decode(FORMAT)


def send_msg(conn, msg: str):
	data = msg.encode(FORMAT)
	header = f"{len(data):<{HEADER}}".encode(FORMAT)
	conn.sendall(header + data)


def _listen_forever(conn):
	while True:
		try:
			msg = recv_msg(conn)
			if msg is None:
				print("[CLIENT] Server closed connection")
				break
			print(f"[CLIENT] Received: {msg}")
		except Exception as e:
			print(f"[CLIENT] Listener error: {e}")
			break


def start_listener():
	global _listener_thread
	if _listener_thread and _listener_thread.is_alive():
		return
	_listener_thread = threading.Thread(target=_listen_forever, args=(client,), daemon=True)
	_listener_thread.start()


def connect():
	try:
		client.connect(ADDR)
	except Exception as e:
		print(f"[CLIENT] Could not connect to {ADDR}: {e}")
		raise
	start_listener()


try:
	client.connect(ADDR)
	start_listener()
except Exception:
	pass