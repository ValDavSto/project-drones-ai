package cheatahh.android.drone.ui.widgets

import android.annotation.SuppressLint
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.TextUnitType
import androidx.compose.ui.unit.dp
import cheatahh.android.drone.network.Address
import cheatahh.android.drone.network.AddressSequence
import cheatahh.android.drone.network.threadedAddressEnumerator
import kotlin.concurrent.thread

@Composable
fun ReceiverDeviceSelector(addresses: AddressSequence, validateAddress: (Address) -> Boolean, onSelect: (Address) -> Unit) {
    var progress by remember { mutableFloatStateOf(0f) }
    val devices = remember { mutableStateListOf<Address>().apply stream@ {
        thread {
            threadedAddressEnumerator(addresses, validateAddress,
                { address, success, current ->
                    if (success) this@stream += address
                    progress = maxOf(progress, current)
                }, {
                    this@stream.sortBy { it.value.substringAfterLast('.').toInt() }
                }
            )
        }
    } }
    Column(
        modifier = Modifier
            .padding(start = 30.dp, top = 60.dp, end = 30.dp, bottom = 30.dp)
            .fillMaxWidth(1f)
    ) {
        Text(
            text = "Select Receiver${if (devices.isEmpty()) "" else " (${devices.size})"}",
            color = MaterialTheme.colorScheme.primary,
            textAlign = TextAlign.Center,
            modifier = Modifier
                .fillMaxWidth(1f)
                .padding(bottom = 3.dp),
            fontSize = TextUnit(8f, TextUnitType.Em)
        )
        LinearProgressIndicator(
            progress = { progress },
            color = MaterialTheme.colorScheme.primary,
            trackColor = MaterialTheme.colorScheme.secondary,
            modifier = Modifier
                .fillMaxWidth(1f)
                .height(2.dp)
        )
        if (devices.isNotEmpty()) LazyColumn {
            items(devices) { address ->
                ReceiverDevice(address, onSelect)
            }
        } else Text(
            text = "No receivers found.",
            color = MaterialTheme.colorScheme.secondary,
            modifier = Modifier
                .fillMaxWidth(1f)
                .padding(top = 10.dp)
        )
    }
}

@Preview
@Composable
@SuppressLint("UnrememberedMutableState")
fun ReceiverDeviceSelectorPreview() {
    val addresses = AddressSequence(3, mutableListOf(
        Address("192.168.0.1"),
        Address("192.168.0.2"),
        Address("192.168.0.3")
    ).asSequence())
    ReceiverDeviceSelector(addresses, { true }) {}
}