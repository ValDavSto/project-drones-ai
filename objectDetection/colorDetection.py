from picamera2 import Picamera2
import cv2
import numpy as np
import time

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

        lower_blue = np.array([100, 150, 50])
        upper_blue = np.array([140, 255, 255])

        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        found_red = any(cv2.contourArea(cnt) > 500 for cnt in contours_red)
        found_blue = any(cv2.contourArea(cnt) > 500 for cnt in contours_blue)

        if found_red:
            print("Rotes Objekt erkannt!")
        elif found_blue:
            print("Blaues Objekt erkannt!")
        else:
            print("Keine Farbe erkannt.")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nVom Benutzer beendet.")

finally:
    picam2.stop()
