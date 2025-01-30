# services/events.py
from typing import Callable, Dict, List
class EventEmitter:
    """Sistema de eventos simples para desacoplar componentes."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.listeners: Dict[str, List[Callable]] = {}
        return cls._instance
    
    def on(self, event: str, callback: Callable) -> None:
        """Registra um callback para um evento."""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
    
    def emit(self, event: str, *args, **kwargs) -> None:
        """Emite um evento para todos os listeners registrados."""
        if event in self.listeners:
            for callback in self.listeners[event]:
                callback(*args, **kwargs)
