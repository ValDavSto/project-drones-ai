package cheatahh.android.drone.receiver

import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import cheatahh.android.drone.network.Address
import java.net.Socket
import java.util.UUID

private const val APPLICATION_ACK = "DroneUAS"
val SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB") as UUID

fun addressAcknowledge(address: Address) = Socket(address.value, 1337).use { socket ->
    //socket.oobInline = true
    val result = socketAcknowledge(socket)
    if(result) Action.DISCONNECT(socket)
    result
}

@SuppressLint("MissingPermission")
fun addressAcknowledge(device: BluetoothDevice) = device.createRfcommSocketToServiceRecord(SPP_UUID).use { socket ->
    socket.connect()
    val result = socketAcknowledge(socket)
    if(result) Action.DISCONNECT(socket)
    result
}

fun socketAcknowledge(socket: Socket) : Boolean {
    val bytes = APPLICATION_ACK.encodeToByteArray()
    socket.getOutputStream().write(bytes)
    return socket.getInputStream().readNBytes(bytes.size).contentEquals(bytes)
}

fun socketAcknowledge(socket: BluetoothSocket) : Boolean {
    val bytes = APPLICATION_ACK.encodeToByteArray()
    socket.outputStream.write(bytes)
    return socket.inputStream.readNBytes(bytes.size).contentEquals(bytes)
}
