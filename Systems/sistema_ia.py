#lê ComponenteIA de cada inimigo → modifica ComponenteFisica deles
import pygame
from Model.gerenciador_recursos import GerenciadorRecursos

VELOCIDADE_VOANDO = 8

class SistemaIA:
    def atualizar(self, inimigos: list, plataformas: list):
        for inimigo in inimigos:
            ia = inimigo.obter_componente("ia")
            if not ia:
                continue
            if ia.tipo == "patrulhar":
                self._atualizar_caminhante(inimigo, ia, plataformas)

    def _atualizar_caminhante(self, inimigo, ia, plataformas):
        posicao = inimigo.obter_componente("posicao")
        fisica  = inimigo.obter_componente("fisica")
        anim    = inimigo.obter_componente("animacao")
        sprite  = inimigo.obter_componente("sprite")
        if not posicao or not fisica or not anim or not sprite:
            return

        if ia.estado == "vivo":
            if fisica.no_chao and self._borda_a_frente(posicao, ia, plataformas):
                ia.direcao *= -1
            fisica.vel_x = ia.velocidade * ia.direcao
            sprite.flip_x = (ia.direcao == -1)
            if anim.estado_atual != "andar":
                anim.estado_atual = "andar"
                anim.frame_atual = 0
                anim.contador = 0

        elif ia.estado == "casco":
            fisica.vel_x = 0
            if anim.estado_atual != "casco":
                anim.estado_atual = "casco"
                anim.frame_atual = 0
                anim.contador = 0

        elif ia.estado == "voando":
            fisica.vel_x = VELOCIDADE_VOANDO * ia.direcao
            if anim.estado_atual != "voando":
                anim.estado_atual = "voando"
                anim.frame_atual = 0
                anim.contador = 0

    def _borda_a_frente(self, posicao, ia, plataformas) -> bool:
        x_sonda = posicao.x + ia.direcao * (posicao.largura + 2)
        y_sonda = posicao.y + posicao.altura + 4
        sonda = pygame.Rect(x_sonda, y_sonda, 4, 8)
        for plat in plataformas:
            pos_plat = plat.obter_componente("posicao")
            if pos_plat and sonda.colliderect(pos_plat.rect):
                return False
        return True
