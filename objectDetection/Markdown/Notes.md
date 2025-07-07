# FPV Drone with AI Detection

---

## PI Zero - Config
```
Username: CloudChasers
Password: fpvDrone123

SSID: CloudChasers
Password: fpvDrone123
Domain: drone or drone.local
```

## Pi-camera

### Configuration:

```bash
sudo nano /boot/config.txt
```

```bash
[all]
camera_auto_detect=0
dtoverlay=imx219
start_x=1
gpu_mem=128
```

```bash
sudo reboot
```

### Capture Picture:
```bash
libcamera-still -o photo_name.jpg
```
or
```bash
rpicam-still -o ./photo_name.jpg
```

## TMUX

### Install
```bash
sudo apt-get install tmux
```

### New Session
```bash
tmux new -s <process_name>
```

### Decouple
```bash
Ctrl + B, then D
```

### Reconnect
```bash
tmux attach -t <process_name>
```

### Show running sessions
```bash
tmux ls
```

### Terminate session 
#### (inside)
```bash
Ctrl + D
```
or
```bash
exit
```
#### (outside)
```bash
tmux kill-session -t <process_name>
```
Terminate all sessions
```bash
tmux kill-server
```
