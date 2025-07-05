from picamera2 import Picamera2
import cv2
import numpy as np
import time

MIN_CONTOUR_AREA = 500

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
time.sleep(1)

try:
    while True:
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

        if found_red:
            print("Red object detected!")
        else:
            print("No red object detected.")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nTerminated by user.")

finally:
    picam2.stop()

