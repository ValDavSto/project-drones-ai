# Rotors

Rotors are the spinning assemblies on a drone that provide necessary lift, thrust, and control. 
A standard quadcopter (4-rotor drone) has four rotors, each consisting of:

- A motor
- A propeller
- A mounting hub

<img border-effect="rounded" src="rotor_labeled.png" alt="A photo showing a rotor, labeled with motor, mounting and propeller."/>

The motor spins the propeller at high speeds, pushing air downwards and thereby creating lift through Newton’s Third Law (for every action, there's an equal and opposite reaction). 

## Propeller Orientation
The direction in which a propeller is mounted and spins determines how efficiently and correctly that lift is generated.
Propellers have a specific airfoil shape and pitch, they are twisted to force air downward as they spin. 
Correct orientation matters - If a blade is mounted with the wrong orientation, even if it's spinning in the correct direction, it may cause several issues:

- It won’t generate lift effectively.
- It could produce negative thrust or unstable airflow.
- The drone may fail to take off or become uncontrollable.

A correct orientation involves:

- The leading edge (thicker, more angled part) faces the direction of rotation.
- The curved surface of the blade faces up, and the flatter surface faces down.

<img border-effect="rounded" src="propeller_orientation.png" alt="A photo showing the correct and incorrect orientation of blades."/>

## Propeller Direction

To keep a drone stable and controllable in the air, neighboring pairs of rotors must spin in opposite directions:

- Two rotors spin clockwise (CW)
- Two spin counterclockwise (CCW)

<img border-effect="rounded" src="propeller_direction.png" alt="A photo showing a quadcopter with rotors labeled CW and CCW."/>

When a motor spins a rotor, it exerts an opposite torque on the drone’s frame, 
causing the body of the drone would spin in the opposite direction.
Counter-rotating rotors cancel out the rotational torque, keeping the drone stable.

Additionally, having rotors spin in opposite directions allows the drone to yaw(rotate around its vertical axis):
For example, in order to yaw right, the drone slows the CW rotors and speeds up the CCW rotors (or vice versa), creating an imbalance in torque.