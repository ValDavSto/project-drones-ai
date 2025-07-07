# Power Supply

A challenge we faced while building our drone is how to power additional peripherals like the `Raspberry Pi`,
its `PI Camera Module`, the `Coral Edge TPU` and the [`Electro Magnet`](Package-Transportation.md).

Both the `PI Camera Module` and the `Coral Edge TPU` run directly off the `Raspberry Pi`'s internal power rail,
but the `Electro Magnet` requires a separate power supply. We also need to ensure that the `Raspberry Pi` has 
enough power to run all these peripherals without any issues.

Fortunately, the `Raspberry Pi` and the `Electro Magnet` share a common supply voltage of `5V`, 
allowing us to bundle them to a single high-amperage 5V power source.

As the 5V rail of the flight controller is shared between other peripherals, 
such as the `GPS Module` and the `Radio Transceiver`, and an additional 5V battery is not feasible due to 
weight constraints, we need to use the [9V3A](https://www.speedybee.com/speedybee-f405-mini-bls-35a-20x20-stack/#Parameters) 
rail instead.

An amperage of 3A is sufficient to power all components, as long as they stay in the specifications 
posed in the datasheets:
- `Coral Edge TPU USB`: max. 900mA | [coral.ai](https://coral.ai/static/files/Coral-USB-Accelerator-datasheet.pdf)
- `Electro Magnet`: ~250mA (measured) + relay overhead
- `Raspberry Pi Zero 2 W`: ~600mA*

`*` We could not verify the exact max. consumption of the `Raspberry Pi Zero 2 W` as there is no 
mentioning is official datasheets. Users report a consumption of around 600mA 
([cnx-software.com](https://www.cnx-software.com/2021/12/09/raspberry-pi-zero-2-w-power-consumption)) 
under full load, which roughly aligns with our own measurements. Assuming a 3A power supply, we would have
more than 1.5A available for the `Raspberry Pi`, so we should be fine (famous last words I guess).

Converting 9V to 5V when staying in a single digit amperage is straightforward, 
and we can use a simple buck step-down converter to achieve this.

<img border-effect="rounded" src="buck_step_down_front.png" alt="A photo showing the front-side of the buck step-down converter used."/>
<img border-effect="rounded" src="buck_step_down_back.png" alt="A photo showing the back-side of the buck step-down converter used."/>

Our choice uses a `4R7` inductor, allowing for a modular input voltage range of `4.5V` to `24V`. 
The potentiometer is used to adjust the relative output voltage to `5V`, assuming a somewhat stable 
`9V` input voltage.

Note that when running under high load, the converter reaches temperatures which can damage the 
silicon over time. The vendor recommends a maximum continuous current of `2.5A` for the converter,
which we should stay below with our setup. Additionally, the down-wind of our drone cools
the chip while flying, so we again, should be fine :)