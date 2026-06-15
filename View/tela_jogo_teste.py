## view/tela_jogo.py
import pygame

class TelaJogo:
    def __init__(self, largura=None, altura=None):
        pygame.init()
        if largura is None or altura is None:
            info = pygame.display.Info()
            self.largura = info.current_w
            self.altura = info.current_h
        else:
            self.largura = largura
            self.altura = altura

        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("JOGOPOO")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 36)   # fonte padrão tamanho 36

    def desenhar_texto(self, texto, x, y, cor=(255,255,255)):
        """Desenha um texto centralizado em (x,y) se x for None, centraliza horizontal."""
        superficie = self.fonte.render(texto, True, cor)
        rect = superficie.get_rect()
        if x is None:
            x = self.largura // 2 - rect.width // 2
        self.tela.blit(superficie, (x, y))

    def desenhar_menu(self):
        """Tela de entrada (menu principal)."""
        self.tela.fill((30, 30, 60))                     # fundo escuro azulado
        self.desenhar_texto("JOGOPOO", None, 150, (255, 255, 0))
        self.desenhar_texto("Pressione ENTER para jogar", None, 250)
        self.desenhar_texto("Pressione ESC para sair", None, 300)
        pygame.display.flip()

    def desenhar_jogo(self, entidades, camera):
        """Tela do jogo – desenha jogador e informações da fase."""
        """Desenha todas as entidades com offset da câmera."""
        self.tela.fill((100, 100, 150))   # céu azul claro
        for ent in entidades:
            pos = ent.obter_componente("posicao")
            if not pos:
                continue
            # Aplica offset da câmera
            x_tela = pos.x - camera.x
            y_tela = pos.y - camera.y
            # Desenha retângulo colorido (verde para plataformas, vermelho para jogador)
            cor = (255, 0, 0) if hasattr(ent, 'obter_componente') and ent.obter_componente("fisica") else (0, 255, 0)
            pygame.draw.rect(self.tela, cor, (x_tela, y_tela, pos.largura, pos.altura))
        pygame.display.flip()

    def desenhar_pause(self, fase_atual=1):
        """Tela de pausa – sobreposta ao jogo (mas aqui desenhamos separadamente)."""
        self.tela.fill((0, 0, 0, 128))                   # preenchimento escuro
        # Para um efeito de semi-transparência seria necessário usar surface com alpha,
        # mas para simplificar, preenchemos com preto sólido.
        self.tela.fill((0, 0, 0))
        self.desenhar_texto("JOGO PAUSADO", None, 200, (255, 255, 0))
        self.desenhar_texto("Pressione P para continuar", None, 280)
        self.desenhar_texto(f"Fase atual: {fase_atual}", None, 350)
        self.desenhar_texto("ESC para sair do jogo", None, 420)
        pygame.display.flip()

    def tick(self, fps=60):
        self.relogio.tick(fps)

    def fechar(self):
        pygame.quit()