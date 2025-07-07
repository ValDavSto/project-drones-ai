# Hardware
This page serves as a manual for building the same drone that we used for our project.
It contains a list of all the necessary parts, a soldering plan, and instructions for modifying the frame.

## Components
### Drone components
Following are the components which are necessary to build and FPV drone:
- **Flight- & Electronic Speed Controller | [SpeedyBee F405 Mini BLS 35A 20x20 Stack](https://www.speedybee.com/speedybee-f405-mini-bls-35a-20x20-stack/):**
  - The flight- and electronic speed controller stack is the brain and muscles of the drone. All electrical components are soldered to the stack.
- **Motor | [XING-E Pro 2207 FPV Motor ](https://iflight-rc.eu/de-de/products/xing-e-pro-2207-fpv-motor?srsltid=AfmBOorZfJb61m3TZF4U7hq-KOzMObZ-45vVHunS8bDKBJENCsUe33gM)**
  - With the propellers attached to the motors and the power supplied by the ESC the motors generate thrust to lift the drone up from the ground
- **Propellers | [ETHIX S4 LEMON LIME PROPS](https://ethixltd.com/portfolio/ethix-s4-lemon-lime-props/):**
  - The propellers are mounted on the motors to lift the drone. In this case 5" tri-wing propellers are used, this defines the size of the drone overall
  - The page [Rotors](Rotors.md) provide a detailed description of how to mount the propellers. 
- **Frame | [FlyFishRC Volador II VX5](https://www.flyfish-rc.com/products/volador-ii-vx5-o3-fpv-freestyle-t700-frame-kit?variant=42215327170740):**
  - The frame is the housing for mounting all parts of the drone, giving it stability.
- **Video Transmitter | [SpeedyBee TX800 VTX](https://www.speedybee.com/speedybee-tx800/):**
  - The video transmitter sends the video signal from the FPV camera via a specific channel.
  - As this is an analogue transmitter, the FPV goggles must be compatible. Companies like DJI offer its own digital transmission standard, which provides better video quality, but is much more expensive.  
- **FPV-Camera | [CADDXFPV Ratel Pro Analog](https://caddxfpv.com/products/caddxfpv-ratel-pro-analog-camera?srsltid=AfmBOopvcLiCMd0d08VYGrb2wajsdDMdZSaasnMHIc9Me2bdpfDDi-bh):**
  - The FPV camera captures video and sends it to the pilot, enabling them to fly the drone from a first-person view.
  - A controller for changing camera modes is shipped with the camera, but it is not necessary to use it because the FC can also control it.
- **ELRS-Receiver | [SpeedyBee Nano 2.4G 2.4G-TCXO 915M ExpressLRS ELRS Receiver](https://www.speedybee.com/speedybee-nano-2-4g-2-4g-tcxo-915m-expresslrs-elrs-receiver/)**
  - This receiver enables the flight controller to receive inputs from the remote control to control the drone.
  - For communication, the open source protocol ExpressLRS is used.
- **GPS Module: [HGLRC M100.5883 GPS](https://www.hglrc.com/products/m100-5883-gps?srsltid=AfmBOoq4Prd8-xOA7TuLEUwku7EqjJars7u9iBcFuTG9qOaUqb-IY-ut):**
  - The GPS module tracks the drone's location. This is not necessary for the AI features to work, but it is helpful for features such as locating the drone if it gets lost.
- **Remote | [Radiomaster Zorro](https://www.radiomasterrc.com/products/zorro-radio-controller):**
  - The remote must have a software version installed which supports the protocol of the used receiver on the drone. 
    In our case it has to support ExpressLRS.
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
- **TPU Accelerator [Google Coral TPU USB Accelerator](https://coral.ai/products/accelerator)**:
  - To enhance the Raspberry Pi's processing power for AI applications, the Google Coral is used.
    Connected via USB, it gives the Pi a performance boost, making it feasible for real-time operations.
- **[Step Down Buck Converter](https://www.amazon.de/Konverter-Einstellbarer-Spannungsregler-Converter-Adjustable/dp/B0DPM9FDV3/?_encoding=UTF8&pd_rd_w=WN2Wp&content-id=amzn1.sym.8992a918-7136-40dd-be86-a27cde0e1b99%3Aamzn1.symc.9b8fba90-e74e-4690-b98f-edc36fe735a6&pf_rd_p=8992a918-7136-40dd-be86-a27cde0e1b99&pf_rd_r=ZCB79RSTXXWKGF268DFE&pd_rd_wg=ufe1L&pd_rd_r=739581d0-2789-4094-b340-515096f8fa2b&ref_=pd_hp_d_btf_ci_mcx_mr_ca_id_hp_d)**
  - To be able to power the Raspberry Pi via the 9V connection of the FC a buck step-down converter is required.

### Components for Package delivering
To be able to deliver small packages with the drone, additional components are necessary:
- **Relay | Tongling 5VDC JQC-3FF-S-Z:**
  - The relay is needed to toggle the electro magnet.
    It is connected to the Raspberry Pi, which then can power the electro magnet on and off via the relay.
- **Electro Magnet:**
  - Used to pick up small light packages for transportation via drone
  

  
## Soldering
The two main components of a drone are the flight controller (FC) and the electronic speed controller (ESC).
Stack. Initially, the *SpeedyBee F405 AIO 40A Bluejay* was used, which combines the functions of the FC and ESC in one unit. However, a shortage damaged the FC during soldering of the drone.
A shortage damaged the FC while soldering the drone.

With the SpeedyBee F405 Mini BLS stack, soldering can be completed in two steps.
First, solder the motors and the battery connector to the ESC. Then, solder the rest to the FC.
Once soldering is complete, connect the FC and ESC using the provided cable.

### Soldering plan Flight Controller
The camera, ELRS receiver, GPS module, video transmitter, and Raspberry Pi are soldered to the flight controller.
When soldering some components, it is important to note that the cables for UART communications (RX/TX) must be crossed.
For example, the RX of the ELRS receiver must be connected to the corresponding TX pin on the FC, and the TX pin of the receiver must be connected to the RX pin on the FC.
<img border-effect="rounded" src="soldering_fc_complete.jpg" alt="Picture of soldering plan for the FC" />
The relay and electromagnet shown in the soldering plan are only necessary if the drone is capable of transporting small packages.
The green OSD cable of the camera is also only necessary if the camera modes can be changed via the remote.

### Soldering plan Electronic Speed Controller
To solder the motors, solder the three cables to the ESC. It is important to solder the motors in the order in which they are placed on the frame.

To prevent damage to the ESC and FC from voltage spikes, a capacitor is soldered to the power connection.
It is recommended to add insulation to the capacitor connectors.
<img border-effect="rounded" src="soldering_mc.JPG" alt="Picture of soldering plan for the MC" />


## Frame Modification
The off-the-shelf drone frame is designed for building a simple FPV drone without any additional features.
We therefore had to modify it to accommodate the Raspberry Pi and Coral. There are two ways to achieve this.
Either all the AI components can be strapped to the top of the drone, which requires less modification, or they can be placed inside the frame.
We decided to place them inside the frame for better protection and a more compact drone.

To achieve this, as can be seen in the picture, the FC stack and the VTX are stacked on top of each other at the rear of the frame.
This is a tight fit because the FC stack is usually placed in the center of the frame. Instead, four of the standoffs that would usually support the top of the frame are removed.
This creates enough space in the center of the frame to place the Raspberry Pi and Coral on top of each other.
The frame remains stable, and we experienced no issues with its stability.
<img border-effect="rounded" src="frame_mod.jpg" alt="Picture of frame modification for Raspberry Pi" />