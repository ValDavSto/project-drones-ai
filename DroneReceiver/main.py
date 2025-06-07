import signal
import socket
import sys
from enum import Enum

def create_server(port: int) -> socket:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    print(f"Starting server on {hostname}:{port}")
    srv.bind((hostname, port))
    srv.listen(1)
    return srv

def close_server(srv: socket) -> None:
    srv.close()
    print("Server closed.")
    sys.exit(0)

def receive_bytes(cli: socket, n: int) -> bytes:
    received = b''
    while len(received) < n:
        packet = cli.recv(n - len(received))
        if not packet:
            raise ConnectionError("Socket connection closed before receiving all data.")
        received += packet
    return received

APPLICATION_ACK = "DroneUAS".encode('utf-8')
def acknowledge_client(cli: socket) -> None:
    cli.sendall(APPLICATION_ACK)
    if not receive_bytes(cli, len(APPLICATION_ACK)) == APPLICATION_ACK:
        raise ConnectionError("Client did not acknowledge the application.")

class Action(Enum):
    PACKAGE_PICK = 0
    PACKAGE_DROP = 1

server = create_server(1337)
signal.signal(signal.SIGINT, lambda signum, frame: close_server(server))   # CTRL+C
signal.signal(signal.SIGTERM, lambda signum, frame: close_server(server))  # Termination

while True:
    client, clientAddress = server.accept()
    print(f"Connection from {clientAddress} has been established.")
    try:
        acknowledge_client(client)
        while True:
            match receive_bytes(client, 1)[0]:
                case Action.PACKAGE_PICK:
                    print(f"[CMD from {clientAddress}] Picking up package...")
                    # TODO: Implement package pick logic
                    pass
                case Action.PACKAGE_DROP:
                    print(f"[CMD from {clientAddress}] Dropping off package...")
                    # TODO: Implement package drop logic
                    pass
                case _:
                    raise ValueError("Unknown opcode received.")
    except Exception as error:
        print(error)
        print(f"Connection to {clientAddress} has been closed.")
    finally:
        client.close()