import serial
import struct
import time

MSP_API_V1_START = b'$M<'
MSP_API_V1_REQUEST = b'$M<'
MSP_API_V1_RESPONSE = b'$M>'

MSP_RC = 105  # MSP command for RC channel data

# MSPv1 message builder
def build_msp_request(command):
    payload_size = 0
    payload = b''
    checksum = payload_size ^ command

    return (
        MSP_API_V1_REQUEST +
        bytes([payload_size]) +
        bytes([command]) +
        bytes([checksum])
    )

# MSPv1 response parser
def parse_msp_response(data):
    if not data.startswith(MSP_API_V1_RESPONSE):
        print("Invalid header")
        return None

    size = data[3]
    cmd = data[4]
    payload = data[5:5 + size]

    if cmd == MSP_RC:
        # Each channel is 2 bytes (little endian uint16), 16 channels
        channels = struct.unpack('<16H', payload)
        return channels

    return None

def read_aux_channels(serial_port='COM5', baudrate=115200):
    with serial.Serial(serial_port, baudrate, timeout=2) as ser:
        print("Sending MSP_RC request...")
        ser.write(build_msp_request(MSP_RC))
        time.sleep(0.1)

        header = ser.read(3)
        if header != MSP_API_V1_RESPONSE:
            print("Invalid response header")
            return

        size = ser.read(1)
        cmd = ser.read(1)
        size_val = size[0]
        cmd_val = cmd[0]

        payload = ser.read(size_val)
        checksum = ser.read(1)

        full_response = header + size + cmd + payload + checksum

        channels = parse_msp_response(full_response)
        if channels:
            print("RC Channels:", channels)
            print("AUX1-4:", channels[4])  # Channels 5–8 (index 4–7) are AUX1–4
        else:
            print("Failed to parse response")

if __name__ == "__main__":
    while True:
        read_aux_channels()
        time.sleep(2)