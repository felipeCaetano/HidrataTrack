import pytest
from main import MainApp

def test_main_app_initialization():
    """Testa se a MainApp é inicializada corretamente."""
    app = MainApp()
    
    assert app is not None  # Garante que a instância foi criada
    # Se MainApp tiver um método para iniciar, podemos chamá-lo e verificar se não há erros
    if hasattr(app, "run"):
        app.run()  # Verifica se a aplicação inicia sem crash