from kivy.metrics import dp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

def show_snackbar(msg):

        MDSnackbar(
            MDSnackbarText(
                text=msg,
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        ).open()