from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.colisao import ComponenteColisao

class Jogador(Entidade):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.adicionar_componente("posicao", ComponentePosicao(x, y, 30, 30)) #onde está e tamanho
        self.adicionar_componente("fisica", ComponenteFisica(gravidade=True, no_chao=False)) # para se mover
        # solido=False porque o jogador não bloqueia a passagem de outras entidades
        # tipo="normal" porque reage à física (não é gatilho nem causa dano por contato)
        self.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="normal"))
