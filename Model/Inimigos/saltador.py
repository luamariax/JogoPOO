#Fica parado até o jogador entrar no raio de detecção, aí pula em direção a ele. 
#Interessante porque força o jogador a ter timing.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida

class Saltador(Entidade):
    def __init__(self, id: int, x: float, y: float):
        super().__init__(id)
        self.adicionar(ComponentePosicao(x, y, 32, 32)) #onde está e tamanho
        self.adicionar(ComponenteFisica(velocidade=3)) # para se mover
        self.adicionar(ComponenteIA("pular"))
        self.adicionar(ComponenteVida(hp=3))