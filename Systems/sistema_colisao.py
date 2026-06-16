#lê ComponentePosicao + ComponenteColisao → resolve sobreposições → preenche colidindo_com
# systems/sistema_colisao.py
import pygame
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.fisica import ComponenteFisica

MARGEM_BROAD_PHASE = 200 #define quantos pixels além do rect do jogador o sistema vai considerar

class SistemaColisao:
    """Resolve colisões entre jogador e plataformas sólidas."""

    def resolver_colisoes_x(self, jogador, plataformas):
        posicao_jog = jogador.obter_componente("posicao")
        fisica = jogador.obter_componente("fisica")
        if not posicao_jog or not fisica:
            return
        rect_jog = pygame.Rect(posicao_jog.rect)
        candidatas = self._broad_phase(rect_jog, plataformas)
        for plat in candidatas:
            posicao_plat = plat.obter_componente("posicao")
            if not posicao_plat:
                continue
            rect_plat = pygame.Rect(posicao_plat.rect)
            if rect_jog.colliderect(rect_plat):
                if rect_jog.centerx < rect_plat.centerx:
                    posicao_jog.x = rect_plat.left - rect_jog.width
                else:
                    posicao_jog.x = rect_plat.right
                rect_jog.topleft = (posicao_jog.x, posicao_jog.y)

    def resolver_colisoes_y(self, jogador, plataformas):
        posicao_jog = jogador.obter_componente("posicao")
        fisica = jogador.obter_componente("fisica")
        if not posicao_jog or not fisica:
            return
        fisica.no_chao = False
        rect_jog = pygame.Rect(posicao_jog.rect)
        candidatas = self._broad_phase(rect_jog, plataformas)
        for plat in candidatas:
            posicao_plat = plat.obter_componente("posicao")
            if not posicao_plat:
                continue
            rect_plat = pygame.Rect(posicao_plat.rect)
            if rect_jog.colliderect(rect_plat):
                if fisica.vel_y >= 0:
                    posicao_jog.y = rect_plat.top - rect_jog.height
                    fisica.vel_y = 0
                    fisica.no_chao = True
                else:
                    posicao_jog.y = rect_plat.bottom
                    fisica.vel_y = 0
                rect_jog.topleft = (posicao_jog.x, posicao_jog.y)

    def _broad_phase(self, rect_jog, plataformas):
        zona = rect_jog.inflate(MARGEM_BROAD_PHASE * 2, MARGEM_BROAD_PHASE * 2)
        return [
            p for p in plataformas
            if (posicao := p.obter_componente("posicao")) and zona.colliderect(posicao.rect)
        ]
