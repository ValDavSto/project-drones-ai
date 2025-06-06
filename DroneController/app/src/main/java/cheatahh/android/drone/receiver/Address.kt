package cheatahh.android.drone.receiver

import cheatahh.android.drone.network.Address
import cheatahh.android.drone.network.AddressSequence

const val RECEIVER_SUBNET = "192.168.19"
const val RECEIVER_PORT = 1337

fun addressSequence() = AddressSequence(256, sequence {
    val subnet = RECEIVER_SUBNET
    for(x in 0 .. 255) yield(Address("$subnet.$x"))
})