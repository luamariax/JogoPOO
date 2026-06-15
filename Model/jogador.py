from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.sprite import ComponenteSprite
from Model.Componentes.animacao import ComponenteAnimacao

class Jogador(Entidade):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.adicionar_componente("posicao", ComponentePosicao(x, y, 30, 30)) #onde está e tamanho
        self.adicionar_componente("fisica", ComponenteFisica(gravidade=True, no_chao=False)) # para se mover
        # solido=False porque o jogador não bloqueia a passagem de outras entidades
        # tipo="normal" porque reage à física (não é gatilho nem causa dano por contato)
        self.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="normal"))
        # frame inicial — SistemaAnimacao vai substituir a cada frame
        self.adicionar_componente("sprite", ComponenteSprite(
            chave_imagem="jogador_andar_direita_0"
        ))
        # sequências de frames por estado — chaves estão no GerenciadorRecursos
        self.adicionar_componente("animacao", ComponenteAnimacao(
            animacoes={
                "andar_direita":   ["jogador_andar_direita_0",  "jogador_andar_direita_1"],
                "andar_esquerda":  ["jogador_andar_esquerda_0", "jogador_andar_esquerda_1"],
            },
            velocidade=8  # troca de sprite a cada 8 frames (~7x por segundo a 60fps)
        ))
