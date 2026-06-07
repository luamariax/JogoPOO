#O inimigo base. Anda em linha reta, vira quando bate na parede ou chega na borda da plataforma. 
#Comportamento mais simples, bom para as primeiras fases.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida

class Caminhante(Entidade):
    def __init__(self, id: int, x: float, y: float):
        super().__init__(id)
        self.adicionar(ComponentePosicao(x, y, 32, 32)) #onde está e tamanho
        self.adicionar(ComponenteFisica(velocidade=2)) # para se mover
        self.adicionar(ComponenteIA("patrulhar"))
        self.adicionar(ComponenteVida(hp=3))