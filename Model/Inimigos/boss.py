# Único, por fase ou no final do jogo. 
# Combina comportamentos dos outros — anda, pula e atira. Tem muito mais HP.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida

class Boss(Entidade):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.adicionar_componente("posicao", ComponentePosicao(x, y, 64, 64)) #onde está e tamanho
        self.adicionar_componente("fisica", ComponenteFisica(gravidade=True, no_chao=False)) # para se mover
        self.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="dano"))
        self.adicionar_componente("ia", ComponenteIA("combinar", velocidade=4))
        self.adicionar_componente("vida", ComponenteVida(hp=5))