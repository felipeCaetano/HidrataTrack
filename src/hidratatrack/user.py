from datetime import date


class User:
    def __init__(self, nome, genero, data_nascimento, peso, detalhes):
        self.nome = nome
        self.genero = genero
        self.data_nascimento = data_nascimento
        self.idade = self.get_age()
        self.peso = peso
        self.detalhes = detalhes
        self.observers = []

    def add_observer(self, observer):
        """Adiciona um observador."""
        self.observers.append(observer)

    def notify_observers(self):
        """Notifica todos os observadores."""
        for observer in self.observers:
            observer.update()
    
    def get_age(self):
        """Calcula a idade do usuário conforme a data de nascimento."""
        today = date.today()

        age = today.year - self.data_nascimento.year
        if (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day):
            age -= 1
        return age
    
    def update_weight(self, value):
        """Atualiza o valor do peso do usuário para value"""
        if value > 0:
            self.peso = value
            self.notify_observers()
        else:
            raise ValueError("O peso deve ser maior que zero!")
        return self.peso
    