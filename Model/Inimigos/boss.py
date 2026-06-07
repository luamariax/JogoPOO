# Único, por fase ou no final do jogo. 
# Combina comportamentos dos outros — anda, pula e atira. Tem muito mais HP.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida

class Boss(Entidade):
    def __init__(self, id: int, x: float, y: float):
        super().__init__(id)
        self.adicionar(ComponentePosicao(x, y, 64, 64)) #onde está e tamanho
        self.adicionar(ComponenteFisica(velocidade=4)) # para se mover
        self.adicionar(ComponenteIA("combinar"))
        self.adicionar(ComponenteVida(hp=10))