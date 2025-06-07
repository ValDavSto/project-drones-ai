package cheatahh.android.drone.receiver

import cheatahh.android.drone.network.Address
import java.net.Socket

private const val APPLICATION_ACK = "DroneUAS"

fun addressAcknowledge(address: Address) = Socket(address.value, 1337).use { socket ->
    socketAcknowledge(socket)
}

fun socketAcknowledge(socket: Socket) : Boolean {
    val bytes = APPLICATION_ACK.encodeToByteArray()
    socket.getOutputStream().write(bytes)
    return socket.getInputStream().readNBytes(bytes.size).contentEquals(bytes)
}