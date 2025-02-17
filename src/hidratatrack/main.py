import logging
import sys
from datetime import date

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.utils.set_bars_colors import set_bars_colors    # Only for Android
from screens.createuserscreen.createuser import CreateUserScreen  # NoQA
from screens.login.loginscreen import LoginScreen  # NoQA
from screens.profile.createprofilescreen import CreateProfileScreen  # NoQA
from screens.profile.editprofilescreen import EditProfileScreen  # NoQA
from screens.trackerscreen.trackerscreen import TrackerScreen  # NoQA
from utils.snackbar_utils import show_snackbar  # NoQA

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,  # Nível do log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
    datefmt="%Y-%m-%d %H:%M:%S"  # Formato da data/hora
)


class NavigationService:
    def __init__(self, root):
        self.manager: MDScreenManager = root
        self.current_screen = None

    def switch_to(self, screen_name):
        if screen_name in self.manager.screen_names:
            self.current_screen = screen_name
            self.manager.current = self.current_screen
        else:
            raise ValueError(f"Screen {screen_name} not found")

    def get_current_screen(self):
        return self.current_screen


class MainApp(MDApp):

    def __init__(self):
        super(MainApp, self).__init__()
        self.date_dialog = None
        self.user = None
        self.navigation = None
        self.set_bars_colors()

    def build(self):
        self.title = "HidrataTrack"
        self.navigation = NavigationService(self.root)

    def set_bars_colors(self):
        set_bars_colors(
            self.theme_cls.primary_palette,  # status bar color
            self.theme_cls.primary_palette,  # navigation bar color
            "Light",  # icons color of status bar
        )

    def switch_to_create_account(self):
        self.navigation.switch_to("createuser")

    def switch_to_login(self):
        self.root.current = "login"

    def switch_to_tracker(self):
        """Switch to the tracker screen."""
        if not self.user:
            show_snackbar("Por favor, crie um perfil antes.")
            return
        self.root.current = "tracker"

    def switch_to_profile(self, user):
        """Switch to the profile screen."""
        self.user = user
        self.root.current = "create_profile"

    def switch_to_edit_profile(self, profile_id):
        """Switch to the edit profile screen."""
        if "edit_profile" not in self.root.screen_names:
            profile_screen = EditProfileScreen(profile_id)
            self.root.add_widget(profile_screen)
        self.root.get_screen("edit_profile").set_profile(profile_id)
        self.root.current = "edit_profile"


if __name__ == "__main__":
    Window.size = (350, 720)  # não use para android ou ios
    from services.database import create_db
    try:
        create_db()
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
    MainApp().run()
