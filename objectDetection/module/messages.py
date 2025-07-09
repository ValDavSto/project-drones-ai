from socket import socket, AF_INET, SOCK_STREAM

s = None

def getOrConnectLocalSocket(hostname: str = "127.0.0.1", port: int = 4242, reconnect: bool = False) -> socket:
    """
    Establishes a connection to a local socket server or returns an existing connection.
    Args:
        hostname (str): The hostname or IP address of the server. Defaults to "127.0.0.1".
        port (int): The port to connect to. Defaults to 4242.
    Returns:
        socket: The connected socket instance.
    """
    global s
    if not s or reconnect:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((hostname, port))
    return s

def sendMessage(msg: str):
    """
    Sends a message as a UTF-8 encoded string over the local socket.
    Args:
        msg (str): The message to send.
    Raises:
        ValueError: If the message is empty or larger than 65536 bytes.
    """
    data = msg.encode(encoding="utf-8")
    if not 0 < len(data) < (1 << 16):
        raise ValueError('Message may not be empty or larger than 1<<16 bytes.')
    try:
        getOrConnectLocalSocket().sendall(len(data).to_bytes(2, byteorder='big', signed=False) + data)
    except ConnectionError:
        getOrConnectLocalSocket(reconnect=True).sendall(len(data).to_bytes(2, byteorder='big', signed=False) + data)