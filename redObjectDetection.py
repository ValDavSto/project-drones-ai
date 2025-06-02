from picamera2 import Picamera2
import cv2
import numpy as np
import time

# Kamera initialisieren
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
time.sleep(1)  # Kamera warmlaufen lassen

try:
    while True:
        # Bild aufnehmen
        frame = picam2.capture_array()
        
        # In HSV-Farbraum umwandeln
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Zwei Rottöne abdecken (für HSV)
        lower_red1 = np.array([0, 50, 40])
        upper_red1 = np.array([350, 50, 40])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        
        # Rote Bereiche maskieren
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 | mask2
        
        # Konturen finden
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Prüfen, ob größere rote Fläche vorhanden ist
        found_red = False
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # Fläche anpassen je nach Objektgröße
                found_red = True
                break

        if found_red:
            print("🔴 Rotes Objekt erkannt!")
        else:
            print("⚪️ Kein rotes Objekt erkannt.")
        
        time.sleep(1)  # Wartezeit zwischen Erkennungen

except KeyboardInterrupt:
    print("\nBeendet durch Benutzer.")

finally:
    picam2.stop()
