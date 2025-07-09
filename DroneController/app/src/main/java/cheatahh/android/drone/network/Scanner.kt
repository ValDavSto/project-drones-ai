package cheatahh.android.drone.network

import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.content.Context
import android.util.Log
import java.net.InetAddress
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

@JvmInline
value class Address(val value: String) {
    fun ping() = InetAddress.getByName(value).isReachable(200)
}
class AddressSequence(val count: Int, generator: Sequence<Address>) : Sequence<Address> by generator

fun getHotspotDevice(address: Address, onAcknowledge: (Address) -> Boolean) = runCatching {
    require(address.ping())
    onAcknowledge(address)
}.getOrNull() ?: false

fun getBluetoothDevice(device: BluetoothDevice, onAcknowledge: (BluetoothDevice) -> Boolean) = runCatching {
    onAcknowledge(device)
}.getOrNull() ?: false

fun threadedAddressEnumerator(addresses: AddressSequence, validateAddress: (Address) -> Boolean, onProgress: (Address, Boolean, Float) -> Unit, onFinish: () -> Unit) {
    val pool = Executors.newFixedThreadPool(10)
    try {
        addresses.forEachIndexed { i, address ->
            pool.execute {
                val success = validateAddress(address)
                Log.d("PING", "Target address $address responded with $success")
                onProgress(address, success, (i + 1) / addresses.count.toFloat())
            }
        }
    } finally {
        pool.shutdown()
        pool.awaitTermination(1, TimeUnit.MINUTES)
        onFinish()
    }
}

@SuppressLint("MissingPermission")
fun threadedBluetoothEnumerator(context: Context, validateDevice: (BluetoothDevice) -> Boolean, onProgress: (BluetoothDevice, Boolean, Float) -> Unit, onFinish: () -> Unit) {
    val pool = Executors.newFixedThreadPool(10)
    try {
        val bluetoothManager = context.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        val devices = bluetoothManager.adapter.bondedDevices.toList()
        devices.forEachIndexed { i, device ->
            pool.execute {
                val success = validateDevice(device)
                Log.d("PING", "Target address $device responded with $success")
                onProgress(device, success, (i + 1) / devices.size.toFloat())
            }
        }
    } finally {
        pool.shutdown()
        pool.awaitTermination(1, TimeUnit.MINUTES)
        onFinish()
    }
}