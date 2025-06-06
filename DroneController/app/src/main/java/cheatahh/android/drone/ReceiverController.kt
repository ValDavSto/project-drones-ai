package cheatahh.android.drone

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.sp
import cheatahh.android.drone.ReceiverController.Intents.RECEIVER_ADDRESS
import cheatahh.android.drone.network.Address
import cheatahh.android.drone.ui.theme.DroneControllerTheme

class ReceiverController : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val address = Address(requireNotNull(intent.extras?.getString(RECEIVER_ADDRESS)))
        setContent {
            DroneControllerTheme {
                Box(
                    modifier = Modifier
                        .fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = address.value,
                        color = MaterialTheme.colorScheme.primary,
                        fontSize = 24.sp
                    )
                }
            }
        }
    }
    object Intents {
        const val RECEIVER_ADDRESS = "receiverAddress"
    }
}