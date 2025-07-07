# Autostart Using systemd (cloudchasers.service)

This section explains how to run the magnet control and object detection script automatically on boot using systemd. This ensures the script starts reliably after networking is initialized and restarts if it crashes.

## cloudchasers.service:
```
[Unit]
Description=CloudChasers Object Detection Script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/CloudChasers/objectDetection/main.py
WorkingDirectory=/home/CloudChasers/objectDetection
User=CloudChasers
Restart=on-failure

[Install]
WantedBy=multi-user.target

```
* **[Unit]**
  - **After=network.target:** Ensures the service starts only after network interfaces are up.
* **[Service]**
  - **ExecStart:** Path to the Python interpreter and the main script.
  - **WorkingDirectory:** The directory from which the script is executed.
  - **User:** Specifies the Linux user that runs the service (CloudChasers).
  - **Restart=on-failure:** Automatically restarts the script if it crashes.
* **[Install]**
  - **WantedBy=multi-user.target:** Ensures the service is started during normal system boot.

### Service File Definition
Place the cloudchasers.service into:

```
/etc/systemd/system/cloudchasers.service
```