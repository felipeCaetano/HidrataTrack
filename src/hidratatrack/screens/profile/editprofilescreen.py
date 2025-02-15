from kivymd.uix.screen import MDScreen
from kivymd.uix.segmentedbutton import MDSegmentedButton


class EditProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_edit_confirm(self, *args):
        ...