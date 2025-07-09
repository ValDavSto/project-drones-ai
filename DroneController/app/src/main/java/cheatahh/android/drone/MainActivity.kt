package cheatahh.android.drone

import android.Manifest
import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.core.app.ActivityCompat
import cheatahh.android.drone.network.getBluetoothDevice
import cheatahh.android.drone.network.getHotspotDevice
import cheatahh.android.drone.receiver.addressAcknowledge
import cheatahh.android.drone.receiver.addressSequence24
import cheatahh.android.drone.ui.theme.DroneControllerTheme
import cheatahh.android.drone.ui.widgets.ReceiverBluetoothDeviceSelector
import cheatahh.android.drone.ui.widgets.ReceiverDeviceSelector

const val RECEIVER_SUBNET = "192.168.19"
const val CONNECT_BLUETOOTH = true

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.BLUETOOTH_CONNECT, Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT, Manifest.permission.BLUETOOTH_ADMIN), 0)
        enableEdgeToEdge()
        setContent {
            DroneControllerTheme {
                if(CONNECT_BLUETOOTH)
                    ReceiverBluetoothDeviceSelector(this@MainActivity, { device -> getBluetoothDevice(device, ::addressAcknowledge) }) { device ->
                        startActivity(Intent(baseContext, ReceiverControllerBluetooth::class.java).putExtra(ReceiverControllerBluetooth.Intents.RECEIVER_ADDRESS, device.address))
                    }
                else
                    ReceiverDeviceSelector(addressSequence24(RECEIVER_SUBNET), { address -> getHotspotDevice(address, ::addressAcknowledge) }) { address ->
                        startActivity(Intent(baseContext, ReceiverController::class.java).putExtra(ReceiverController.Intents.RECEIVER_ADDRESS, address.value))
                    }
            }
        }
    }
}