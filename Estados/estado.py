# Classe base abstrata
from abc import ABC, abstractmethod

class Estado(ABC):
    def __init__(self, controlador):
        self.controlador = controlador

    def entrar(self): pass
    def sair(self): pass

    @abstractmethod
    def processar_eventos(self): ...

    @abstractmethod
    def desenhar(self): ...

    def atualizar(self): pass
