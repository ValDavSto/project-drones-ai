from picamera2 import Picamera2

from msp_communication import MSP
import gpiozero

import cv2
import numpy as np
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
    magnet = gpiozero.LED(11)
    msp = MSP(port="/dev/serial0")

    MIN_CONTOUR_AREA = 500
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())
    picam2.start()
    time.sleep(1)
    
    try:
        throttle_before = 1000
        check_stable = True
        check_forward = True
        MAX_COUNT = 40
        count = MAX_COUNT
        direction = False # False-> left, True -> right

        while True:
            # do the object detection
            frame = picam2.capture_array()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([179, 255, 255])

            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = cv2.bitwise_or(mask1, mask2)

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            found_red = False
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > MIN_CONTOUR_AREA:
                    found_red = True
                    break
            
            ##############################################################
            # check drone part
            rc = msp.read_rc()
            aux3 = rc[6]
            aux5 = rc[8]
            aux6 = rc[9]
            throttle = rc[3]

            # check aux3 for msp override
            if aux3 < 1300:
                check_stable = True
                check_forward = True

            elif 1300 <= aux3 < 1800:
                if check_stable:
                    stable_flight(msp, throttle_before)
                    check_stable = False
                elif not check_forward:
                    forward_flight(msp, throttle - 50)
                    check_forward = True
                else:
                    if found_red:
                        if direction:
                            turn_right(msp, throttle)
                        else:
                            turn_left(msp, throttle)
                        count = MAX_COUNT
                    else:
                        stable_flight(msp, throttle)
                        count = count - 1
                        if count == 0:
                            direction = not direction
                            count = MAX_COUNT

            elif aux3 >= 1800:
                if check_forward:
                    forward_flight(msp, throttle + 50)
                    check_forward = False
                else:
                    forward_flight(msp, throttle)

            # check aux5 for picking up packet
            if aux5 >= 1800:
                magnet.on()

            # check aux6 for dropping packet
            if aux6 >= 1800:
                magnet.off()

            throttle_before = throttle
            time.sleep(0.1)



    except Exception as e:
        print("Fehler:", e)

    finally:
        msp.close()



if __name__ == "__main__":
    main()