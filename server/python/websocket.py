import socket
import threading


HEADER = 64
PORT = 8765


try:
    SERVER = socket.gethostbyname(socket.gethostname())
except Exception:
    SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)


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
    data = msg.encode(FORMAT)
    header = f"{len(data):<{HEADER}}".encode(FORMAT)
    conn.sendall(header + data)


def handle_client(conn, addr):
    
    try:
        while True:
            msg = recv_msg(conn)
            if msg is None:
                break
            if msg == DISCONNECT_MESSAGE:
                break
            
            
    except ConnectionResetError:
        pass
    except Exception:
        pass
    finally:
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