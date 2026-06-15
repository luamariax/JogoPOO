# view/tela_jogo.py
import pygame
from Model.jogador import Jogador

class TelaJogo:
    """Gerencia a janela e o desenho. Inicializa o pygame."""
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.largura = info.current_w
        self.altura = info.current_h
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("JOGOPOO - Fase 1")
        self.relogio = pygame.time.Clock()

    def desenhar(self, jogador):
        """Recebe a entidade jogador e desenha um retângulo na posição atual."""
        self.tela.fill((50, 50, 100))          # fundo escuro
        pos = jogador.obter("posicao")
        if pos:
            pygame.draw.rect(self.tela, (255, 0, 0), pos.rect)   # jogador vermelho
        pygame.display.flip()

    def tick(self, fps=60):
        self.relogio.tick(fps)

    def fechar(self):
        pygame.quit()