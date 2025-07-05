
# Image Classification with EdgeTPU and PiCamera2

This Python script captures images from the Raspberry Pi camera, performs real-time image classification using a TensorFlow Lite model optimized for the Coral EdgeTPU, and sends notifications via the `messages` module.

---

## Dependencies

Make sure the following Python packages and system libraries are installed:

- `picamera2`
- `opencv-python` (`cv2`)
- `numpy`
- `tflite_runtime` (with EdgeTPU support)
- Coral EdgeTPU runtime and `libedgetpu.so.1`
---

## Files and Resources

- `models/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite` – Quantized TFLite model for EdgeTPU
- `models/imagenet_labels.txt` – Label file mapping class indices to names
---

## 🔧 Initialization

```python
model_path = "models/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite"
label_path = "models/imagenet_labels.txt"
```

- Loads the TFLite model and labels used for classification.

```python
labels = {}
with open(label_path, 'r') as f:
    for i, line in enumerate(f):
        labels[i] = line.strip()
```

- Reads class labels from the file into a dictionary.

```python
edgetpu_delegate = load_delegate('libedgetpu.so.1')
interpreter = Interpreter(model_path=model_path, experimental_delegates=[edgetpu_delegate])
interpreter.allocate_tensors()
```

- Loads the model with the EdgeTPU delegate to enable hardware acceleration.

---

## Camera Configuration

```python
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (224, 224)}))
picam2.start()
```

- Configures the PiCamera2 to output images in the correct format and resolution for the model (224x224 RGB).

---

## Main Loop

### 1. **Capture Image**
```python
frame = picam2.capture_array()
```

### 2. **Preprocess for Model Input**
```python
img = cv2.resize(frame, (input_shape[2], input_shape[1]))
img = img.astype(np.uint8)
input_data = np.expand_dims(img, axis=0)
```

- Resizes the image to match the model's expected input size and adds a batch dimension.

### 3. **Run Inference**
```python
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
```

### 4. **Get Prediction**
```python
output_data = interpreter.get_tensor(output_details[0]['index'])[0]
top_k = output_data.argsort()[-1:][::-1]
class_id = int(top_k[0])
confidence = output_data[class_id] / 255.0 if output_data[class_id] > 1 else output_data[class_id]
```

- Extracts the top-1 prediction and normalizes confidence (if quantized).

### 5. **Threshold & Notify**
```python
if confidence > 0.5:
    label = labels.get(class_id, "Unknown")
    print(f"Recognized: {label} with probability of {confidence:.2f}")
    messages.sendMessage(f"Recognized: {label} with probability of {confidence:.2f}")
else:
    print("Nothing recognized with high confidence.")
    messages.sendMessage("Nothing recognized with high confidence.")
```

- If confidence exceeds 50%, the label is printed and a message is sent.
- Otherwise, a fallback message is issued.

### 6. **Delay Between Inferences**
```python
time.sleep(0.5)
```

---

## Graceful Shutdown

```python
except KeyboardInterrupt:
    print("Finished")
```

- Terminates the program cleanly when interrupted by the user.

---

## Notes

- The confidence threshold (`0.5`) can be adjusted to make the system more or less sensitive.
- Make sure the EdgeTPU runtime is correctly installed and `libedgetpu.so.1` is accessible.
---

## Example Output

```
Recognized: banana with probability of 0.87
Nothing recognized with high confidence.
```