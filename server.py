import socket
import threading
import json

# Changed from '127.0.0.1' to '0.0.0.0' to bind to all interfaces
HOST = '0.0.0.0'
PORT = 65432

# client_socket -> {'public_key': str, 'addr': (ip, port)}
clients = {}
clients_lock = threading.Lock()


def _remove_client(client_socket):
    try:
        client_socket.close()
    except Exception:
        pass
    with clients_lock:
        clients.pop(client_socket, None)


def send_keys_update():
    """Send updated list of public keys to all connected clients."""
    with clients_lock:
        keys = {str(info['addr']): info['public_key'] for info in clients.values()}
        payload = json.dumps(keys).encode()
        sockets = list(clients.keys())

    for sock in sockets:
        try:
            sock.send(payload)
        except Exception:
            _remove_client(sock)


def broadcast(message, sender_socket):
    with clients_lock:
        recipients = [s for s in clients.keys() if s is not sender_socket]

    for sock in recipients:
        try:
            sock.send(message)
        except Exception:
            _remove_client(sock)


def handle_client(client_socket):
    addr = None
    try:
        pubkey_data = client_socket.recv(4096).decode()
        addr = client_socket.getpeername()

        with clients_lock:
            clients[client_socket] = {'public_key': pubkey_data, 'addr': addr}

        print(f"Received public key from {addr}")
        send_keys_update()

        while True:
            message = client_socket.recv(8192)
            if not message:
                break
            broadcast(message, client_socket)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if addr is not None:
            print(f"Connection closed {addr}")
        _remove_client(client_socket)
        send_keys_update()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    # Get the actual IP address of the machine
    import socket as sock
    local_ip = sock.gethostbyname(sock.gethostname())
    print(f"Server started on {HOST}:{PORT}")
    print(f"Local IP address: {local_ip}")
    print("To connect from other devices on the same network, use this IP address")

    while True:
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()