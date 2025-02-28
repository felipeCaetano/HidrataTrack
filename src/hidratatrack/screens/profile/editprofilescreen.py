import logging
from datetime import date, datetime
from functools import partial

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog, MDDialogButtonContainer, MDDialogContentContainer,
    MDDialogHeadlineText, MDDialogIcon, MDDialogSupportingText
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.segmentedbutton import MDSegmentedButton

from src.hidratatrack.services.database import get_session
from src.hidratatrack.services.events import EventEmitter
from src.hidratatrack.services.profile_service import (
    get_profile_byid, update_profile)
from src.hidratatrack.utils.snackbar_utils import show_snackbar


def handle_events(msg):
    show_snackbar(msg)


class EditProfileScreen(MDScreen):
    def __init__(self, profile_id, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.profile_id = profile_id
        self.session = get_session()
        self.dialog = MDDialog()
        self.events = EventEmitter()
        self.events.on('profile-event', handle_events)

    def set_profile(self, profile_id):
        """Define o ID do perfil que será editado"""
        self.profile_id = profile_id

    def on_edit_confirm(self, *args):
        with self.session() as session:
            fields_values = self._get_fields()
            db_profile = get_profile_byid(self.profile_id, session)
            for key, value in fields_values.items():
                if value != "":
                    setattr(db_profile, key, fields_values[key])
            update_db = partial(update_profile, db_profile)
            Clock.schedule_once(update_db, .5)
            self.app.switch_to_tracker()

    def _get_fields(self):
        name = self.ids.name.text
        birth_date = self.ids.birth_date.text
        weight = self.ids.weight.text
        goal = self.ids.goal.text
        details = self.ids.details.text
        gender_selector: MDSegmentedButton = self.ids.gender_select
        gender = gender_selector.get_marked_items()
        gender_selected = ""
        if gender:
            gender_selected = gender[0].ids.container.children[0].text
        fields_list = [name, birth_date, weight, goal, gender_selected, details]
        if all([field == "" for field in fields_list]):
            show_snackbar("Preencha ou escolha algum campo!")
        else:
            logging.debug(f'Data de nascimento: {birth_date}')
            returned_fields = {
                'name': name,
                'birth_date': datetime.strptime(birth_date, '%d/%m/%Y') if
                birth_date != "" else "",
                'weight':weight,
                'goal':goal,
                'details':details,
                'gender': gender_selected,
            }
            return returned_fields

    def show_discard_dialog(self):
        self.dialog = MDDialog(
            MDDialogIcon(icon="human-edit"),
            MDDialogHeadlineText(text="Deseja Sair?"),
            MDDialogSupportingText(
                text="Ao clicar em sair nenhuma alteração será feita."
            ),
            MDDialogContentContainer(MDDivider(), orientation="vertical"),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancelar"),
                    style="text",
                    on_release=self.on_dismiss
                ),
                MDButton(
                    MDButtonText(text="Sair"),
                    style="text",
                    on_release=self.on_dialog_confirm
                ),
                spacing="8dp",
            ),
        )
        self.dialog.open()

    def show_options_menu(self):
        menu_items = [
            {
                "text": "Limpar campos",
                "on_release": lambda x: self.clear_fields(),
                "icon": "refresh"
            },
            {
                "text": "Ajuda",
                "on_release": lambda x: self.show_help(),
                "icon": "help-circle"
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.menu_button,
            items=menu_items,
            width_mult=3
        )
        self.menu.open()

    def on_dismiss(self, *args):
        self.dialog.dismiss()

    def on_dialog_confirm(self, *args):
        self.on_dismiss()
        self.app.switch_to_tracker()

    def show_date_picker(self, focus):
        if not focus:
            return

        self.date_dialog = MDDockedDatePicker(
            theme_bg_color="Custom",  # Cor principal do calendário
            scrim_color=(1, 1, 1, 0),  # Cor do texto dos botões
            theme_text_color="Secondary",  # Cor da data atual
            supporting_text="Selecione a data",
            sel_year=1983
        )
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

    def set_date_field(
            self, instance_date_picker, birth_date_field, pick_date):
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
