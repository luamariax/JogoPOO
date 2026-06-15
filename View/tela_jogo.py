import pygame
import sys
import os


class TelaJogo:
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.largura = info.current_w
        self.altura = info.current_h

        self.janela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("JOGOPOO")

        self.clock = pygame.time.Clock()

        self.estado = "menu"

        self.background = self.carregar_background()

        self.COR_TITULO = (245, 232, 192)
        self.COR_SUBTITULO = (184, 216, 154)
        self.COR_BTN_PRINCIPAL = (80, 150, 50)
        self.COR_BTN_HOVER_P = (100, 180, 60)
        self.COR_BTN_SECUNDARIO = (20, 50, 15)
        self.COR_BTN_HOVER_S = (40, 80, 20)
        self.COR_BTN_BORDA_P = (168, 212, 112)
        self.COR_BTN_BORDA_S = (106, 154, 64)
        self.COR_BTN_TEXTO_P = (240, 248, 232)
        self.COR_BTN_TEXTO_S = (200, 232, 160)

        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont("serif", 72, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("serif", 22)
        self.fonte_botao = pygame.font.SysFont("serif", 28, bold=True)

        self.btn_continuar = pygame.Rect(0, 0, 260, 56)
        self.btn_novo_jogo = pygame.Rect(0, 0, 260, 56)

        self._calcular_layout()

    def carregar_background(self):
        caminho_bg = os.path.join(
            os.path.dirname(__file__),
            "..",
            "Assets",
            "background_pampulha1.jpg"
        )

        caminho_bg = os.path.abspath(caminho_bg)

        if os.path.exists(caminho_bg):
            imagem = pygame.image.load(caminho_bg).convert()
            return pygame.transform.scale(imagem, (self.largura, self.altura))

        return None

    def _calcular_layout(self):
        cx = self.largura // 2
        cy = self.altura // 2

        self.btn_continuar.centerx = cx
        self.btn_continuar.centery = cy + 20

        self.btn_novo_jogo.centerx = cx
        self.btn_novo_jogo.centery = cy + 90

    def _desenhar_fundo(self):
        if self.background:
            self.janela.blit(self.background, (0, 0))
        else:
            self.janela.fill((30, 120, 40))

        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 90))
        self.janela.blit(overlay, (0, 0))

    def _desenhar_botao(
        self,
        rect,
        texto,
        hover,
        cor_base,
        cor_hover,
        cor_borda,
        cor_texto
    ):
        cor_fundo = cor_hover if hover else cor_base

        pygame.draw.rect(self.janela, cor_fundo, rect, border_radius=6)
        pygame.draw.rect(self.janela, cor_borda, rect, 2, border_radius=6)

        label = self.fonte_botao.render(texto, True, cor_texto)
        x = rect.centerx - label.get_width() // 2
        y = rect.centery - label.get_height() // 2
        self.janela.blit(label, (x, y))

    def desenhar_menu(self):
        mouse_pos = pygame.mouse.get_pos()

        self._desenhar_fundo()

        cx = self.largura // 2
        base_y = self.altura // 2 - 220

        titulo1 = self.fonte_titulo.render("Floresta", True, self.COR_TITULO)
        titulo2 = self.fonte_titulo.render("Ancestral", True, self.COR_TITULO)

        self.janela.blit(titulo1, (cx - titulo1.get_width() // 2, base_y))
        self.janela.blit(titulo2, (cx - titulo2.get_width() // 2, base_y + 80))

        subtitulo = self.fonte_subtitulo.render(
            "✦  A  J O R N A D A  D A  C A P I V A R A ✦",
            True,
            self.COR_SUBTITULO
        )
        self.janela.blit(
            subtitulo,
            (cx - subtitulo.get_width() // 2, base_y + 160)
        )

        pygame.draw.line(
            self.janela,
            self.COR_BTN_BORDA_P,
            (cx - 120, base_y + 196),
            (cx + 120, base_y + 196),
            2
        )

        hover_continuar = self.btn_continuar.collidepoint(mouse_pos)
        hover_novo = self.btn_novo_jogo.collidepoint(mouse_pos)

        self._desenhar_botao(
            self.btn_continuar,
            "▶ Continuar",
            hover_continuar,
            self.COR_BTN_PRINCIPAL,
            self.COR_BTN_HOVER_P,
            self.COR_BTN_BORDA_P,
            self.COR_BTN_TEXTO_P
        )

        self._desenhar_botao(
            self.btn_novo_jogo,
            "✦ Novo Jogo",
            hover_novo,
            self.COR_BTN_SECUNDARIO,
            self.COR_BTN_HOVER_S,
            self.COR_BTN_BORDA_S,
            self.COR_BTN_TEXTO_S
        )

        pygame.display.flip()

    def processar_menu(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if self.btn_continuar.collidepoint(mouse_pos):
                self.estado = "jogando"

            if self.btn_novo_jogo.collidepoint(mouse_pos):
                self.estado = "jogando"

    def desenhar(self, jogador):
        if self.estado == "menu":
            self.desenhar_menu()
            return

        if self.background:
            self.janela.blit(self.background, (0, 0))
        else:
            self.janela.fill((30, 120, 40))

        pos = jogador.obter("posicao")

        if pos:
            pygame.draw.rect(
                self.janela,
                (255, 200, 0),
                (pos.x, pos.y, pos.largura, pos.altura)
            )

        pygame.display.flip()

    def tick(self, fps):
        self.clock.tick(fps)

    def fechar(self):
        pygame.quit()
        sys.exit()