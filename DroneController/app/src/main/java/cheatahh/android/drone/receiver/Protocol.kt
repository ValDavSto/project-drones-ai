package cheatahh.android.drone.receiver

import cheatahh.android.drone.network.Address

private const val APPLICATION_ACK = "DroneUAS"

fun addressAcknowledge(address: Address) = true
/*Socket(address, 1337).use { device ->
    val bytes = APPLICATION_ACK.encodeToByteArray()
    device.getOutputStream().write(bytes)
    require(device.getInputStream().readNBytes(bytes.size).contentEquals(bytes))
}*/