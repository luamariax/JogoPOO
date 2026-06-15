# Recebe o offset da câmera antes de desenhar qualquer coisa.
# lê ComponentePosicao + ComponenteSprite → desenha na tela

import pygame
from Model.Componentes.posicao import ComponentePosicao
from Model.jogador import Jogador

class TelaJogo:
    def __init__(self):
        pygame.init()
        
        self.largura = 800
        self.altura = 600
        self.janela = pygame.display.set_mode((self.largura, self.altura))
        
        self.janela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("JOGOPOO")
        
        self.clock = pygame.time.Clock()

    def desenhar(self, entidades):
        self.janela.fill((30, 30, 30))
        
        for entidade in entidades:
            pos = entidade.obter(ComponentePosicao)
            if pos:
                if isinstance(entidade, Jogador):
                    cor = (0, 120, 255)
                else:
                    cor = (220, 50, 50)
                
                pygame.draw.rect(
                    self.janela,
                    cor,
                    (pos.x, pos.y, pos.largura, pos.altura)
                )
        
        pygame.display.flip()