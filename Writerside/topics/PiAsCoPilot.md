# Pi as Co-Pilot

This section describes how we utilize a Raspberry Pi Zero 2W as an intelligent co-pilot for our drone system. The Raspberry Pi communicates with the Betaflight flight controller using the MultiWii Serial Protocol (MSP) over a UART interface. This setup enables semi-autonomous flight behavior while maintaining full compatibility with manual pilot inputs.

---

## Overview

The Raspberry Pi serves as an auxiliary flight control unit that interacts with the main flight controller. It sends RC commands and reads telemetry data using MSP over a serial interface. Depending on the flight mode selected via the Betaflight AUX3 channel, the Pi executes different behaviors.

There are two main operational modes:

- **Stable Hover Mode** (`AUX3: 1300–1800`):  
  In this mode, the Pi takes over the control sticks to maintain a level and stable hover. It continuously sends neutral control values to keep the drone steady.

- **Object Detection Mode** (`AUX3: 1800–2100`):  
  The Pi initiates forward motion and simultaneously performs object detection. Based on the detected object's color, it steers the drone:
  - **Red object** → slight turn to the **left**
  - **Blue object** → slight turn to the **right**

> For configuration details, refer to [](BetaflightSetup.md), which explains how to enable MSP Override mode.

---

## Hardware Setup

To establish communication between the Raspberry Pi and the flight controller, connect the two devices via a UART interface:

- **Raspberry Pi TX** → **Flight Controller RX** (e.g., UART3)
- **Raspberry Pi RX** → **Flight Controller TX**

Ensure the Pi is properly powered from the drone's power system.




## Software Architecture

A custom Python script runs on the Raspberry Pi to handle MSP communication. This script acts as a bridge between the Pi and the Betaflight flight controller, issuing control commands and reading telemetry over a serial connection.

### Operational Behavior

The core logic revolves around continuously monitoring the AUX channels to determine the Pi's control behavior:

- **AUX3** (Mode Selector):
  - **< 1300**: MSP Override is off – the Pi remains inactive.
  - **1300–1800**: Stable mode – the Pi maintains the drone’s current position.
  - **> 1800**: Object detection mode – the Pi commands forward motion and reacts to visual input.

- **AUX5**: Activates the magnet (e.g., to pick up a package).
- **AUX6**: Deactivates the magnet (e.g., to release a package).

All control logic is managed through a custom `MSP` class, which sends and receives MSP messages over the serial connection. This class allows us to inject RC commands while preserving the pilot's AUX settings.

> For further information on payload delivery, refer to [](Package-Transportation.md).

> The MSP implementation in Python includes full support for packet formatting, UART communication, and RC channel synchronization.

---

## MSP Communication Module

The `MSP` class abstracts the protocol details and provides high-level methods for:

- **Sending RC input** (`send_rc`)
- **Reading current RC channel values** (`read_rc`)
- **Sending flight control commands** with pitch, roll, yaw, and throttle inputs while maintaining AUX values (`send_flight_control`)

This module encodes MSP packets with proper binary formatting and checksum validation to ensure robust communication. It typically operates over `/dev/serial0` (Linux) or `COMx` ports (Windows).

Through this abstraction, the Raspberry Pi can behave like a secondary flight controller that only overrides inputs when allowed by the MSP Override switch.

---

## Co-Pilot Flight Logic

### Stable Mode

When the `AUX3` channel reads between `1400` and `1900`, the Pi activates its "Stable Mode." In this state, the Pi keeps the drone level by sending neutral RC inputs:

`roll = 1500`

`pitch = 1500`

`yaw = 1500`  

`throttle = (last known throttle from pilot)`

This allows the drone to maintain its attitude, assuming it was already stable at the time of mode activation. The Pi does not attempt to recover unstable motion — it simply holds the current attitude using balanced control inputs.

### Object Detection and Forward Movement

When `AUX3` exceeds `1900`, the Pi enters "Object Detection Mode." It adjusts the drone’s behavior as follows:

- Increases throttle slightly (adds `+50` to the last known throttle input).
- Tilts the drone forward by setting **pitch = 1600**.
- Uses onboard image recognition to scan for colored objects:
  - If a **red object** is detected → **yaw = 1450** (turn left)
  - If a **blue object** is detected → **yaw = 1550** (turn right)
  - If no object is detected → **yaw = 1500** (no turn)

> Important: Avoid switching directly from the lowest AUX3 value (Off Mode) to the highest (Object Detection Mode). Always pass through Stable Mode to ensure smooth transition and stable flight behavior.
