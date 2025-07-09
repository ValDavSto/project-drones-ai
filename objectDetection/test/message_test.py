import messages
import time

x = 0

while True:
    x += 1
    messages.sendMessage(f"Hello World{x}")
    time.sleep(1)