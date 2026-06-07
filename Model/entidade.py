from abc import ABC, abstractmethod

class Entidade(ABC):
    def __init__(self, id: int):
        self.id = id
        self.componentes = {}

    def adicionar(self, componente):
        self.componentes[type(componente)] = componente

    def obter(self, tipo):
        return self.componentes.get(tipo)
