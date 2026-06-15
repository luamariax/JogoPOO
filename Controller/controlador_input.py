#lê teclado → modifica ComponenteFisica do Jogador
# controller/controlador_input.py
import pygame
from Model.jogador import Jogador

class ControladorInput:
    """Lê as teclas e modifica o ComponenteFisica do jogador."""
    @staticmethod
    def processar_teclado(jogador):
        """Chamar a cada frame. Aplica velocidade horizontal baseada nas setas."""
        fisica = jogador.obter("fisica")
        if not fisica:
            return

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            fisica.vel_x = -5
        elif teclas[pygame.K_RIGHT]:
            fisica.vel_x = 5
        else:
            fisica.vel_x = 0

        # O pulo (K_SPACE) só será utilizado na Fase 2 com gravidade ativada
        # Por enquanto ignoramos