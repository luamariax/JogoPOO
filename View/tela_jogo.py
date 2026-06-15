import pygame
import sys
import os


class TelaJogo:
    def __init__(self):
        pygame.init()

        self.largura = 900
        self.altura = 600

        self.janela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("JOGOPOO")

        self.clock = pygame.time.Clock()

        self.estado = "menu"
        self.fase = 1

        self.background = self.carregar_background()

        self.fonte_titulo = pygame.font.SysFont("serif", 64, bold=True)
        self.fonte_texto = pygame.font.SysFont("serif", 28, bold=True)
        self.fonte_pequena = pygame.font.SysFont("serif", 22)

        self.btn_continuar = pygame.Rect(320, 330, 260, 55)
        self.btn_novo_jogo = pygame.Rect(320, 400, 260, 55)

    def carregar_background(self):
        caminho = os.path.join(
            os.path.dirname(__file__),
            "..",
            "Assets",
            "background_pampulha1.jpg"
        )

        caminho = os.path.abspath(caminho)

        if os.path.exists(caminho):
            img = pygame.image.load(caminho).convert()
            return pygame.transform.scale(img, (self.largura, self.altura))

        return None

    def desenhar_fundo(self, cor):
        if self.background:
            self.janela.blit(self.background, (0, 0))
        else:
            self.janela.fill(cor)

    def desenhar_botao(self, rect, texto):
        mouse = pygame.mouse.get_pos()

        if rect.collidepoint(mouse):
            cor = (100, 180, 60)
        else:
            cor = (70, 140, 50)

        pygame.draw.rect(self.janela, cor, rect, border_radius=6)
        pygame.draw.rect(self.janela, (220, 240, 180), rect, 2, border_radius=6)

        label = self.fonte_texto.render(texto, True, (255, 255, 255))
        x = rect.centerx - label.get_width() // 2
        y = rect.centery - label.get_height() // 2
        self.janela.blit(label, (x, y))

    def desenhar_menu(self):
        self.desenhar_fundo((30, 120, 40))

        titulo1 = self.fonte_titulo.render("Floresta", True, (245, 232, 192))
        titulo2 = self.fonte_titulo.render("Ancestral", True, (245, 232, 192))

        self.janela.blit(titulo1, (self.largura // 2 - titulo1.get_width() // 2, 120))
        self.janela.blit(titulo2, (self.largura // 2 - titulo2.get_width() // 2, 190))

        subtitulo = self.fonte_pequena = pygame.font.SysFont("Times New Roman", 26, bold=True)(
            "A JORNADA DA CAPIVARA",
            True,
            (184, 216, 154)
        )

        self.janela.blit(
            subtitulo,
            (self.largura // 2 - subtitulo.get_width() // 2, 275)
        )

        self.desenhar_botao(self.btn_continuar, "Continuar")
        self.desenhar_botao(self.btn_novo_jogo, "Novo Jogo")

        pygame.display.flip()

    def processar_menu(self, evento):
        if self.estado != "menu":
            return

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse = pygame.mouse.get_pos()

            if self.btn_continuar.collidepoint(mouse):
                self.estado = "jogando"

            if self.btn_novo_jogo.collidepoint(mouse):
                self.estado = "jogando"
                self.fase = 1

    def desenhar_jogador(self, jogador):
        pos = jogador.obter("posicao")

        if pos:
            pygame.draw.rect(
                self.janela,
                (255, 220, 0),
                (pos.x, pos.y, pos.largura, pos.altura)
            )

    def desenhar_fase1(self, jogador):
        self.desenhar_fundo((70, 160, 70))

        texto = self.fonte_pequena.render(
            "FASE 1 - Movimento simples",
            True,
            (255, 255, 255)
        )
        self.janela.blit(texto, (20, 20))

        self.desenhar_jogador(jogador)

    def desenhar_fase2(self, jogador):
        self.desenhar_fundo((50, 120, 170))

        texto = self.fonte_pequena.render(
            "FASE 2 - Plataformas e pulo",
            True,
            (255, 255, 255)
        )
        self.janela.blit(texto, (20, 20))

        pygame.draw.rect(self.janela, (100, 70, 40), (0, 520, 900, 80))
        pygame.draw.rect(self.janela, (100, 70, 40), (250, 400, 180, 25))
        pygame.draw.rect(self.janela, (100, 70, 40), (550, 320, 180, 25))

        self.desenhar_jogador(jogador)

    def desenhar_fase3(self, jogador):
        self.desenhar_fundo((80, 40, 40))

        texto = self.fonte_pequena.render(
            "FASE 3 - Inimigos e desafio final",
            True,
            (255, 255, 255)
        )
        self.janela.blit(texto, (20, 20))

        pygame.draw.rect(self.janela, (100, 70, 40), (0, 520, 900, 80))

        pygame.draw.rect(self.janela, (200, 0, 0), (500, 470, 50, 50))
        pygame.draw.rect(self.janela, (200, 0, 0), (700, 470, 50, 50))

        self.desenhar_jogador(jogador)

    def desenhar_game_over(self):
        self.janela.fill((20, 20, 20))

        texto = self.fonte_titulo.render("GAME OVER", True, (220, 40, 40))
        self.janela.blit(
            texto,
            (self.largura // 2 - texto.get_width() // 2, 240)
        )

        pygame.display.flip()

    def desenhar(self, jogador):
        if self.estado == "menu":
            self.desenhar_menu()
            return

        if self.estado == "game_over":
            self.desenhar_game_over()
            return

        if self.fase == 1:
            self.desenhar_fase1(jogador)

        elif self.fase == 2:
            self.desenhar_fase2(jogador)

        elif self.fase == 3:
            self.desenhar_fase3(jogador)

        pygame.display.flip()

    def tick(self, fps):
        self.clock.tick(fps)

    def fechar(self):
        pygame.quit()
        sys.exit()
