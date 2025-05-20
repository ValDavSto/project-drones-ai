# Hardware

Deploying real-time object detection on a drone with on-board processing presents unique challenges due to constraints in size, 
weight, power consumption, and processing capability. The hardware package must be able to receive video frames at a reasonable 
frame rate, process them in real-time, and optimally send the results back to the drone's control system.

For our purposes, we are using a `2.5-inch` `FlyFish Velociraptor` drone frame, which is already quite compact and has no dedicated space 
for additional hardware besides flight related components. As the usage of larger single-board computers (SBCs) is not feasible due to 
space constraints, our choice fell on the 32-bit `Raspberry Pi Zero W 1.1`. Why not the later revision `Raspberry Pi Zero W 2` with 64-bit support? 
Well, we didn't have any in stock.

However, a single-board computer of this size, especially the Pi Zero, is limited in computational power. This makes it insufficient for running 
complex machine learning models, particularly those required for real-time object detection using camera input.

The `Coral Edge TPU` (Tensor Processing Unit) is specifically designed to execute deep learning models efficiently, enabling high-speed inference 
with significantly lower power consumption compared to CPU-based processing. When paired with a Raspberry Pi, it offloads the heavy lifting of 
running TensorFlow Lite models. The model we are using, the [`Coral USB Accelerator`](https://coral.ai/products/accelerator), is connected via `USB 2.0`.

While being a generic USB device, the Coral TPU requires proper drivers for the Raspberry Pi to function correctly.

## Installation

The `Edge TPU Runtime` is not included in the standard Raspberry Pi OS image, nor the standard debian `APT` package manager repository. Thus, 
we need to install it manually:

```bash
# Add repository to the APT sources list
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
# Add the GPG key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
# Update the package list
sudo apt-get update
```

Afterwards, the `Edge TPU Runtime` can be installed with the following command:

```bash
sudo apt-get install libedgetpu1-std
```

There is also a `libedgetpu1-max` package available, which is optimized for maximum performance. But to be honest, we are quite limited by 
all means of the Raspberry Pi, so we don't need to worry about that.

Installation Guide Source: [coral.ai](https://coral.ai/docs/accelerator/get-started/#1-install-the-edge-tpu-runtime)

## Python API

For our purpose, we are using the `Python` programming language. The `Coral Edge TPU` provides an api for integration with TensorFlow Lite models. 
With the repository already added, we can install the `python3-pycoral` package with the following command:

```bash
sudo apt-get install python3-pycoral
```

The package has additional dependencies such as `numpy`, which are automatically installed by the package manager. To be fully set up for our poject, 
we also need to install the OpenCV `cv2` package for image processing and video handling. This can be done with the following command:

```bash
sudo apt-get install python3-opencv
```

## Integration Test

To test the integration of the `Coral Edge TPU` with the `Raspberry Pi`, we can run an example provided by the `Google Coral` team.

```bash
mkdir coral && cd coral
git clone https://github.com/google-coral/pycoral.git
cd pycoral
```

The repository does not come with the finished model files, so we need to download them manually. The `Google Coral` team provides a 
set of pre-trained models for the `Coral Edge TPU`, which can be found [here](https://coral.ai/models/). 
For this test, we are looking into classification of birds from an image.

```bash
bash examples/install_requirements.sh classify_image.py
```

Once done, we start the classification test run:

```bash
python examples/classify_image.py --model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --labels test_data/inat_bird_labels.txt --input test_data/parrot.jpg
```

The output should (and fortunately does) look like this:

```bash
----INFERENCE TIME----
Note: The first inference on Edge TPU is slow because it includes loading the model into Edge TPU memory.
129.8ms
3.0ms
2.8ms
2.9ms
2.9ms
-------RESULTS--------
Ara macao (Scarlet Macaw): 0.75781
```

Our measured initial first inference time of `129.8ms` is quite high, which is likely caused by us using the `USB 2.0` interface of 
the `Raspberry Pi Zero W`, instead of the `3.0` standard recommended by Coral.

Note: The `Coral USB Accelerator` has no means of communicating its functionality besides a white LED on the device, where a continuous
light means a passive state, while a blinking light indicates an active state. The proper way of knowing if the device is working is by
measuring the processing time. If the model was executed on the CPU, the time would be significantly higher.