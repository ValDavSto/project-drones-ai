# Drone Manual

## Components
Following are the components which are necessary to build and FPV drone:
- **Flight- & Motor controller | [SpeedyBee F405 Mini BLS 35A 20x20 Stack](https://www.speedybee.com/speedybee-f405-mini-bls-35a-20x20-stack/):**
  The flight- and motorcontroller stack is the heart of the drone. All electrical components are soldered to the stack
    <img border-effect="rounded" src="fc_mc_stack.jpg" alt="Picture of SpeedyBee F405 Mini BLS stack" width="220"/>
- **Motor | [XING-E Pro 2207 FPV Motor ](https://iflight-rc.eu/de-de/products/xing-e-pro-2207-fpv-motor?srsltid=AfmBOorZfJb61m3TZF4U7hq-KOzMObZ-45vVHunS8bDKBJENCsUe33gM)**
    <img border-effect="rounded" src="motor.jpg" alt="Picture of SpeedyBee F405 Mini BLS stack" width="400"/>
- **Frame | [FlyFishRC Volador II VX5](https://www.flyfish-rc.com/products/volador-ii-vx5-o3-fpv-freestyle-t700-frame-kit?variant=42215327170740):**
  - The frame is the base were every part of the drone is mounted on
- **Video Transmitter | [SpeedyBee TX800 VTX](https://www.speedybee.com/speedybee-tx800/):**
  - The video transmitter transmits the video signal of the FPV camera on a given channel.
  - This is an analog transmitter, therefor the FPV googles have to be compatible. DJI offers their own digital transition standard which has a better video quality, but it is way more expensive. 
- **FPV-Camera | [CADDXFPV Ratel Pro Analog](https://caddxfpv.com/products/caddxfpv-ratel-pro-analog-camera?srsltid=AfmBOopvcLiCMd0d08VYGrb2wajsdDMdZSaasnMHIc9Me2bdpfDDi-bh):**
  - The FPV camera captures the video which send to the pilot to fligh the drone from first person view.
  - With the camera a camera controller is shipped, but this is not necessary because the controls can be covered by the flight controller
- **ELRS-Receiver | [SpeedyBee Nano 2.4G 2.4G-TCXO 915M ExpressLRS ELRS Receiver](https://www.speedybee.com/speedybee-nano-2-4g-2-4g-tcxo-915m-expresslrs-elrs-receiver/)**
  - Via this receiver the flight controller receives the inputs from the remote to control the drone
  - The used protocol is ExpressLRS, which is open source.
- **GPS Module: [HGLRC M100.5883 GPS](https://www.hglrc.com/products/m100-5883-gps?srsltid=AfmBOoq4Prd8-xOA7TuLEUwku7EqjJars7u9iBcFuTG9qOaUqb-IY-ut):**
- **Remote | [Radiomaster Zorro](https://www.radiomasterrc.com/products/zorro-radio-controller):**
  - The remote must have a software version installed which supports the protocol of the used receiver on the drone. 
    In our case it has to support ExpressLRS.
  - We flashed with [Buddy EdgeTx](https://buddy.edgetx.org/#/flash?version=v2.11.1&source=releases) the new software on the remote via USB-Connection. 
    In the case of the *Zorro* the top USB port must be used.
- Batterie pack
- FPV-Googles

## Soldering
The main part of the drone is the **Flight Controller (FC)** and **Motor Controller (MC)**
stack. First the *SpeedyBee F405 AIO 40A Bluejay* was used which is a combination of FC and MC in one, but during the
soldering of the drone a shortage damaged the FC.
<img border-effect="rounded" src="soldering_fc.jpg" alt="Picture of soldering plan of the FC" />

