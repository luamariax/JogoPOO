# model/entidade.py
class Entidade:
    """Classe base que armazena componentes. Nenhuma lógica de jogo aqui."""
    def __init__(self):
        self._componentes = {}

    def adicionar_componente(self, nome, componente):
        self._componentes[nome] = componente

    def obter_componente(self, nome):
        return self._componentes.get(nome)
