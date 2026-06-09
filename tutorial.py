#DESIGN PATTERNS

import pygame




class Jogador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_x = 0
        self.vel_y = 0

    def atualizar(self, teclas):
        self.vel_x = 0
        if teclas[pygame.K_LEFT]:
            self.vel_x = -5
        if teclas[pygame.K_RIGHT]:
            self.vel_x = 5
        self.rect.x += self.vel_x

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 0, 0), self.rect)

class Jogo:
    def __init__(self):
        self.tela = pygame.display.set_mode((360,480))
        self.relogio = pygame.time.Clock()
        self.jogador = Jogador(180,240)
        self.rodando = True

    def executar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
        
            teclas = pygame.key.get_pressed()
            self.jogador.atualizar(teclas)

            self.tela.fill((0,0,0))
            self.jogador.desenhar(self.tela)
            pygame.display.flip()
            self.relogio.tick(30)
        pygame.quit()

main = Jogo()
main.executar()