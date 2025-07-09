# Remote Magnet Control via TCP (Raspberry Pi)

This Python script sets up a TCP server to receive commands from remote clients. It listens for instructions to activate or deactivate a magnet (via GPIO pin), used e.g. for package pickup/drop-off. It supports graceful shutdown and includes a local-to-global communication bridge.

## Libaries
```python
import sys
import time
import enum
import signal
import gpiozero
import threading
from socket import socket, AF_INET, SOCK_STREAM
import datetime
```

* **sys, time, datetime:** Core system functions, delays, and timestamp logging.
* **enum:** Defines action types for client commands.
* **signal:** Handles system signals for graceful exit.
* **gpiozero:** Simplified GPIO control (here: magnet on GPIO 23).
* **threading:** Used for managing parallel communication (local ↔ global).
* **socket:** Manages TCP communication.
---

## Logging Startup
```python
with open("/home/CloudChasers/objectDetection/logs/autostart_log.txt", "a") as f:
    f.write(f"Script gestartet um {datetime.datetime.now()}\n")
```

* Logs script startup time for diagnostics.
---

## TCP Server Setup
```python
def create_server(hostname: str, port: int) -> socket:
    ...
```

* Creates a TCP server bound to the specified hostname and port.
* Starts listening for incoming connections.

```python
server = create_server("0.0.0.0", 1337)
local  = create_server("127.0.0.1", 4242)
```

* **server:** Global client access (e.g. drone command).
* **local:** Internal/local communication (optional submodule).

## Graceful Shutdown
```python
signal.signal(signal.SIGINT, lambda ..., ...: close_servers([server, local]))
signal.signal(signal.SIGTERM, lambda ..., ...: close_servers([server, local]))
```
* Handles CTRL+C or system termination to cleanly shut down sockets and exit.

```python
def close_servers(srv: list[socket]) -> None:
    ...
```
* Closes all open server sockets and exits the script.

## Client Communication Handling
```python
def receive_bytes(cli: socket, n: int) -> bytes:
    ...
```
* Receives exactly n bytes from a socket connection.
* Raises an error if the connection breaks mid-transmission.

```python
def acknowledge_client(cli: socket) -> None:
    ...
```
* Sends a handshake message ("DroneUAS") and expects acknowledgment back from the client.

## Action Commands
```python
class Action(enum.Enum):
    DISCONNECT = 0
    PACKAGE_PICK = 1
    PACKAGE_DROP = 2
```

* Defines valid commands the server can interpret:
- #0 - Disconnect
- #1 - Activate magnet (pick)
- #2 - Deactivate magnet (drop)

## GPIO Control
```python
magnet = gpiozero.LED(23)
```
* Sets up GPIO pin 23 as digital output to control the magnet.

```python
def activate_magnet():
    magnet.on()

def deactivate_magnet():
    magnet.off()
```
* Turns the magnet on/off for physical package handling.

## Local Communication Bridge
```python
def localMessageLoop(pipe: socket):
    ...
```
* Accepts connections on the local port (127.0.0.1:4242) and forwards all received messages to the main client socket.
* Runs in a background thread.

## Main Control Loop
```python
while True:
    client, clientAddress = server.accept()
    ...
```

* Waits for incoming client connections.
* After successful handshake, spawns the localMessageLoop as a thread.
* Processes incoming commands one byte at a time:
* Disconnect (0): Ends session.
    - Package Pick (1): Activates magnet.
    - Package Drop (2): Deactivates magnet.
    - Unknown codes raise an error.

## Architecture Diagram

<img border-effect="rounded" src="architecture.png" alt="Project poster."/>