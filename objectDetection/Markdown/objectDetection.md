
# Image Classification with EdgeTPU and PiCamera2

This Python script captures images from a Raspberry Pi camera using PiCamera2, classifies them in real-time using a TensorFlow Lite model optimized for the Coral EdgeTPU, and sends classification results via a custom messages module.

---

## Libraries

```python
import time
import numpy as np
import cv2
from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter, load_delegate
import messages
```

* **time:** Controls the delay between classification cycles.
* **numpy:** Handles image data and numerical operations.
* **cv2 (OpenCV):** Image resizing and format conversion.
* **picamera2:** Interface for accessing the Raspberry Pi Camera.
* **tflite_runtime:** Lightweight TensorFlow interpreter for running TFLite models.
* **messages:** Custom module to send notifications/messages.
---

## Files and Resources

```python
model_path = "models/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite"
label_path = "models/imagenet_labels.txt"
CONFIDENCE_THRESHOLD = 0.5
```
* **model_path:** Path to the pre-trained quantized MobileNetV3 TFLite model.
* **label_path:** Text file containing class labels.
* **CONFIDENCE_THRESHOLD:** Minimum confidence level required to accept a classification.

```python
labels = {}
with open(label_path, 'r') as f:
    for i, line in enumerate(f):
        labels[i] = line.strip()
```

* Loads the TFLite model and labels used for classification.

## Model Interpreter Configuration

```python
edgetpu_delegate = load_delegate('libedgetpu.so.1')
interpreter = Interpreter(model_path=model_path, experimental_delegates=[edgetpu_delegate])
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
```

* Loads the model using the EdgeTPU delegate to run inference on the Coral accelerator.
* Retrieves input and output tensor metadata.
---

## Camera Configuration

```python
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (224, 224)}))
picam2.start()
```

* Initializes the PiCamera with a preview configuration that matches the model’s input size and color format (RGB888, 224×224 pixels).

---

## Main Loop
```python
while True:
    ...
```
* Runs indefinitely until manually interrupted.
  
### 1. Capture Image
```python
frame = picam2.capture_array()
```
* Captures a single frame from the PiCamera.
* 
### 2. Preprocessing
```python
img = cv2.resize(frame, (input_shape[2], input_shape[1]))
img = img.astype(np.uint8)
input_data = np.expand_dims(img, axis=0)
```
* Resizes the image to fit the model’s input shape and adds a batch dimension.

### 3. Model Inference
```python
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
```
* Sends the image to the model and triggers inference.

### 4. Output Extraction
```python
output_data = interpreter.get_tensor(output_details[0]['index'])[0]
top_k = output_data.argsort()[-1:][::-1]
class_id = int(top_k[0])
confidence = output_data[class_id] / 255.0 if output_data[class_id] > 1 else output_data[class_id]
```
* Retrieves the model's top prediction and calculates confidence, normalizing it if necessary.

### 5. Classification Decision
```python
if confidence > CONFIDENCE_THRESHOLD:
    label = labels.get(class_id, "Unknown")
    print(f"Recognized: {label} with probability of {confidence:.2f}")
    messages.sendMessage(f"Recognized: {label} with probability of {confidence:.2f}")
else:
    print("Nothing recognized with high confidence.")
    messages.sendMessage("Nothing recognized with high confidence.")
```
* Compares the confidence score against the threshold.
* If confident, prints and sends the result; otherwise sends a default message.

### 6. Delay Between Inferences
```python
time.sleep(0.5)
```
* Adds a short delay between cycles to reduce load and avoid redundant classifications.

### 7. Example Output

```
Recognized: banana with probability of 0.87
Nothing recognized with high confidence.
```
---

## Graceful Shutdown

```python
except KeyboardInterrupt:
    print("Finished")
```
* Terminates the program cleanly when interrupted by the user.

---

## Notes
* You can adjust CONFIDENCE_THRESHOLD to control the model's sensitivity.
* Ensure that libedgetpu.so.1 is correctly installed on your device for EdgeTPU acceleration.
---