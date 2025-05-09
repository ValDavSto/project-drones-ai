import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # USB-Kamera oder Pi-Cam (wenn aktiviert)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # In HSV umwandeln (besser für Farbfilter)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Farb-Range für ROT definieren
    lower_red = np.array([0, 50, 40])
    upper_red = np.array([350, 50, 40])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = mask1 + mask2

    # Konturen finden
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Nur größere Objekte
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            print("Rotes Objekt erkannt!")

    cv2.imshow("Erkennung", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
