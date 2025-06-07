import signal
import socket
import sys
import enum
import gpiozero

# [SECTION]: Communication

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

class Action(enum.Enum):
    """
    Enum for possible actions that can be requested by the client.
    """
    DISCONNECT = 0
    PACKAGE_PICK = 1
    PACKAGE_DROP = 2

# [SECTION]: Hardware

def activate_magnet() -> None:
    """
    Activates the magnet for package handling.
    """
    print("Activating magnet...")
    magnet.on()

def deactivate_magnet() -> None:
    """
    Deactivates the magnet after package handling.
    """
    print("Deactivating magnet...")
    magnet.off()

# [SECTION]: Main

# Server setup
server = create_server(1337)
signal.signal(signal.SIGINT, lambda signum, frame: close_server(server))   # CTRL+C
signal.signal(signal.SIGTERM, lambda signum, frame: close_server(server))  # Termination

# GPIO setup
magnet = gpiozero.LED(23)

# Main loop to accept and handle client connections
while True:
    client, clientAddress = server.accept()
    print(f"Connection from {clientAddress} has been established.")
    try:
        acknowledge_client(client)
        while True:
            match receive_bytes(client, 1)[0]:
                case Action.DISCONNECT:
                    print(f"[CMD from {clientAddress}] Disconnecting...")
                    break
                case Action.PACKAGE_PICK:
                    print(f"[CMD from {clientAddress}] Picking up package...")
                    activate_magnet()
                    pass
                case Action.PACKAGE_DROP:
                    print(f"[CMD from {clientAddress}] Dropping off package...")
                    deactivate_magnet()
                    pass
                case _:
                    raise ValueError("Unknown opcode received.")
    except Exception as error:
        print(error)
        print(f"Connection to {clientAddress} has been closed.")
    finally:
        client.close()