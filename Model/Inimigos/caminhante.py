#O inimigo base. Anda em linha reta, vira quando bate na parede ou chega na borda da plataforma. 
#Comportamento mais simples, bom para as primeiras fases.

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.ia import ComponenteIA
from Model.Componentes.vida import ComponenteVida
from Model.Componentes.sprite import ComponenteSprite
from Model.Componentes.animacao import ComponenteAnimacao

class Caminhante(Entidade):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.adicionar_componente("posicao", ComponentePosicao(x, y, 48, 48)) #onde está e tamanho
        self.adicionar_componente("fisica", ComponenteFisica(gravidade=True, no_chao=False)) # para se mover
        self.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="dano"))
        self.adicionar_componente("ia", ComponenteIA("patrulhar", velocidade=2))
        self.adicionar_componente("vida", ComponenteVida(hp=2))
        self.adicionar_componente("sprite", ComponenteSprite("tatu_walk_0"))
        anim = ComponenteAnimacao(
            animacoes={
                "andar":  ["tatu_walk_0", "tatu_walk_1", "tatu_walk_2", "tatu_walk_3"],
                "casco":  ["tatu_death_1"],
                "voando": ["tatu_bye"],
            },
            velocidade=8
        )
        anim.estado_atual = "andar"
        self.adicionar_componente("animacao", anim)

