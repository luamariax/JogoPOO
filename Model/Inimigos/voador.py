#Patrulha em trajetória fixa (horizontal ou senoidal). 
#Não é afetado pela gravidade. 
#Cobre os espaços aéreos que o Caminhante não alcança.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida

class Voador(Entidade):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.adicionar_componente("posicao", ComponentePosicao(x, y, 32, 32)) #onde está e tamanho
        self.adicionar_componente("fisica", ComponenteFisica(gravidade=False, no_chao=False)) # para se mover
        self.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="dano"))
        self.adicionar_componente("ia", ComponenteIA("voar", velocidade=2))
        self.adicionar_componente("vida", ComponenteVida(hp=1))