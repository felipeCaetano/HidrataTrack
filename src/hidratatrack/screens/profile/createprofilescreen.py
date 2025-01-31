from datetime import datetime

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.segmentedbutton import MDSegmentedButton
from services.profile_service import create_profile, save_profile
from utils.snackbar_utils import show_snackbar  # NOQA

from src.hidratatrack.models.models import session


class CreateProfileScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

    def create_profile(self):
        """Create a user profile and calculate the daily water goal."""
        profile_name = self.ids.name.text.strip()
        birth_date = self.ids.birth_date.text
        profile_weight = self.ids.weight.text
        gender_selector: MDSegmentedButton = self.ids.gender_select
        details = self.ids.details.text
        try:
            gender = gender_selector.get_marked_items()[0]._label.text  # NOQA
        except IndexError:
            force_selected = gender_selector.get_items()[1]
            gender_selector.mark_item(force_selected)
            gender = gender_selector.get_marked_items()[1]._label.text  # NOQA

        if not birth_date:
            show_snackbar("Data de nascimento inválida")
            return
        else:
            date_obj = datetime.strptime(birth_date, '%d/%m/%Y')

        user_profile = create_profile(self.app.user, profile_name,  date_obj,
                                      profile_weight, gender, details)

        self.app.user.profile = user_profile
        self.app.daily_goal = self.app.user.profile.calculate_goal(
            user_profile.weight)
        if self.app.user.profile is not None:
            save_profile(self.app.user, user_profile, session)
            self.app.switch_to_tracker()
