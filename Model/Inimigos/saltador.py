#Fica parado até o jogador entrar no raio de detecção, aí pula em direção a ele. 
#Interessante porque força o jogador a ter timing.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida
from Model.Componentes.sprite import ComponenteSprite
from Model.Componentes.animacao import ComponenteAnimacao


class Saltador(Entidade):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.adicionar_componente("posicao", ComponentePosicao(x, y, 64, 64)) #onde está e tamanho
        self.adicionar_componente("fisica", ComponenteFisica(gravidade=True, no_chao=False))
        self.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="dano"))
        self.adicionar_componente("vida", ComponenteVida(hp=1))
        self.adicionar_componente("sprite", ComponenteSprite("sapo_pular_0"))
        ia_comp = ComponenteIA("pular", velocidade=3)
        ia_comp.raio_deteccao = 700
        ia_comp.timer_pulo = 30
        self.adicionar_componente("ia", ia_comp)
        anim = ComponenteAnimacao(
            animacoes={
                "pular": ["sapo_pular_0", "sapo_pular_1", "sapo_pular_2",
                        "sapo_pular_3", "sapo_pular_4", "sapo_pular_5"],
                "morto": ["sapo_bye"],
                "parado": ["sapo_pular_0"],
            },
            velocidade=6
        )
        anim.estado_atual = "pular"
        self.adicionar_componente("animacao", anim)
