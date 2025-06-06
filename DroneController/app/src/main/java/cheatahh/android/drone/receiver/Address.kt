package cheatahh.android.drone.receiver

import cheatahh.android.drone.network.Address
import cheatahh.android.drone.network.AddressSequence

fun addressSequence() = AddressSequence(256, sequence {
    val subnet = "192.168.19"
    for(x in 0 .. 255) yield(Address("$subnet.$x"))
})