#lê ComponentePosicao + ComponenteColisao → resolve sobreposições → preenche colidindo_com
# systems/sistema_colisao.py
import pygame
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.fisica import ComponenteFisica

MARGEM_BROAD_PHASE = 200 #define quantos pixels além do rect do jogador o sistema vai considerar

class SistemaColisao:
    """Resolve colisões entre jogador e plataformas sólidas."""

    def resolver_colisoes(self, jogador, plataformas):
        pos_jog = jogador.obter_componente("posicao")
        fisica = jogador.obter_componente("fisica")
        if not pos_jog or not fisica:
            return

        fisica.no_chao = False
        rect_jog = pygame.Rect(pos_jog.rect)  # cria Rect a partir da tupla
        candidatas = self._broad_phase(rect_jog, plataformas)

        for plat in candidatas:
            pos_plat = plat.obter_componente("posicao")
            if not pos_plat:
                continue
            rect_plat = pygame.Rect(pos_plat.rect)
            if rect_jog.colliderect(rect_plat):
                self._resolver_colisao(rect_jog, rect_plat, pos_jog, fisica)
                rect_jog.topleft = (pos_jog.x, pos_jog.y)

    #filtro de plataformas candidatas à colisão
    def _broad_phase(self, rect_jog, plataformas):
        zona = rect_jog.inflate(MARGEM_BROAD_PHASE * 2, MARGEM_BROAD_PHASE * 2)
        return [
            p for p in plataformas
            if (pos := p.obter_componente("posicao")) and zona.colliderect(pos.rect)
        ]

    def _resolver_colisao(self, rect_jog, rect_plat, pos_jog, fisica):
        overlap = rect_jog.clip(rect_plat)
        if overlap.width == 0 and overlap.height == 0:
            return

        if overlap.width < overlap.height:
            # Eixo horizontal
            if rect_jog.centerx < rect_plat.centerx:
                pos_jog.x = rect_plat.left - rect_jog.width
            else:
                pos_jog.x = rect_plat.right
        else:
            # Eixo vertical
            if fisica.vel_y >= 0:
                pos_jog.y = rect_plat.top - rect_jog.height
                fisica.vel_y = 0
                fisica.no_chao = True
            else:
                pos_jog.y = rect_plat.bottom
                fisica.vel_y = 0