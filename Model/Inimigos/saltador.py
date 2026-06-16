#Fica parado até o jogador entrar no raio de detecção, aí pula em direção a ele. 
#Interessante porque força o jogador a ter timing.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida

class Saltador(Entidade):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.adicionar_componente("posicao", ComponentePosicao(x, y, 32, 32)) #onde está e tamanho
        self.adicionar_componente("fisica", ComponenteFisica(gravidade=True, no_chao=False))
        self.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="dano"))
        self.adicionar_componente("ia", ComponenteIA("pular", velocidade=3))
        self.adicionar_componente("vida", ComponenteVida(hp=1))