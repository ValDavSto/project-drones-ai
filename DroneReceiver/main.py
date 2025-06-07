import signal
import socket
import sys
from enum import Enum

def create_server(port: int) -> socket:
    """
    Creates a TCP server socket, binds it to the hostname and port, and starts listening.
    Args:
        port (int): The port on which the server should listen.
    Returns:
        socket: The created and listening server socket.
    """
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    print(f"Starting server on {hostname}:{port}")
    srv.bind((hostname, port))
    srv.listen(1)
    return srv

def close_server(srv: socket) -> None:
    """
    Closes the given server socket and terminates the program.
    Args:
        srv (socket): The server socket to close.
    """
    srv.close()
    print("Server closed.")
    sys.exit(0)

def receive_bytes(cli: socket, n: int) -> bytes:
    """
    Receives exactly n bytes from a client socket.
    Args:
        cli (socket): The client socket to receive from.
        n (int): The number of bytes to receive.
    Returns:
        bytes: The received bytes.
    Raises:
        ConnectionError: If the connection is closed before all data is received.
    """
    received = b''
    while len(received) < n:
        packet = cli.recv(n - len(received))
        if not packet:
            raise ConnectionError("Socket connection closed before receiving all data.")
        received += packet
    return received

APPLICATION_ACK = "DroneUAS".encode('utf-8')
def acknowledge_client(cli: socket) -> None:
    """
    Sends an application acknowledgement to the client and expects a confirmation.
    Args:
        cli (socket): The client socket.
    Raises:
        ConnectionError: If the client does not acknowledge the application.
    """
    cli.sendall(APPLICATION_ACK)
    if not receive_bytes(cli, len(APPLICATION_ACK)) == APPLICATION_ACK:
        raise ConnectionError("Client did not acknowledge the application.")

class Action(Enum):
    """
    Enum for possible actions that can be requested by the client.
    """
    PACKAGE_PICK = 0
    PACKAGE_DROP = 1

# Server setup
server = create_server(1337)
signal.signal(signal.SIGINT, lambda signum, frame: close_server(server))   # CTRL+C
signal.signal(signal.SIGTERM, lambda signum, frame: close_server(server))  # Termination

# Main loop to accept and handle client connections
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