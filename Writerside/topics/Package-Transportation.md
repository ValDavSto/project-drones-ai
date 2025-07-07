# Package Transportation

Our drone is required to handle payload pickup and drop-off of a prepared package.

## Grip Methods

There are a couple of ways a drone can hold on to a given package. During our research, 
we explored the following systems:

- `Mechanical Grippers or Claws`, where servo motors are used to open 
and close a gripping mechanism. While this approach yields a good in-flight 
performance for irregular or non-metallic items, pickup also requires 
accurate alignment to properly connect with any payload. 

- `Fixed Hooks or Clips`, where the drone flyes by the package and hooks 
into it, effectively picking it up upon flight. This allows for passive pickup 
and drop-off, without electronic controls. However, the minimalistic design requires accurate 
alignment and properly prepared packages with possibilities to hook into. This also results 
in the drone not being able to drop off the package mid-flight.

- `Electromagnetic Systems`, where an electromagnet is used to attach to magnet-fitted 
packages. The magnet is controlled via the drone and can be turned on to hold on to the 
package or turned off in order to drop the package. While this approach is energy intensive, 
it requires less flight accuracy when pickup or drop-off.

Due to our not existing flight skills combined with the fast pickup and drop-off, we decided 
to build a solution using an electromagnet.

## Grip System

For our purposes, we chose an electromagnet with a pulling strength of ~25 newtons, 
yielding in a theoretical grip strength of:

$$
m = \frac{F}{g} = \frac{25}{9.81} \approx 2.55\ \text{kg}
$$

However, factors like surface area contact between the magnet and object, air gaps or misalignment and flight winds
reduce the effective strength significantly.

The electromagnet is powered with continuous 5V DC and pulls ~250mA while operating. As an electromagnet of this 
magnitude has no electronic polarity, there is no V+ or V-, just two cables that we can connect in either direction.

<img border-effect="rounded" src="electromagnet.png" alt="A photo showing the electromagnet used."/>

As the pickup and drop-off shall happen on command, we need to connect it to our on-board `Raspberry Pi Zero` 
computer. Unfortunately, the 5V rail of such is not capable of continuously delivering 1.25W, especially 
considering an electromagnet tends to spike energy consumption when turned on.

The solution: a `Relay`

A `Relay` is an electronic component that controls an isolated electronic circuit with inputs from another. 
As our `Raspberry Pi` is already powered by a 5V DC source, we can reuse the same source to power the
electromagnet and toggle the connection via the low-amperage GPIO output of the `Raspberry Pi`.

A `Relay` is connected as such:

<img border-effect="rounded" src="relay.png" alt="A photo showing the relay used and how it is connected."/>
<img border-effect="rounded" src="electromagnet_wiring.png" alt="A photo showing the complete wiring for powering the electromagnet."/>

In our programs, we chose the pin `GPIO #23` for controls, but any other will do. As our `Common Circuit` 
(electromagnet) uses 5V, our `Control Circuit` (gpio) needs to be at a lower voltage (potential difference) 
in order to give the `Relay` some operation headroom. Thus, we went with the static 3.3V output rail. 
Alternatively a resistor of ~100$\Omega$ would have done the trick.

The relay toggles `COM` (Common Power) between `NO` (Normal Open, powered if relay is open = low flag on `IN`) 
and (Normal Closed, powered if relay is closed = high flag on `IN`). As we identify a high flag with magnet=on, 
we went with the `NC` port for the magnet circuit.

## Boxed Solution

In order to make the entire solution more resistant against potential impacts, we decided to pack all hardware
into a pvc pipe:

<img border-effect="rounded" src="boxed_electromagnet1.png" alt="A photo showing the finished electromagnet box."/>
<img border-effect="rounded" src="boxed_electromagnet2.png" alt="A photo showing the finished electromagnet box."/>

It looks like a pipe-bomb and probably should not be brought to an airport, but serves its purpose. 