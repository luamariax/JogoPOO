#Patrulha em trajetória fixa (horizontal ou senoidal). 
#Não é afetado pela gravidade. 
#Cobre os espaços aéreos que o Caminhante não alcança.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida

class Voador(Entidade):
    def __init__(self, id: int, x: float, y: float):
        super().__init__(id)
        self.adicionar(ComponentePosicao(x, y, 32, 32)) #onde está e tamanho
        self.adicionar(ComponenteFisica(velocidade=3, gravidade=False)) # para se mover
        self.adicionar(ComponenteIA("voar"))
        self.adicionar(ComponenteVida(hp=3))