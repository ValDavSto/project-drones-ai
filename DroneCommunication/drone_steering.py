from msp_communication import MSP
import time

def stable_flight(msp, throttle=1300):
    msp.send_flight_control(1500, 1500, throttle, 1500)

def forward_flight(msp, throttle=1300):
    msp.send_flight_control(1500, 1600, throttle, 1500)

def turn_left(msp, throttle=1300):
    msp.send_flight_control(1500, 1500, throttle, 1450)

def turn_right(msp, throttle=1300):
    msp.send_flight_control(1500, 1500, throttle, 1550)

def main():
    msp = MSP(port="COM5")
    check_stable = True
    check_forward = True
    drop = False

    try:
        print("Start -  wait for MSP Override")
        throttle_before = 1000
        while True:
            rc = msp.read_rc()
            aux3 = rc[6]
            aux5 = rc[8]
            aux6 = rc[9]
            throttle = rc[3]

            # check aux3 for msp override
            if aux3 < 1400:
                print("MSP Override off - no steering \t ", throttle)
                check_stable = True
                check_forward = True

            elif 1400 <= aux3 < 1900:
                print("stable flight \t\t\t\t\t ", throttle)
                if check_stable:
                    stable_flight(msp, throttle_before)
                    check_stable = False
                elif not check_forward:
                    forward_flight(msp, throttle - 50)
                    check_forward = True
                else:
                    stable_flight(msp, throttle)

            elif aux3 >= 1900:
                print("flying forward \t\t\t\t\t ", throttle)
                if check_forward:
                    forward_flight(msp, throttle + 50)
                    check_forward = False
                else:
                    forward_flight(msp, throttle)


            # check aux5 for picking up packet
            if aux5 >= 1900:
                print("magnet on")
                drop = False  # turn on magnet

            # check aux6 for dropping packet
            if aux6 >= 1900:
                print("magnet off")
                drop = True # turn off magnet


            throttle_before = throttle
            time.sleep(0.1)



    except Exception as e:
        print("Fehler:", e)

    finally:
        msp.close()

if __name__ == "__main__":
    main()