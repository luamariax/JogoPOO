# Recebe o offset da câmera antes de desenhar qualquer coisa.
# lê ComponentePosicao + ComponenteSprite → desenha na tela

import pygame

class TelaJogo:
    def __init__(self):
        pygame.init() #inicializa tudo do pygame
        
        info = pygame.display.Info() #pega informações da tela do usuário
        self.largura = info.current_w
        self.altura = info.current_h
        
        self.janela = pygame.display.set_mode((self.largura, self.altura)) #set_mode cria a janela com o tamanho da tela
        pygame.display.set_caption("JOGOPOO") #define o título da janela
        
        self.clock = pygame.time.Clock() #controla o FPS, vai ser usado no loop principal

        def desenhar(self, entidades):