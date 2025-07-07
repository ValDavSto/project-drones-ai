package cheatahh.android.drone

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import cheatahh.android.drone.ReceiverController.Intents.RECEIVER_ADDRESS
import cheatahh.android.drone.network.Address
import cheatahh.android.drone.receiver.Action
import cheatahh.android.drone.receiver.socketAcknowledge
import cheatahh.android.drone.ui.theme.DroneControllerTheme
import cheatahh.android.drone.ui.widgets.ReceiverDeviceConnection
import java.io.DataInputStream
import java.net.Socket
import java.time.LocalTime
import java.time.format.DateTimeFormatter
import kotlin.concurrent.thread

const val RECEIVER_PORT = 1337

class ReceiverController : ComponentActivity() {
    private var socket: Socket? = null
    private val socketState = mutableIntStateOf(0)
    private val loadingState = mutableIntStateOf(0)
    private val messageState = mutableStateOf("")

    private fun disconnect() {
        try {
            socket?.close()
        } catch (_: Exception) {}
        socket = null
        socketState.intValue = 0
        loadingState.intValue = 0
        messageState.value = ""
    }

    private fun connect() {
        disconnect()
        val address = Address(requireNotNull(intent.extras?.getString(RECEIVER_ADDRESS)))
        try {
            socket = Socket(address.value, RECEIVER_PORT)
            val socket = socket!!
            //socket!!.oobInline = true
            require(socketAcknowledge(socket))
            socketState.intValue = 1
            loadingState.intValue = 0
            messageState.value = ""
            thread {
                val data = DataInputStream(socket.getInputStream())
                try {
                    while(true) {
                        val bytes = data.readNBytes(data.readUnsignedShort())
                        messageState.value = "${
                            LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm"))
                        }\n${bytes.decodeToString()}"
                    }
                } catch (_: Exception) {}
            }
        } catch (_: Exception) {
            disconnect()
            socketState.intValue = 2
        }
    }

    private fun executeAction(action: Action) {
        val socket = socket ?: return
        loadingState.intValue = 1
        thread {
            try {
                action(socket)
                runOnUiThread {
                    Toast.makeText(this@ReceiverController, "Command '${action.label}' sent.", Toast.LENGTH_SHORT).show()
                }
            } catch (_: Exception) {
                runOnUiThread {
                    Toast.makeText(this@ReceiverController, "Command '${action.label}' failed.", Toast.LENGTH_SHORT).show()
                }
            } finally {
                loadingState.intValue = 0
            }
            if(action == Action.DISCONNECT) runOnUiThread {
                this@ReceiverController.finish()
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            DroneControllerTheme {
                ReceiverDeviceConnection(socketState, loadingState, messageState, ::executeAction)
            }
        }
        thread { connect() }
    }

    override fun onDestroy() {
        super.onDestroy()
        thread { disconnect() }
    }

    object Intents {
        const val RECEIVER_ADDRESS = "receiverAddress"
    }
}