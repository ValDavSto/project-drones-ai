import serial
import struct
import time

class MSP:
    MSP_HEADER = b"$M<"
    MSP_RESPONSE = b"$M>"
    MSP_SET_RAW_RC = 200
    MSP_RC = 105

    def __init__(self, port="/dev/serial0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for connection to FC

    def _build_message(self, command, payload=b''):
        size = len(payload)
        checksum = size ^ command
        for b in payload:
            checksum ^= b
        return self.MSP_HEADER + bytes([size]) + bytes([command]) + payload + bytes([checksum])

    def _read_response(self):
        header = self.ser.read(3)
        if header != self.MSP_RESPONSE:
            raise Exception("Invalid response header")

        size = self.ser.read(1)[0]
        cmd = self.ser.read(1)[0]
        payload = self.ser.read(size)
        checksum = self.ser.read(1)

        return cmd, payload

    def send_rc(self, channels):
        """
        channels: list of 8 integers (Roll, Pitch, Throttle, Yaw, AUX1–4)
        """
        if len(channels) != 8:
            raise ValueError("Must provide exactly 8 channels")
        payload = struct.pack("<8H", *channels)
        msg = self._build_message(self.MSP_SET_RAW_RC, payload)
        self.ser.write(msg)

        try:
            cmd, _ = self._read_response()
            #print("Antwort erhalten (kann ignoriert werden):", cmd)
        except:
            pass  # keine Antwort oder Timeout

    def read_rc(self):
        """
        Returns: list of 16 integers (all RC channels, including AUX)
        """
        msg = self._build_message(self.MSP_RC)
        self.ser.write(msg)

        cmd, payload = self._read_response()
        if cmd != self.MSP_RC:
            raise Exception(f"Unexpected MSP command in response: {cmd}")
        if len(payload) < 16 * 2:
            raise Exception("Payload too short")

        channels = struct.unpack("<16H", payload[:32])
        return channels

    def read_aux_channels(self):
        """
        Returns only the AUX channels (channels 5–8, index 4–7)
        """
        all_channels = self.read_rc()
        aux_channels = all_channels[4:8]
        return aux_channels

    def send_flight_control(self, roll, pitch, throttle, yaw):
        """
        Send only flight data for remote control of the drone
        """
        def clamp(val): return max(1000, min(2000, val))

        # read existing AUX data
        try:
            current_channels = self.read_rc()
            aux = current_channels[4:8]
        except Exception as e:
            print("Error reading AUX values:", e)
            aux = [1000] * 4  # neutral value if communication with FC failed

        rc_values = [
            clamp(roll),
            clamp(pitch),
            clamp(throttle),
            clamp(yaw),
            *aux
        ]
        self.send_rc(rc_values)


    def close(self):
        self.ser.close()
