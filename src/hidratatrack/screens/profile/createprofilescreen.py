from datetime import date, datetime

from kivymd.app import MDApp
from kivymd.uix.segmentedbutton import MDSegmentedButton
from kivymd.uix.screen import MDScreen

from models.perfil import Profile


class CreateProfileScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
    
    # def on_start(self):
    #     self.ids.gender_select.adjust_segment_radius(15)

    def create_profile(self):
        """Create a user profile and calculate the daily water goal."""
        
        user_name = self.ids.name.text.strip()
        birth_date = self.ids.birth_date.text
        user_weight = self.ids.weight.text
        gender_selector: MDSegmentedButton = self.ids.gender_select
        details = self.ids.details.text
        try:
            gender = gender_selector.get_marked_items()[0]._label.text
        except IndexError:
            force_selected = gender_selector.get_items()[1]
            gender_selector.mark_item(force_selected)
            gender = gender_selector.get_marked_items()[1]._label.text

        if not birth_date:
            self.show_snackbar("Data de nascimento inválida")
            return
        else:
            date_obj = datetime.strptime(birth_date, '%d/%m/%Y')

        if not all([user_name, user_weight, gender, date_obj]):
            self.app.show_snackbar("Por favor, preencha todos os campos.")
            return
        
        user_profile = Profile(
            nome=user_name,
            genero=gender,
            data_nascimento=date_obj,
            peso=user_weight,
            detalhes=details)
        
        self.app.user.profile = user_profile
        self.app.daily_goal = self.app.user.profile.daily_goal
        if self.app.user.profile is not None:
            self.app.save_profile(user_profile)
            # self.app.show_snackbar(
            #     f"Perfil criado: {self.app.user.profile.nome}"
            #     )
            self.app.switch_to_tracker()