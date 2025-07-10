from msp_communication import MSP  # Passe den Dateinamen an

msp = MSP(port="COM5")  # Passe den Port an

try:
    # Beispiel: lies RC-Daten aus
    rc_channels = msp.read_rc()
    print("RC Channels:", rc_channels)

    # Beispiel: sende einfache Steuerdaten
    msp.send_flight_control(rc_channels[0], rc_channels[1], rc_channels[2], 1700)  # neutrale Werte
    # msp.send_flight_control(1500, 1500, 1500, 1700)  # neutrale Werte

    rc = msp.read_rc()
    print("Empfangene RC-Werte:", rc)

finally:
    msp.close()
