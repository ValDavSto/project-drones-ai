# Betaflight Setup

This guide describes the steps we took to configure our drone using Betaflight.

## Step 1: Connect to Betaflight Configurator

Connect your drone’s flight controller to your PC using a USB cable. Then open the Betaflight Configurator and click **Connect**.

## Step 2: Configure Ports

Go to the **Ports** tab and configure the ports as follows:

- **USB VCP**: Configuration/MSP — enabled  
- **UART1**: Peripherals — VTX (IRC Tramp)  
- **UART2**: Serial RX — enabled  
- **UART3** & **UART4**: Configuration/MSP — enabled  
- **UART6**: Sensor Input — GPS (baud rate: 576000)

<img border-effect="rounded" src="Betaflight_Ports_1.png" alt="Betaflight Ports Configuration"/>

## Step 3: Set CLI MSP Override to 15

1. Open the **CLI** tab.
2. Enter the following commands:

    ```bash
    set msp_override_channels_mask = 15
    save
    ```

> This setting allows Betaflight to accept MSP commands from specific channels or devices, such as a connected Raspberry Pi.

<img border-effect="rounded" src="Betaflight_CLI.png" alt="Betaflight CLI Command for MSP Override"/>

## Step 4: Configure Modes

Navigate to the **Modes** tab and assign switches on your transmitter as follows:

### Basic Flight Modes

- **ARM**: AUX1 and AUX4 — range: 1925–2100  
  > Required to arm the drone for flight.  
- **ANGLE**: AUX2 — range: 900–1100  
  > Enables a stabilized flight mode.

<img border-effect="rounded" src="Betaflight_Modes_1.png" alt="Betaflight Modes: ARM and ANGLE"/>

### Custom MSP Override Mode

- **MSP OVERRIDE**: AUX3 — range:  
  - 1300–1700 → Mode A  
  - 1800–2100 → Mode B  

> This allows a connected Raspberry Pi to control the drone in two distinct modes.  
> (See the separate topic: *Pi as Co-Pilot*.)

<img border-effect="rounded" src="Betaflight_Modes_2.png" alt="Betaflight MSP Override Mode"/>

## Step 5: Verify and Set Motor Direction

1. Go to the **Motors** tab.
2. **Remove all propellers!**
3. Enable motor testing.
4. Test each motor individually and verify the direction matches the **Motor Diagram** displayed in Betaflight.

> For more information about rotor direction and propeller orientation, see [](Rotors.md).

<img border-effect="rounded" src="Betaflight_Motors.png" alt="Betaflight Motor Test"/>
