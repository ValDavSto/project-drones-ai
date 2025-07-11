package cheatahh.android.drone.ui.widgets

import android.annotation.SuppressLint
import android.bluetooth.BluetoothDevice
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonColors
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.TextUnitType
import androidx.compose.ui.unit.dp
import cheatahh.android.drone.network.Address

@Composable
fun ReceiverDeviceOption(address: Address, onSelect: (Address) -> Unit) {
    Button(
        onClick = { onSelect(address) },
        modifier = Modifier
            .fillMaxWidth(1f)
            .padding(top = 10.dp),
        colors = ButtonColors(Color.Transparent, MaterialTheme.colorScheme.primary, Color.Transparent, Color.DarkGray),
        shape = RoundedCornerShape(10.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.secondary)
    ) {
        Text(
            text = address.value,
            textAlign = TextAlign.Center,
            modifier = Modifier
                .fillMaxWidth(1f)
                .padding(vertical = 10.dp),
            fontSize = TextUnit(6f, TextUnitType.Em)
        )
    }
}

@SuppressLint("MissingPermission")
@Composable
fun ReceiverBluetoothDeviceOption(device: BluetoothDevice, onSelect: (BluetoothDevice) -> Unit) {
    Button(
        onClick = { onSelect(device) },
        modifier = Modifier
            .fillMaxWidth(1f)
            .padding(top = 10.dp),
        colors = ButtonColors(Color.Transparent, MaterialTheme.colorScheme.primary, Color.Transparent, Color.DarkGray),
        shape = RoundedCornerShape(10.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.secondary)
    ) {
        Text(
            text = device.name ?: "Unknown Device",
            textAlign = TextAlign.Center,
            modifier = Modifier
                .fillMaxWidth(1f)
                .padding(vertical = 10.dp),
            fontSize = TextUnit(6f, TextUnitType.Em)
        )
    }
}