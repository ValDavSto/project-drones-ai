# FPV Drone with AI Detection

---


## TMUX

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