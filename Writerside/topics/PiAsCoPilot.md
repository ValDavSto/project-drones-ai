# Pi as Co-Pilot

This topic explains how we use a Raspberry Pi to control the drone either alongside or independently of the pilot.  
The Pi communicates with the Betaflight flight controller using the MSP (MultiWii Serial Protocol) over a UART interface.

---

## Overview

The Raspberry Pi acts as a co-pilot that sends flight commands and receives telemetry from the flight controller.  
It operates in two distinct modes, determined by the `MSP OVERRIDE` switch position in Betaflight:

- **Stable Mode (AUX3: 1300–1700)** – The Pi sends input values that keep the drone flying in a stable, level position.
- **Object Detection Mode (AUX3: 1800–2100)** – The Pi moves the drone forward slightly. It uses object detection to identify colors:
  - If a **red object** is detected, the drone turns slightly **left**
  - If a **blue object** is detected, the drone turns slightly **right**

> See [](BetaflightSetup.md) for how the `MSP OVERRIDE` mode is configured.

---

## Hardware Connection

Connect the Raspberry Pi to the flight controller via a UART interface:

- **Pi TX** → **FC RX** (e.g., UART3)  
- **Pi RX** → **FC TX**

> For details on powering the Raspberry Pi safely from the drone, see [](Power-Supply.md).

---

## Software

We use a Python program on the Raspberry Pi to interact with the drone via the **MSP protocol** (MultiWii Serial Protocol). The Pi communicates directly with the flight controller over a UART connection and sends flight control commands like roll, pitch, yaw, and throttle.

### Behavior Overview

The program continuously reads the drone's **AUX channels** to decide what to do:

- **AUX3** controls the flight behavior:
  - **< 1400**: MSP Override is off – the Pi does nothing.
  - **1400–1900**: Stable hover mode – the Pi keeps the drone in position.
  - **> 1900**: Object detection mode – the Pi moves the drone forward slightly, and reacts to detected objects.

- **AUX5** activates the magnet (e.g., to pick up a payload).
- **AUX6** deactivates the magnet (e.g., to drop a payload).

All flight commands are sent via a custom `MSP` class, which uses the serial port to exchange MSP messages with the flight controller. The Pi sends new RC values and also reads existing channel values, to combine its flight input with the AUX values set by the pilot.

> See more to Package Transportation here: [](Package-Transportation.md)

> The full MSP protocol implementation is written in Python and handles packet formatting, communication over UART, and RC channel synchronization.

### MSP Communication Class

The custom `MSP` class provides methods to:

- Send RC data to the flight controller (`send_rc`)
- Read all current RC channels (`read_rc`)
- Send flight input (roll, pitch, yaw, throttle) while preserving AUX values (`send_flight_control`)

It handles packet formatting according to the MSP protocol and runs over a serial UART interface (e.g., `/dev/serial0` or `COM5`). The protocol uses a binary message format with checksums to ensure reliable communication.

This allows the Raspberry Pi to behave as an auxiliary flight control unit, without interfering with pilot input unless MSP Override is enabled.
