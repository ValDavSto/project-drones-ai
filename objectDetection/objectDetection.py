import time
import numpy as np
import cv2
from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter, load_delegate
import messages

model_path = "models/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite"
label_path = "models/imagenet_labels.txt"

CONFIDENCE_THRESHOLD = 0.5

labels = {}
with open(label_path, 'r') as f:
    for i, line in enumerate(f):
        labels[i] = line.strip()


edgetpu_delegate = load_delegate('libedgetpu.so.1')

interpreter = Interpreter(model_path=model_path, experimental_delegates=[edgetpu_delegate])
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (224, 224)}))
picam2.start()

print("Start image classification... (CTRL+C to exit))")

try:
    while True:
        frame = picam2.capture_array()

        input_shape = input_details[0]['shape']
        img = cv2.resize(frame, (input_shape[2], input_shape[1]))
        img = img.astype(np.uint8)
        input_data = np.expand_dims(img, axis=0)

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])[0]
        top_k = output_data.argsort()[-1:][::-1]  # only Top-1

        class_id = int(top_k[0])
        confidence = output_data[class_id] / 255.0 if output_data[class_id] > 1 else output_data[class_id]

        if confidence > CONFIDENCE_THRESHOLD:
            label = labels.get(class_id, "Unknown")
            print(f"Recognized: {label} with probability of {confidence:.2f}")
            messages.sendMessage(f"Recognized: {label} with probability of {confidence:.2f}")
        else:
            print("Nothing recognized with high confidence.")
            messages.sendMessage("Nothing recognized with high confidence.")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Finished")
