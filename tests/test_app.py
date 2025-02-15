def test_main_app_initialization(app):
    """Testa se a MainApp é inicializada corretamente."""
    assert app is not None  # Verifica se a aplicação foi criada

    # Verifica se a aplicação tem uma tela principal configurada
    assert hasattr(app, 'root') or hasattr(app, 'screen_manager')


def test_screens_loaded(app):
    """Testa se as telas foram carregadas corretamente."""
    screen_manager = app.root
    # 🔍 Verificar se o root está inicializado
    print(
        f"ScreenManager: {screen_manager}")
    if screen_manager:
        print(
            f"Telas disponíveis: {[
                screen.name for screen in screen_manager.screens]}"
        )

    # Verifica se a tela 'tracker' existe
    assert screen_manager is not None, "O screen_manager não foi inicializado!"
    assert screen_manager.has_screen('tracker')

    # Verifica se a tela 'login' existe
    assert screen_manager.has_screen('login')

