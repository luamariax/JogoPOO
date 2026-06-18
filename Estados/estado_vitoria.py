import pygame
from Estados.estado import Estado

class EstadoVitoria(Estado):
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.controlador.rodando = False
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_ESCAPE:
                    self.controlador.mudar_estado("menu")

    def desenhar(self):
        self.controlador.tela.desenhar_vitoria()
