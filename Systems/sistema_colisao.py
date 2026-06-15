#lê ComponentePosicao + ComponenteColisao → resolve sobreposições → preenche colidindo_com

from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.fisica import ComponenteFisica

class SistemaColisao:
    def verificar(self, entidades, jogador):
        fisica = jogador.obter(ComponenteFisica)
        posicao_jogador = jogador.obter(ComponentePosicao)
        
        fisica.no_chao = False  # reseta a cada frame
        
        for entidade in entidades:
            if entidade is jogador:
                continue  # não verifica colisão do jogador com ele mesmo
                
            colisao = entidade.obter(ComponenteColisao)
            if not colisao:
                continue  # só verifica entidades que têm ComponenteColisao
                
            if self.verificar_colisao(entidade, jogador):
                self._resolver(entidade, jogador)

    def _resolver(self, entidade, jogador):
        posicao_plat = entidade.obter(ComponentePosicao)
        posicao_jog = jogador.obter(ComponentePosicao)
        fisica = jogador.obter(ComponenteFisica)
        
        # jogador veio de cima — pousa na plataforma
        if fisica.vel_y > 0:
            posicao_jog.y = posicao_plat.y - posicao_jog.altura
            fisica.vel_y = 0
            fisica.no_chao = True

    def verificar_colisao(self, entidade, jogador):
        posicao_entidade = entidade.obter(ComponentePosicao)
        posicao_jogador = jogador.obter(ComponentePosicao)

        if (posicao_jogador.x < posicao_entidade.x + posicao_entidade.largura and
            posicao_jogador.x + posicao_jogador.largura > posicao_entidade.x and
            posicao_jogador.y < posicao_entidade.y + posicao_entidade.altura and
            posicao_jogador.y + posicao_jogador.altura > posicao_entidade.y):
            return True
        return False