#!/bin/bash

sudo systemctl enable bluetooth
sudo systemctl start bluetooth
python3 ./main_ble.py