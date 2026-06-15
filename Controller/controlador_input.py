# lê teclado → modifica ComponenteFisica do Jogador

import pygame

class ControladorInput:
    VELOCIDADE_X = 5
    FORCA_PULO = -10  # negativo porque y cresce para baixo no pygame

    @staticmethod
    def processar_teclado(jogador):
        fisica = jogador.obter_componente("fisica")
        if not fisica:
            return
        teclas = pygame.key.get_pressed()
        ControladorInput._processar_movimento_horizontal(fisica, teclas)
        ControladorInput._processar_pulo(fisica, teclas)

    @staticmethod
    def _processar_movimento_horizontal(fisica, teclas):
        
        if teclas[pygame.K_LEFT]:
            fisica.vel_x = -ControladorInput.VELOCIDADE_X
        elif teclas[pygame.K_RIGHT]:
            fisica.vel_x = ControladorInput.VELOCIDADE_X
        else:
            fisica.vel_x = 0

    @staticmethod
    def _processar_pulo(fisica, teclas):
        
        if teclas[pygame.K_SPACE] and fisica.no_chao:
            fisica.vel_y = ControladorInput.FORCA_PULO
            fisica.no_chao = False
