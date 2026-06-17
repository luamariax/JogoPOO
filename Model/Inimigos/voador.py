#Patrulha em trajetória fixa (horizontal ou senoidal). 
#Não é afetado pela gravidade. 
#Cobre os espaços aéreos que o Caminhante não alcança.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida
from Model.Componentes.sprite import ComponenteSprite
from Model.Componentes.animacao import ComponenteAnimacao

class Voador(Entidade):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.adicionar_componente("posicao", ComponentePosicao(x, y, 48, 48))
        self.adicionar_componente("fisica", ComponenteFisica(gravidade=False, no_chao=False))
        self.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="dano"))
        ia_comp = ComponenteIA("voar", velocidade=2)
        ia_comp.timer_pulo = 120
        self.adicionar_componente("ia", ia_comp)
        self.adicionar_componente("vida", ComponenteVida(hp=1))
        self.adicionar_componente("sprite", ComponenteSprite("abelha_voar_0"))
        anim = ComponenteAnimacao(
            animacoes={
                "voar": ["abelha_voar_0", "abelha_voar_1"],
            },
            velocidade=8
        )
        anim.estado_atual = "voar"
        self.adicionar_componente("animacao", anim)
