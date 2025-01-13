import pytest
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
#from src.hidratatrack.main import HidrataTrackApp  # Substitua com o nome correto do arquivo.

class TestHidrataTrackApp:

    def setup_method(self):
        self.app = HidrataTrackApp()
        self.app.build()

    def teardown_method(self):
        self.app.stop()

    def test_create_profile_success(self):
        menu_screen = self.app.sm.get_screen("menu")
        menu_screen.ids.user_name.text = "João"
        menu_screen.ids.user_weight.text = "75"

        self.app.create_profile()

        assert self.app.user is not None
        assert self.app.daily_goal == 3750

    def test_create_profile_invalid_weight(self):
        menu_screen = self.app.sm.get_screen("menu")
        menu_screen.ids.user_name.text = "Maria"
        menu_screen.ids.user_weight.text = "invalid"

        with pytest.raises(ValueError):
            self.app.create_profile()

    def test_switch_to_tracker_without_profile(self):
        self.app.switch_to_tracker()
        assert self.app.sm.current == "login"

    def test_add_water(self):
        self.app.user = {"name": "Carlos", "weight": 80}
        self.app.daily_goal = 4000

        self.app.add_water(500)
        tracker_screen = self.app.sm.get_screen("tracker")

        assert self.app.progress == 500
        assert tracker_screen.ids.progress_label.text == "Progresso: 500 ml"

    def test_update_weight(self):
        self.app.user = {"name": "Ana", "weight": 60}
        self.app.daily_goal = 3000

        settings_screen = self.app.sm.get_screen("settings")
        settings_screen.ids.new_weight.text = "65"
        self.app.update_weight()

        assert self.app.user["weight"] == 65
        assert self.app.daily_goal == 3250
