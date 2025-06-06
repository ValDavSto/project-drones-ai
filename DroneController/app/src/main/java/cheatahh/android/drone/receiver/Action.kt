package cheatahh.android.drone.receiver

import java.net.Socket

enum class Action(val label: String) {
    PACKAGE_PICK("Pick Package"),
    PACKAGE_DROP("Drop Package");
    fun execute(socket: Socket) {
        // TODO
    }
}