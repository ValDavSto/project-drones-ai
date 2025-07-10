# Future Work

On this page we discuss what can be improved in the feature and added to the drone.

### Communication between Raspberry Pi and FC
In the current version of the drone, we were not successful in establishing communication with the flight controller (FC) via pin connections.
This should be possible and would eliminate the need for additional cables and adapters, which make the drone heavier and more prone to damage.

### Drone Construction

The off-the-shelf drone frame is not designed for adding additional hardware that is not usually used in FPV drones.
Therefore, there are no suitable mounting options for the electromagnet. As a result, the drone would constantly land on the electromagnet.

In a future iteration, a landing frame can be 3D-printed to protect the electromagnet.
Additionally, the hardware for the electromagnet could be designed in a more compact way.

The same issue applies to mounting the camera for image recognition, as the drone is supposed to have vision underneath.
There is currently no good mounting option for the camera.

### Autopilot
The current autopilot behavior still needs improvement. We didn't fully test if it actually flies stable, moves forward, or turns as intended.
With more time, a smarter system could be implemented – for example, flying around to search for a package, steering toward it, and picking it up automatically.