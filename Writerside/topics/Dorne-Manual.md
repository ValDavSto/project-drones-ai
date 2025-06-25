# Drone Manual
This page is a manual on how to build the same drone that we used for our project.
It includes a list of all the necessary parts, a soldering plan, and details of all the software configurations.
## Components

### Drone components
Following are the components which are necessary to build and FPV drone:
- **Flight- & Electronic Speed Controller | [SpeedyBee F405 Mini BLS 35A 20x20 Stack](https://www.speedybee.com/speedybee-f405-mini-bls-35a-20x20-stack/):**
  - The flight- and electronic speed controller stack is the brain and muscles of the drone. All electrical components are soldered to the stack.
      <img border-effect="rounded" src="fc_mc_stack.jpg" alt="Picture of SpeedyBee F405 Mini BLS stack" width="220"/>
- **Motor | [XING-E Pro 2207 FPV Motor ](https://iflight-rc.eu/de-de/products/xing-e-pro-2207-fpv-motor?srsltid=AfmBOorZfJb61m3TZF4U7hq-KOzMObZ-45vVHunS8bDKBJENCsUe33gM)**
    <img border-effect="rounded" src="motor.jpg" alt="Picture of SpeedyBee F405 Mini BLS stack" width="400"/>
- **Propellers | [ETHIX S4 LEMON LIME PROPS](https://ethixltd.com/portfolio/ethix-s4-lemon-lime-props/):**
  - The propellers are mounted on the motors to lift the drone. In this case 5" tri-wing propellers are used, this defines the size of the drone overall
  - The page [Rotors](Rotors.md) provides a detailed description of how to mount the propellers. 
- **Frame | [FlyFishRC Volador II VX5](https://www.flyfish-rc.com/products/volador-ii-vx5-o3-fpv-freestyle-t700-frame-kit?variant=42215327170740):**
  - The frame is the housing for mounting all parts of the drone, giving it stability.
- **Video Transmitter | [SpeedyBee TX800 VTX](https://www.speedybee.com/speedybee-tx800/):**
  - The video transmitter sends the video signal from the FPV camera via a specific channel.
  - As this is an analogue transmitter, the FPV goggles must be compatible. Companies like DJI offer its own digital transmission standard, which provides better video quality, but is much more expensive.  
- **FPV-Camera | [CADDXFPV Ratel Pro Analog](https://caddxfpv.com/products/caddxfpv-ratel-pro-analog-camera?srsltid=AfmBOopvcLiCMd0d08VYGrb2wajsdDMdZSaasnMHIc9Me2bdpfDDi-bh):**
  - The FPV camera captures video and sends it to the pilot, enabling them to fly the drone from a first-person view.
  - A controller for changing camera modes is shipped with the camera, but it is not necessary to use it because the FC can also control it.
- **ELRS-Receiver | [SpeedyBee Nano 2.4G 2.4G-TCXO 915M ExpressLRS ELRS Receiver](https://www.speedybee.com/speedybee-nano-2-4g-2-4g-tcxo-915m-expresslrs-elrs-receiver/)**
  - This receiver enables the flight controller to receive inputs from the remote control in order to control the drone.
  - For communication, the open source protocol ExpressLRS is used.
- **GPS Module: [HGLRC M100.5883 GPS](https://www.hglrc.com/products/m100-5883-gps?srsltid=AfmBOoq4Prd8-xOA7TuLEUwku7EqjJars7u9iBcFuTG9qOaUqb-IY-ut):**
  - The GPS module tracks the drone's location. This is not necessary for the AI features to work, but it is helpful for features such as locating the drone if it gets lost.
- **Remote | [Radiomaster Zorro](https://www.radiomasterrc.com/products/zorro-radio-controller):**
  - The remote must have a software version installed which supports the protocol of the used receiver on the drone. 
    In our case, it has to support ExpressLRS.
  - We flashed with [Buddy EdgeTx](https://buddy.edgetx.org/#/flash?version=v2.11.1&source=releases) the new software on the remote via USB-Connection. 
    In the case of the *Zorro* the top USB port must be used.
- **Battery Pack | [Tattu 650mAh 4S1P 75C 14,8V Lipo-Battery pack](https://gensace.de/de/products/tattu-650mah-4s1p-75c-14-8v-lipo-battery-pack-with-xt30-plug)**
  - The battery pack is the drone's power source.
  - We used 4S battery packs, meaning they have four cells.
  - The capacity determines how long the drone can fly for, but it also adds additional weight.
- **FPV-Goggles [Skyzone CobraS](https://www.skyzonefpv.com/en-de/products/cobras?srsltid=AfmBOoqXPgbzHhQ-UA4YqQOgKM_DhduKxrzzWDbp3jmiQP4FeXCJ9EFb):**
  - The goggles can be used to fly the drone in first-person view mode, with the image transmitted by the drone.
  - The image quality received can be compared to that of an older camcorder.
- **Charger [SKYRC S100 neo AC/DC Smart Balance Charger](https://www.skyrc.com/s100neo):**
  - The SkyRC S100 can charge drone battery packs and also read their status.
  - A special charger is necessary for LiPo batteries to ensure the cells don't get damaged.

### Components for AI Application
Additional components are necessary to add AI capabilities to the drone:
- **Single Board Computer | [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/):**
  - The Raspberry Pi is the brain for the AI application
  - Communication with the FC via UART connection using the MSP protocol
  - Control of the electro magnet for the package transportation
- **Camera | [Joy-it 8MP 120° Camera](https://www.joy-it.net/de/products/RB-CAMERA-JT-V2-120):**
  - Camera for computer vision of the Raspberry Pi
- TPU Accelerator [Google Coral TPU USB Accelerator](https://coral.ai/products/accelerator):
  - To enhance the Raspberry Pi's processing power for AI applications, the Google Coral is used.
    Connected via USB, it gives the Pi a performance boost, making it feasible for real-time operations.
  

  

## Soldering
The two main components of the drone are the flight controller (FC) and electronic speed controller (ESC).
stack. Initially, the *SpeedyBee F405 AIO 40A Bluejay* was used, which combines the FC and ESC functions in one unit. However, during the
However, a shortage damaged the FC during soldering of the drone.

With the *SpeedyBee F405 Mini BLS* stack, soldering can be completed in two steps.
First, solder the motors and the battery connector to the ESC, then solder the rest to the FC.
Once soldering is complete, connect the FC and ESC using the cable provided with the stack.

### Soldering plan Flight Controller
The camera, ELRS receiver, GPS module, video transmitter and Raspberry Pi are soldered to the flight controller.
Important to notice when soldering some components, that the cables for the UART communications (RX/TX) always have to be crossed.
That means that, for example, the RX of the ELRS receiver has to be connected to the corresponding TX pin on the FC and reversed for the TX pin of the receiver.
<img border-effect="rounded" src="soldering_fc.jpg" alt="Picture of soldering plan for the FC" />

### Soldering plan Electronic Speed Controller
The 
<img border-effect="rounded" src="soldering_mc.JPG" alt="Picture of soldering plan for the MC" />

