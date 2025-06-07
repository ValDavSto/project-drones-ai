package cheatahh.android.drone.network

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

fun threadedAddressEnumerator(addresses: AddressSequence, validateAddress: (Address) -> Boolean, onProgress: (Address, Boolean, Float) -> Unit, onFinish: () -> Unit) {
    val pool = Executors.newFixedThreadPool(10)
    try {
        addresses.forEachIndexed { i, address ->
            pool.execute {
                val success = validateAddress(address)
                onProgress(address, success, (i + 1) / addresses.count.toFloat())
            }
        }
    } finally {
        pool.shutdown()
        pool.awaitTermination(1, TimeUnit.MINUTES)
        onFinish()
    }
}