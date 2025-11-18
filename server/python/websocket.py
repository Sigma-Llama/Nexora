import socket
import threading


HEADER = 64
PORT = 8765
SERVER = "192.168.1.2" #socket.gethostbyname(socket.gethostname()) #"192.168.x.x"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[SERVER] New connection from {addr}")
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        msg_len = int(msg_len)
        msg = conn.recv(msg_len).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False

        print(f"[SERVER] Received from {addr}: {msg}")
    
    conn.close()


def start():
    server.listen()
    print(f"[SERVER] Listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[SERVER] Active connections: {threading.active_count() - 1}")


print("[SERVER] Starting server...")
start()