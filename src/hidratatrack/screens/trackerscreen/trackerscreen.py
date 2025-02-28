import logging

from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, \
    MDDialogContentContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField, MDTextFieldHelperText, \
    MDTextFieldHintText, \
    MDTextFieldMaxLengthText
from services.events import EventEmitter  # NoQA
from utils.snackbar_utils import show_snackbar  # NoQA

from services.water_tracker import WaterTracker


class EditProfileContent(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.spacing = "16dp"
        self.padding = "24dp"
        self.adaptive_height = True

        # Nome
        self.name_field = MDTextField(
            MDTextFieldHintText(text="Nome"),
            MDTextFieldHelperText(text="altere o nome do peril",
                                  mode="persistent"),
            mode="outlined",
            size_hint_x=None,
            width="240dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            write_tab=False
        )

        # Peso
        self.weight_field = MDTextField(
            MDTextFieldHintText(text="Peso"),
            MDTextFieldHelperText(text="Peso em Kg", mode="persistent"),
            mode="outlined",
            size_hint_x=None,
            width="240dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            write_tab=False,
        )

        # Volume Personalizado
        self.volume_field = MDTextField(
            MDTextFieldHintText(text="volume em mL"),
            MDTextFieldHelperText(text="Helper text", mode="on_error"),
            MDTextFieldMaxLengthText(max_text_length=8),
            mode="outlined",
            size_hint_x=None,
            width="240dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            write_tab=False,
            input_filter="float"
        )

        self.add_widget(self.name_field)
        self.add_widget(self.weight_field)
        self.add_widget(self.volume_field)


class TrackerScreen(MDScreen):
    user_defined = 350

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alert_dialog = MDDialog()
        self.water_tracker = None
        self.profile_menu = None
        self.settings_menu = None
        self.profilemenu_items = None
        self.settingsmenu_items = None
        self.app = MDApp.get_running_app()
        self.events = EventEmitter()
        self.events.on("water_warning", self.handle_warning)
        self.events.on("water_added", self.handle_water_added)
        self.events.on("profile-not_found", self.handle_warning)

    def on_enter(self, *args):
        self.profilemenu_items = self.generate_menu_items(
            self.app.user.profiles, self.profilemenu_callback)
        self.settingsmenu_items = self.generate_menu_items(
            [
                "Criar Perfil",
                "Editar Perfil",
                "Editar Garrafa",
                "Zerar Consumo"
            ],
            self.settings_menu_callback
        )
        self.water_tracker = WaterTracker(self.app.user)
        self.set_profile_button(self.app.user.profiles)
        # self.update_goal()
        # logging.debug(self.water_tracker.current_profile)

    def set_profile_button(self, profile_list):
        self.ids.profile_button.text = self.water_tracker.current_profile.name

    def update_goal(self):
        self.daily_goal = round(self.water_tracker.daily_goal, 0)
        self.ids.daily_goal_label.text = f"Meta Diária: {self.daily_goal} mL"

    def generate_menu_items(self, items, callback):
        menu_items = []
        for index_item, item in enumerate(items):
            if hasattr(item, 'name'):
                menu_items.append({
                    "text": f"{item.name}",
                    "on_release": lambda x=f"{item.name}": callback(x)
                })
            else:
                if index_item == len(items) - 1:
                    menu_items.append({
                        "text": f"{item}",
                        "text_color": 'red',
                        "on_release": lambda x=f"{item}": callback(x)
                    })
                else:
                    menu_items.append({
                        "text": f"{item}",
                        "text_color": 'black',
                        "on_release": lambda x=f"{item}": callback(x)
                    })
        return menu_items

    @staticmethod
    def handle_warning(message: str):
        """Handler para avisos relacionados ao consumo de água."""
        show_snackbar(message)

    def handle_water_added(self, message: str):
        """Handler para quando água é adicionada."""
        # Atualiza progresso
        daily_total = self.water_tracker.get_current_intake()
        self.update_tracker_progress(daily_total)
        show_snackbar(message)

    def add_water(self, amount):
        profile = self.water_tracker.current_profile
        try:
            amount = float(amount)
            if not profile:
                self.events.emit("profile-not_found", "Selecione um perfil.")
                return
            self.water_tracker.add_water(amount, profile)
        except ValueError as e:
            show_snackbar(str(e))

    def update_tracker_progress(self, daily_total):
        """Atualiza os componentes da interface com os dados mais recentes."""
        self.update_goal()
        self.progress = self.water_tracker.get_progress()
        self.ids.progress_bar.value = self.progress
        self.ids.water_add.text = ""
        self.ids.progress_label.text = f"Progresso: {daily_total} mL"
        self.ids.bar_indicator.text = f"{self.progress} %"
        self.ids.profile_button.text = self.water_tracker.current_profile.name

    def menu_open(self):
        self.profile_menu = MDDropdownMenu(
            caller=self.ids.button,
            items=self.profilemenu_items,
            position='bottom',
            width=dp(160)
        )
        self.profile_menu.open()

    def profilemenu_callback(self, text_item):
        self.profile_menu.dismiss()
        self.ids.profile_button.text = text_item
        self.water_tracker.set_current_profile(text_item)
        self.update_goal()
        self.update_tracker_progress(self.water_tracker.get_current_intake())

    def show_settings(self):
        self.settings_menu = MDDropdownMenu(
            caller=self.ids.cog,
            items=self.settingsmenu_items,
            position='bottom',
            width=dp(160)
        )
        self.settings_menu.open()

    def settings_menu_callback(self, text_item):
        menu_actions = {
            "Criar Perfil": self.app.switch_to_profile,
            "Editar Perfil": self.app.switch_to_edit_profile,
            "Editar Garrafa": self.show_bottle_edit,
            "Zerar Consumo": self.show_alert_dialog
        }
        self.settings_menu.dismiss()
        if text_item == "Editar Perfil":
            if not self.water_tracker.current_profile:
                self.events.emit("profile-not_found", "Selecione um perfil.")
                return
            menu_actions[text_item](self.water_tracker.current_profile.id)
        elif text_item == "Criar Perfil":
            menu_actions[text_item](self.app.user)
        else:
            menu_actions[text_item]()

    def reset(self):
        self.water_tracker.reset()
        self.update_tracker_progress(0)

    def show_alert_dialog(self):
        self.alert_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Zerar o consumo?",
                halign="left",
            ),
            MDDialogSupportingText(
                text="Apagará todos os registros deste dia.",
                halign="left",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Cancelar"),
                         on_release=self.on_dialog_cancel),
                MDButton(
                    MDButtonText(text="Zerar",
                                 theme_text_color='Custom',
                                 text_color="red"),
                    style="elevated",
                    theme_shadow_color="Custom",
                    shadow_color="red",
                    on_release=self.on_dialog_confirm
                ),
                spacing="8dp",
            ),
        )
        self.alert_dialog.open()

    def show_bottle_edit(self):
        self.alter_txt_field = MDTextField(
            MDTextFieldHintText(text="volume em mL"),
            MDTextFieldHelperText(text="Valor longo!", mode="on_error"),
            MDTextFieldMaxLengthText(max_text_length=8),
            mode="outlined",
            size_hint_x=None,
            width="240dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            write_tab=False,
            input_filter="float"
        )

        self.alert_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Volume Personalizado:",
                halign="left",
            ),
            MDDialogContentContainer(self.alter_txt_field),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=self.on_dialog_cancel
                ),
                MDButton(
                    MDButtonIcon(
                        icon="water-plus",
                    ),
                    MDButtonText(
                        text="Personalizar",
                    ),
                    style="elevated",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_release=self.on_alter_bottle
                ),
                spacing="8dp",
            ),
        )
        self.alert_dialog.open()

    def show_profile_edit(self):
        self.alert_dialog = MDDialog(
            MDDialogHeadlineText(
                text="Editar Perfil:",
                halign="left",
            ),
            MDDialogContentContainer(EditProfileContent()),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Cancelar"),
                         on_release=self.on_dialog_cancel),
                MDButton(
                    MDButtonText(text="Editar"),
                    style="elevated",
                    theme_shadow_color="Custom",
                    shadow_color="green",
                    on_release=self.app.switch_to_edit_profile()
                ),
                spacing="8dp",
            ),
        )
        self.alert_dialog.open()

    def on_dialog_cancel(self, instance, *args):
        self.alert_dialog.dismiss()

    def on_dialog_confirm(self, *args):
        self.alert_dialog.dismiss()
        self.reset()

    def on_alter_bottle(self, *args):
        if self.alter_txt_field.text == '':
            self.events.emit('water_warning', 'O campo não pode estar vazio!')
            return
        else:
            try:
                self.user_defined = float(self.alter_txt_field.text)
                self.ids.text.text = f'{self.user_defined}mL'
                logging.debug(f'{self.ids.text.text=}')
            except ValueError:
                self.events.emit('water_warning',
                                 'Erro ao utilizar o valor!')
                logging.debug(f'{self.alter_txt_field.text=}')
        self.alert_dialog.dismiss()
