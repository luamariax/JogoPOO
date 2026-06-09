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

        # --- Cores ---
        self.COR_TITULO        = (245, 232, 192)   # dourado claro
        self.COR_SUBTITULO     = (184, 216, 154)   # verde claro
        self.COR_BTN_PRINCIPAL = (80,  150,  50)
        self.COR_BTN_HOVER_P   = (100, 180,  60)
        self.COR_BTN_SECUNDARIO= (20,   50,  15)
        self.COR_BTN_HOVER_S   = (40,   80,  20)
        self.COR_BTN_BORDA_P   = (168, 212, 112)
        self.COR_BTN_BORDA_S   = (106, 154,  64)
        self.COR_BTN_TEXTO_P   = (240, 248, 232)
        self.COR_BTN_TEXTO_S   = (200, 232, 160)
        self.COR_DIVISOR       = (168, 212, 112)
        self.COR_FUNDO_TITULO  = (10,  40,  10)       # verde escuro p/ fundo do título pause

        # --- Fontes ---
        pygame.font.init()
        self.fonte_titulo   = pygame.font.SysFont("serif", 72, bold=True)
        self.fonte_subtitulo= pygame.font.SysFont("serif", 22, bold=False)
        self.fonte_botao    = pygame.font.SysFont("serif", 28, bold=True)

        # --- Background ---
        caminho_bg = os.path.join(os.path.dirname(__file__), "Assets/background_tela_pause_floresta_a_noite.jpg")
        if os.path.exists(caminho_bg):
            bg_raw = pygame.image.load(caminho_bg).convert()
            self.background = pygame.transform.scale(bg_raw, (self.largura, self.altura))
        else:
            self.background = None  # fallback para gradiente

        # --- Estado ---
        # "menu" | "jogando" | "pause"
        self.estado = "menu"

        # --- Botões (rect calculado em _calcular_layout) ---
        self.btn_continuar  = pygame.Rect(0, 0, 260, 56)
        self.btn_novo_jogo  = pygame.Rect(0, 0, 260, 56)
        self._calcular_layout()

    # ------------------------------------------------------------------ #
    def _calcular_layout(self):
        """Centraliza os botões na tela."""
        cx = self.largura  // 2
        cy = self.altura   // 2

        # Continuar fica 30 px acima do centro, Novo Jogo 30 px abaixo
        self.btn_continuar.centerx = cx
        self.btn_continuar.centery = cy + 20

        self.btn_novo_jogo.centerx  = cx
        self.btn_novo_jogo.centery  = cy + 90

    # ------------------------------------------------------------------ #
    def _desenhar_fundo(self):
        if self.background:
            self.janela.blit(self.background, (0, 0))
        else:
            # Gradiente verde simples como fallback
            for y in range(self.altura):
                t = y / self.altura
                r = int(20  + t * 30)
                g = int(80  + t * 60)
                b = int(15  + t * 20)
                pygame.draw.line(self.janela, (r, g, b), (0, y), (self.largura, y))

        # Overlay escuro gradiente (de cima transparente → baixo semi-opaco)
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        for y in range(self.altura):
            alpha = int(40 + (y / self.altura) * 140)
            pygame.draw.line(overlay, (5, 20, 5, alpha), (0, y), (self.largura, y))
        self.janela.blit(overlay, (0, 0))

    # ------------------------------------------------------------------ #
    def _desenhar_botao(self, rect, texto, hover, cor_base, cor_hover, cor_borda, cor_texto):
        cor_fundo = cor_hover if hover else cor_base
        alpha = 210 if hover else 180

        surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        surf.fill((*cor_fundo, alpha))
        self.janela.blit(surf, rect.topleft)

        borda_alpha = 255 if hover else 200
        borda_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(borda_surf, (*cor_borda, borda_alpha),
                         borda_surf.get_rect(), 2, border_radius=4)
        self.janela.blit(borda_surf, rect.topleft)

        label = self.fonte_botao.render(texto, True, cor_texto)
        lx = rect.centerx - label.get_width()  // 2
        ly = rect.centery - label.get_height() // 2
        self.janela.blit(label, (lx, ly))

    # ------------------------------------------------------------------ #
    def _desenhar_menu(self, mouse_pos):
        self._desenhar_fundo()

        cx = self.largura // 2

        # --- Título ---
        titulo1 = self.fonte_titulo.render("Floresta", True, self.COR_TITULO)
        titulo2 = self.fonte_titulo.render("Ancestral", True, self.COR_TITULO)

        base_y = self.altura // 2 - 220
        self.janela.blit(titulo1, (cx - titulo1.get_width() // 2, base_y))
        self.janela.blit(titulo2, (cx - titulo2.get_width() // 2, base_y + 80))

        # --- Subtítulo ---
        sub = self.fonte_subtitulo.render("✦  A  J O R N A D A  ✦", True, self.COR_SUBTITULO)
        self.janela.blit(sub, (cx - sub.get_width() // 2, base_y + 160))

        # --- Divisor ---
        div_w = 120
        div_y  = base_y + 196
        pygame.draw.line(self.janela, self.COR_DIVISOR,
                         (cx - div_w, div_y), (cx + div_w, div_y), 2)

        # --- Botões ---
        h_cont = self.btn_continuar.collidepoint(mouse_pos)
        h_novo = self.btn_novo_jogo.collidepoint(mouse_pos)

        self._desenhar_botao(
            self.btn_continuar, "▶  Continuar", h_cont,
            self.COR_BTN_PRINCIPAL, self.COR_BTN_HOVER_P,
            self.COR_BTN_BORDA_P,   self.COR_BTN_TEXTO_P,
        )
        self._desenhar_botao(
            self.btn_novo_jogo, "✦  Novo Jogo", h_novo,
            self.COR_BTN_SECUNDARIO, self.COR_BTN_HOVER_S,
            self.COR_BTN_BORDA_S,    self.COR_BTN_TEXTO_S,
        )

        pygame.display.flip()

    # ------------------------------------------------------------------ #
    def _desenhar_pause(self, mouse_pos):
        self._desenhar_fundo()

        # Overlay extra escurecido para destacar o pause sobre o jogo
        escuro = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        escuro.fill((0, 0, 0, 120))
        self.janela.blit(escuro, (0, 0))

        cx = self.largura // 2

        # --- Título ---
        titulo1 = self.fonte_titulo.render("PAUSE", True, self.COR_TITULO, self.COR_FUNDO_TITULO)

        base_y = self.altura // 2 - 220
        self.janela.blit(titulo1, (cx - titulo1.get_width() // 2, base_y))

        # --- Divisor ---
        div_w = 120
        div_y  = base_y + 196
        pygame.draw.line(self.janela, self.COR_DIVISOR,
                         (cx - div_w, div_y), (cx + div_w, div_y), 2)

        # --- Botões ---
        h_cont = self.btn_continuar.collidepoint(mouse_pos)
        h_novo = self.btn_novo_jogo.collidepoint(mouse_pos)

        self._desenhar_botao(
            self.btn_continuar, "▶  Continuar", h_cont,
            self.COR_BTN_PRINCIPAL, self.COR_BTN_HOVER_P,
            self.COR_BTN_BORDA_P,   self.COR_BTN_TEXTO_P,
        )
        self._desenhar_botao(
            self.btn_novo_jogo, "✦  Voltar Menu Principal", h_novo,
            self.COR_BTN_SECUNDARIO, self.COR_BTN_HOVER_S,
            self.COR_BTN_BORDA_S,    self.COR_BTN_TEXTO_S,
        )

        pygame.display.flip()

    # ------------------------------------------------------------------ #
    def loop_pause(self):
        """Loop da tela de pausa. Retorna 'continuar' ou 'menu'."""
        self.estado = "pause"
        # Alarga o botão "Voltar Menu Principal" que tem texto maior
        self.btn_novo_jogo.width = 320
        self._calcular_layout()

        while True:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    # ESC ou P fecham o pause e voltam ao jogo
                    if evento.key in (pygame.K_ESCAPE, pygame.K_p):
                        self.estado = "jogando"
                        self.btn_novo_jogo.width = 260  # restaura largura original
                        self._calcular_layout()
                        return "continuar"

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.btn_continuar.collidepoint(mouse_pos):
                        self.estado = "jogando"
                        self.btn_novo_jogo.width = 260
                        self._calcular_layout()
                        return "continuar"
                    if self.btn_novo_jogo.collidepoint(mouse_pos):
                        self.estado = "menu"
                        self.btn_novo_jogo.width = 260
                        self._calcular_layout()
                        return "menu"

            self._desenhar_pause(mouse_pos)

    # ------------------------------------------------------------------ #
    def desenhar(self, entidades, offset=(0, 0)):
        """
        Recebe o offset da câmera antes de desenhar qualquer coisa.
        Lê ComponentePosicao + ComponenteSprite → desenha na tela.
        """
        if self.estado == "menu":
            return  # menu cuida do próprio render

        self.janela.fill((30, 30, 30))
        for entidade in entidades:
            pos    = entidade.get("ComponentePosicao")
            sprite = entidade.get("ComponenteSprite")
            if pos and sprite:
                x = pos["x"] - offset[0]
                y = pos["y"] - offset[1]
                self.janela.blit(sprite["imagem"], (x, y))

        pygame.display.flip()

    # ------------------------------------------------------------------ #
    def loop_menu(self):
        """Loop exclusivo da tela de entrada. Retorna 'continuar' ou 'novo_jogo'."""
        while True:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.btn_continuar.collidepoint(mouse_pos):
                        self.estado = "jogando"
                        return "continuar"
                    if self.btn_novo_jogo.collidepoint(mouse_pos):
                        self.estado = "jogando"
                        return "novo_jogo"

            self._desenhar_menu(mouse_pos)


# ------------------------------------------------------------------ #
# Ponto de entrada para teste isolado
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    tela = TelaJogo()

    # 1) Testa o menu de entrada
    escolha = tela.loop_menu()
    print(f"[MENU] Jogador escolheu: {escolha}")

    # 2) Simula alguns frames de jogo e então abre o pause automaticamente
    print("[JOGO] Rodando por 2 segundos... pressione P ou ESC para pausar.")
    rodando = True
    pausado = False
    tempo_inicio = pygame.time.get_ticks()

    while rodando:
        tela.clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                rodando = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    rodando = False
                if ev.key == pygame.K_p:
                    resultado = tela.loop_pause()
                    print(f"[PAUSE] Jogador escolheu: {resultado}")
                    if resultado == "menu":
                        rodando = False  # voltaria ao menu no jogo real

        # Abre o pause automaticamente após 2 s (só uma vez) para facilitar o teste
        if not pausado and pygame.time.get_ticks() - tempo_inicio >= 2000:
            pausado = True
            print("[TESTE] Abrindo pause automaticamente...")
            resultado = tela.loop_pause()
            print(f"[PAUSE] Jogador escolheu: {resultado}")
            if resultado == "menu":
                rodando = False

        tela.desenhar(entidades=[], offset=(0, 0))

    pygame.quit()
    sys.exit()