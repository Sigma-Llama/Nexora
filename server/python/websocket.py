import socket
import threading
import os


HEADER = 64
PORT = int(os.getenv('NEXORA_WS_PORT', '8765'))
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Bind to all interfaces in container environments
SERVER = '0.0.0.0'
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

# track connected clients for broadcasting
clients = []
clients_lock = threading.Lock()


def recv_exact(conn, n):
    """Receive exactly n bytes or return None if connection closed."""
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
    try:
        data = msg.encode(FORMAT)
        header = f"{len(data):<{HEADER}}".encode(FORMAT)
        conn.sendall(header + data)
    except Exception:
        # caller will handle removal of dead clients
        raise


def broadcast(msg: str, exclude_conn=None):
    with clients_lock:
        for c in list(clients):
            if c is exclude_conn:
                continue
            try:
                send_msg(c, msg)
            except Exception:
                try:
                    c.close()
                except Exception:
                    pass
                try:
                    clients.remove(c)
                except ValueError:
                    pass


def handle_client(conn, addr):
    with clients_lock:
        clients.append(conn)

    try:
        while True:
            msg = recv_msg(conn)
            if msg is None:
                break
            if msg == DISCONNECT_MESSAGE:
                break
            # broadcast received message to all other clients
            broadcast(msg, exclude_conn=conn)

    except ConnectionResetError:
        pass
    except Exception:
        pass
    finally:
        with clients_lock:
            try:
                clients.remove(conn)
            except ValueError:
                pass
        try:
            conn.close()
        except Exception:
            pass


def start():
    server.listen(5)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()


if __name__ == '__main__':
    start()