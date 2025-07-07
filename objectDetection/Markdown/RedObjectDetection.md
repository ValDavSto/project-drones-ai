# Red Object Detection

This Python script captures images from a Raspberry Pi camera using PiCamera2 and analyzes them in real-time to detect the presence of red objects. It uses the HSV color space for more robust color detection.

## Libaries
```python
from picamera2 import Picamera2
import cv2
import numpy as np
import time
```

* **picamera2:** Interface for the Raspberry Pi Camera Module.
* **cv2 (OpenCV):** Image processing and computer vision tasks.
* **numpy:** Efficient array operations, used here for masks and color thresholds.
* **time:** Adds delays and manages timing.

---

## Initialization

```python
from picamera2 import Picamera2
import cv2
import numpy as np
import time
```

* Initializes the camera and configures it for still image capture.
* Waits for one second to ensure the camera is ready.

---

## Main Loop

```python
while True:
    ...
```
The loop runs continuously until the program is interrupted by the user (CTRL+C).

---

## Image Capture and Color Conversion

```python
frame = picam2.capture_array()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```
* Captures a frame from the camera.
* Converts the image to HSV (Hue, Saturation, Value) color space, which is better suited for color segmentation than RGB.

---

## Red Color Range Definition

```python
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])
```
* Red spans two ranges in HSV: near 0° and near 180° hue values.
* Two ranges are defined to cover the full red spectrum.

---

## Mask Creation and Combination

```python
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)
```
* Creates binary masks for each red range.
* Combines the two masks into a single one that highlights all red areas.

---

## Red Object Detection

```python
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
```
* Finds contours in the mask to identify red regions.

```python
for cnt in contours:
    contour_area = cv2.contourArea(cnt)
    if contour_area > MIN_CONTOUR_AREA:
        found_red = True
        break
```

* Loops through all contours and calculates their area using cv2.contourArea().

* If any contour has an area greater than MIN_CONTOUR_AREA, a red object is considered detected. (MIN_CONTOUR_AREA is a configurable threshold value defined earlier in the code to control the sensitivity of red object detection.)

---

## Output

```python
if found_red:
    print("Red object detected!")
else:
    print("No red object detected.")

time.sleep(1)
```
* Prints the detection result every second.
* Adds a delay with time.sleep(1) to reduce processing load and output spam.

---

## Graceful Exit

```python
except KeyboardInterrupt:
    print("\nTerminated by user.")
```

* Handles manual termination (CTRL+C) with a user-friendly message.

```python
finally:
    picam2.stop()
```

* Ensures the camera is properly stopped, whether the loop ends normally or due to an error/interruption.
