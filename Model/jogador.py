from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica

class Jogador(Entidade):
    def __init__(self, id: int, x: float, y: float):
        super().__init__(id)
        self.adicionar(ComponentePosicao(x, y, 32, 48)) #onde está e tamanho
        self.adicionar(ComponenteFisica(velocidade=4)) # para se mover