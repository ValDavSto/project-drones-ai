import sys
import time
import enum
import signal
import gpiozero
import threading
from socket import socket, AF_INET, SOCK_STREAM

# [SECTION]: Communication

def create_server(hostname: str, port: int) -> socket:
    """
    Creates a TCP server socket, binds it to the hostname and port, and starts listening.
    Args:
        hostname (int): The hostname on which the server should listen.
        port (int): The port on which the server should listen.
    Returns:
        socket: The created and listening server socket.
    """
    srv = socket(AF_INET, SOCK_STREAM)
    print(f"Starting server on {port}")
    srv.bind((hostname, port))
    srv.listen(2)
    return srv

def close_servers(srv: list[socket]) -> None:
    """
    Closes the given server socket and terminates the program.
    Args:
        srv (socket): The server socket to close.
    """
    for s in srv:
        # noinspection PyBroadException
        try:
            s.close()
        except Exception:
            pass
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
server = create_server(hostname = "0.0.0.0", port = 1337)
local = create_server(hostname = "127.0.0.1", port = 4242)
signal.signal(signal.SIGINT, lambda signum, frame: close_servers([server, local]))   # CTRL+C
signal.signal(signal.SIGTERM, lambda signum, frame: close_servers([server, local]))  # Termination

# GPIO setup
magnet = gpiozero.LED(23)

def localMessageLoop(pipe: socket):
    """
    Pipe from local to global
    """
    try:
        while True:
            localClient, localClientAddress = local.accept()
            print(f"Local connection from {localClientAddress} has been established.")
            try:
                while True:
                    pipe.sendall(receive_bytes(localClient, 1))
            except Exception as localError:
                print(localError)
                print(f"Local Connection to {localClientAddress} has been closed.")
            finally:
                localClient.close()
    except ConnectionError:
        pass

# Main loop to accept and handle client connections
while True:
    client, clientAddress = server.accept()
    loop: threading.Thread | None = None
    print(f"Connection from {clientAddress} has been established.")
    try:
        acknowledge_client(client)
        loop = threading.Thread(target=localMessageLoop, args = (client,), daemon=True).start()
        while True:
            opcode = receive_bytes(client, 1)[0]
            if opcode == Action.DISCONNECT.value:
                print(f"[CMD from {clientAddress}] Disconnecting...")
                break
            elif opcode == Action.PACKAGE_PICK.value:
                print(f"[CMD from {clientAddress}] Picking up package...")
                activate_magnet()
            elif opcode == Action.PACKAGE_DROP.value:
                print(f"[CMD from {clientAddress}] Dropping off package...")
                deactivate_magnet()
            else:
                raise ValueError(f"Unknown opcode {opcode} received.")
    except Exception as error:
        print(error)
    finally:
        print(f"Connection to {clientAddress} has been closed.")
        time.sleep(1)
        client.close()
        local.close()
        if loop:
            loop.join()
