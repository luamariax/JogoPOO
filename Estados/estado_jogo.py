# Jogo rodando de fato. 
# Onde ficam os systems todos ativos. 
# Transita para EstadoPause ou EstadoGameOver.

import pygame
from Estados.estado import Estado
from Controller.controlador_input import ControladorInput

class EstadoJogo(Estado):
    def entrar(self):
        fisica = self.controlador.jogador.obter_componente("fisica")
        if fisica:
            fisica.vel_x = 0

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.controlador.rodando = False
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    self.controlador.mudar_estado("pause")
                elif evento.key == pygame.K_ESCAPE:
                    self.controlador.rodando = False
        ControladorInput.processar_teclado(self.controlador.jogador)

    def atualizar(self):
        c = self.controlador
        c.sistema_fisica.atualizar_x(c.fase.entidades)
        c.sistema_colisao.resolver_colisoes_x(c.jogador, c.fase.plataformas)
        c.sistema_colisao.resolver_colisoes_inimigos_x(c.fase.inimigos, c.fase.plataformas)
        c.sistema_fisica.atualizar_y(c.fase.entidades)
        c.sistema_colisao.resolver_colisoes_y(c.jogador, c.fase.plataformas)
        c.sistema_colisao.resolver_colisoes_inimigos_y(c.fase.inimigos, c.fase.plataformas)
        c.sistema_ia.atualizar(c.fase.inimigos, c.fase.plataformas, c.jogador)
        c._verificar_pisar_inimigos()
        c.sistema_animacao.atualizar(c.fase.entidades)
        pos_jog = c.jogador.obter_componente("posicao")
        c.sistema_camera.atualizar(c.camera, pos_jog, c.fase.largura_mundo)

    def desenhar(self):
        c = self.controlador
        c.tela.desenhar_jogo(c.fase.entidades, c.camera)
