from datetime import date, datetime

from kivymd.app import MDApp
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.segmentedbutton import MDSegmentedButton
from services.profile_service import create_profile  # NoQA
from utils.snackbar_utils import show_snackbar  # NOQA

from src.hidratatrack.services.events import EventEmitter


class CreateProfileScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        self.events = EventEmitter()
        self.date_dialog = MDDockedDatePicker(
            theme_bg_color="Custom",  # Cor principal do calendário
            scrim_color=(1, 1, 1, 0),  # Cor do texto dos botões
            theme_text_color="Secondary",  # Cor da data atual
            supporting_text="Selecione a data",
            sel_year=1983,
        )

    def create_profile(self):
        """Create a user profile and calculate the daily water goal."""
        date_obj, detls, gender, pfl_name, pfl_weight = self._get_profile_fields()

        user_profile = create_profile(
            self.app.user, pfl_name, date_obj, gender, pfl_weight, detls
        )
        self.app.user.profiles.append(user_profile)
        if self.app.user.profiles is not None:
            self.app.switch_to_tracker()

    def _get_profile_fields(self):
        date_obj = None
        name = self.ids.name.text.strip()
        birth_date = self.ids.birth_date.text
        weight = self.ids.weight.text
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
            date_obj = datetime.strptime(birth_date, "%d/%m/%Y")
        if not all([name, weight, gender, date_obj]):
            self.events.emit("profile-warning", "Por favor, preencha todos os campos.")
            return
        return date_obj, details, gender, name, weight

    def show_date_picker(self, focus):
        if not focus:
            return

        self.date_dialog.bind(
            on_ok=self.on_ok,
            on_select_day=self.on_select_day,
            on_cancel=self.on_cancel_date,
        )
        self.date_dialog.open()

    def on_ok(self, instance_date_picker):
        pick_date = instance_date_picker.get_date()[0]
        birth_date_field = self.ids.birth_date
        self.set_date_field(instance_date_picker, birth_date_field, pick_date)

    def set_date_field(self, instance_date_picker, birth_date_field, pick_date):
        birth_date_field.text = pick_date.strftime("%d/%m/%Y")
        instance_date_picker.dismiss()

    def on_select_day(self, instance, value):
        """Esta função será chamada quando uma data for selecionada"""
        birth_date_field = self.ids.birth_date
        data = date(instance.sel_year, instance.sel_month, value)
        self.set_date_field(instance, birth_date_field, data)

    def on_cancel_date(self, instance):
        """Esta função será chamada quando o usuário cancelar a seleção"""
        instance.dismiss()
