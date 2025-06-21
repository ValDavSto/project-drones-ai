package cheatahh.android.drone.receiver

import cheatahh.android.drone.network.Address
import cheatahh.android.drone.network.AddressSequence

fun addressSequence24(subnet: String) = AddressSequence(256, sequence {
    for(x in 0 .. 255) yield(Address("$subnet.$x"))
})