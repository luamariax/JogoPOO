# Congela tudo, mostra menu de pausa. 
# Transita de volta para EstadoJogo ou para EstadoMenu.
import pygame
from Estados.estado import Estado

class EstadoPause(Estado):
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
                    self.controlador.mudar_estado("jogo")
                elif evento.key == pygame.K_ESCAPE:
                    self.controlador.rodando = False

    def desenhar(self):
        self.controlador.tela.desenhar_pause(self.controlador.indice_fase + 1)
