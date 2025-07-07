from msp_communication import MSP

msp = MSP(port="COM5")

try:
    # Lese initiale Werte
    initial = msp.read_rc()
    print("Initial RC Channels:", initial)

    for i in range(20):
        # Sende Test-Steuerung
        msp.send_flight_control(2000, 2000, 2000, 2000)


        # Danach erneut lesen
        rc = msp.read_rc()
        print("Neue RC-Werte:", rc)

except Exception as e:
    print("Fehler:", e)

finally:
    msp.close()
