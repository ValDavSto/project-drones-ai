package cheatahh.android.drone.receiver

import android.bluetooth.BluetoothSocket
import java.net.Socket

enum class Action(val label: String) {
    DISCONNECT("Disconnect"),
    PACKAGE_PICK("Pick Package"),
    PACKAGE_DROP("Drop Package");
    operator fun invoke(socket: Socket) {
        val out = socket.getOutputStream()
        out.write(ordinal)
        out.flush()
    }
    operator fun invoke(socket: BluetoothSocket) {
        val out = socket.outputStream
        out.write(ordinal)
        out.flush()
    }
}