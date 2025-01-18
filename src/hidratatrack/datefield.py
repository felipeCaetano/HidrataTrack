from datetime import datetime
from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty


class DateField(MDTextField):
    formatted_date = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_text_validate = self.filter_date
        self.validator = 'date'
        self.date_format = 'dd/mm/yyyy'
        self._previous_value = ''
        
    def filter_date(self, *args):
        print(args)
        # Remove qualquer caractere não numérico
        numbers = ''.join(filter(str.isdigit, self.text))

        if len(numbers) > 8:
            numbers = numbers[:8]

        # Formata a data conforme digita
        formatted = ''
        if len(numbers) > 0:
            formatted = numbers[:2]
        if len(numbers) > 2:
            formatted += '/' + numbers[2:4]
        if len(numbers) > 4:
            formatted += '/' + numbers[4:8]

        # Atualiza o texto do campo apenas se houver mudança
        if formatted != self._previous_value:
            self._previous_value = formatted
            self.text = formatted  # Atualiza o texto diretamente
            self.formatted_date = formatted  # Sincroniza a data formatada

        # Retorna vazio pois a atualização já foi feita diretamente
        return ''

    
    def update_text(self, formatted_text):
        self.text = formatted_text
        self.formatted_date = formatted_text
        
    def get_date(self):
        """Converte a data formatada para objeto datetime"""
        try:
            if 8 <= len(self.formatted_date) < 11:  # Formato completo DD/MM/YYYY
                return datetime.strptime(self.formatted_date, '%d/%m/%Y')
            return None
        except ValueError:
            return None