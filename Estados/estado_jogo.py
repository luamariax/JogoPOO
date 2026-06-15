# Jogo rodando de fato. 
# Onde ficam os systems todos ativos. 
# Transita para EstadoPause ou EstadoGameOver.

import pygame

class EstadoJogo:
    def __init__(self, controlador):
        self.controlador = controlador
        self.rodando = True

    def entrar(self):
        print("Entrando no estado de jogo")

    def sair(self):
        print("Saindo do estado de jogo")

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.controlador.mudar_estado("pause")

    def atualizar(self):
        pass

    def desenhar(self, tela):
        tela.fill((135, 206, 235))
        pygame.display.flip()