package cheatahh.android.drone.ui.widgets

import android.annotation.SuppressLint
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.MutableIntState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import cheatahh.android.drone.receiver.Action

@Composable
fun ReceiverDeviceConnection(connectionState: MutableIntState, loadingState: MutableIntState, onAction: (Action) -> Unit) {
    val connection by remember { connectionState }
    val isLoading by remember { loadingState }
    Box(
        modifier = Modifier
            .fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Column {
            Text(
                text = when(connection) {
                    0 -> "Connecting..."
                    1 -> "Connected"
                    else -> "Error"
                },
                color = when(connection) {
                    0, 1 -> MaterialTheme.colorScheme.primary
                    else -> MaterialTheme.colorScheme.error
                },
                fontSize = 24.sp,
                modifier = Modifier.fillMaxWidth(0.5f),
                textAlign = TextAlign.Center
            )
            if(isLoading != 0)LinearProgressIndicator(
                color = MaterialTheme.colorScheme.primary,
                trackColor = MaterialTheme.colorScheme.secondary,
                modifier = Modifier
                    .fillMaxWidth(0.5f)
                    .height(2.dp)
            )
            if(connection == 1) Column(
                modifier = Modifier.padding(top = if(isLoading != 0) 8.dp else 10.dp)
            ) {
                for(action in Action.entries) ReceiverDeviceConnectionAction(isLoading != 0, action, onAction)
            }
        }
    }
}

@Preview
@Composable
@SuppressLint("UnrememberedMutableState")
fun ReceiverDeviceConnectionPreview() {
    val connected = mutableIntStateOf(1)
    val isLoading = mutableIntStateOf(1)
    ReceiverDeviceConnection(connected, isLoading) {}
}