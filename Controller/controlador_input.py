#lê teclado → modifica ComponenteFisica do Jogador

import pygame
import sys
from Model.Componentes.fisica import ComponenteFisica

class ControladorInput:
    def __init__(self):
        self.espaco_pressionado = False

    def processar_eventos(self, jogador, eventos):
        fisica = jogador.obter(ComponenteFisica)
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_RIGHT]:
            fisica.vel_x = fisica.velocidade
        elif teclas[pygame.K_LEFT]:
            fisica.vel_x = -fisica.velocidade
        else:
            fisica.vel_x = 0

        if teclas[pygame.K_SPACE]:
            if fisica.no_chao and not self.espaco_pressionado:
                fisica.vel_y = -10
                self.espaco_pressionado = True
        else:
            self.espaco_pressionado = False

        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    