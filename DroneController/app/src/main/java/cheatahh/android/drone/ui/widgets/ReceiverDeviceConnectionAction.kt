package cheatahh.android.drone.ui.widgets

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonColors
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import cheatahh.android.drone.receiver.Action
import cheatahh.android.drone.ui.theme.Grey30
import cheatahh.android.drone.ui.theme.Grey40

@Composable
fun ReceiverDeviceConnectionAction(isLoading: Boolean, action: Action, onAction: (Action) -> Unit) {
    Button(
        onClick = { onAction(action) },
        modifier = Modifier.fillMaxWidth(0.5f),
        colors = ButtonColors(
            MaterialTheme.colorScheme.primary,
            MaterialTheme.colorScheme.onPrimary,
            Grey30,
            Grey40
        ),
        enabled = !isLoading
    ) {
        Text(
            text = action.label
        )
    }
}

@Preview
@Composable
fun ReceiverDeviceConnectionActionPreview() {
    ReceiverDeviceConnectionAction(false, Action.PACKAGE_DROP) {}
}