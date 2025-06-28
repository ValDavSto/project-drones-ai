package cheatahh.android.drone

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import cheatahh.android.drone.network.getHotspotDevice
import cheatahh.android.drone.receiver.addressAcknowledge
import cheatahh.android.drone.receiver.addressSequence24
import cheatahh.android.drone.ui.theme.DroneControllerTheme
import cheatahh.android.drone.ui.widgets.ReceiverDeviceSelector

const val RECEIVER_SUBNET = "192.168.19"

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            DroneControllerTheme {
                ReceiverDeviceSelector(addressSequence24(RECEIVER_SUBNET), { address -> getHotspotDevice(address, ::addressAcknowledge) }) { address ->
                    startActivity(Intent(baseContext, ReceiverController::class.java).putExtra(ReceiverController.Intents.RECEIVER_ADDRESS, address.value))
                }
            }
        }
    }
}