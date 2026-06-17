# view/tela_jogo.py
import pygame
from Model.gerenciador_recursos import GerenciadorRecursos
import sys
import os

COR_FUNDO    = (135, 206, 235)   # azul escuro — céu noturno
COR_MENU     = (20, 20, 40)
COR_TEXTO    = (255, 255, 255)
COR_PAUSE    = (0, 0, 0, 150) # semi-transparente


class TelaJogoTeste:
    """Inicializa pygame e desenha o estado atual do jogo."""

    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.largura = info.current_w
        self.altura = info.current_h - 80
        self.superficie = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("JOGO_APPOO")
        self.clock = pygame.time.Clock()
        #escrita
        self.fonte_grande = pygame.font.SysFont("serif", 64, bold=True)
        self.fonte_media  = pygame.font.SysFont("serif", 28, bold=True)
        self.fonte_pequena = pygame.font.SysFont("serif", 22)
        #imagem de fundo
        self.background = self.carregar_background()
        self.background_dia = self.carregar_background_dia()
        #tamanho botões
        posicao_x_botao = self.largura // 2 -130
        posicao_y_botao = self.altura // 2 
        self.btn_continuar = pygame.Rect(posicao_x_botao, posicao_y_botao, 260, 55)
        self.btn_novo_jogo = pygame.Rect(posicao_x_botao, posicao_y_botao+60, 260, 55)


    # ------------------------------------------------------------------
    # Utitlidades para criar o fundo e desenhar os botões
    # ------------------------------------------------------------------
    def carregar_background(self):
        caminho = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "Assets", "background_pampulha1.jpg"
        ))

        if os.path.exists(caminho):
            img = pygame.image.load(caminho).convert()
            return pygame.transform.scale(img, (self.largura, self.altura))

        return None
    
    def carregar_background_dia(self):
        caminho = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "Assets", "fundodia.png"
        ))
        if os.path.exists(caminho):
            img = pygame.image.load(caminho).convert()
            proporcao = img.get_width() / img.get_height()
            nova_largura = int(self.altura * proporcao)
            return pygame.transform.scale(img, (nova_largura, self.altura))
        return None

    def desenhar_fundo(self, cor, offset_x=None):
        if offset_x is not None and self.background_dia:
            larg = self.background_dia.get_width()
            inicio = -(offset_x % larg)
            x = inicio
            while x < self.largura:
                self.superficie.blit(self.background_dia, (x, 0))
                x += larg
        elif self.background:
            self.superficie.blit(self.background, (0, 0))
        else:
            self.superficie.fill(cor)


    def desenhar_botao(self, rect, texto):
        mouse = pygame.mouse.get_pos()

        if rect.collidepoint(mouse):
            cor = (100, 180, 60)
        else:
            cor = (70, 140, 50)

        pygame.draw.rect(self.superficie, cor, rect, border_radius=6)
        pygame.draw.rect(self.superficie, (220, 240, 180), rect, 2, border_radius=6)

        label = self.fonte_media.render(texto, True, (255, 255, 255))
        x = rect.centerx - label.get_width() // 2
        y = rect.centery - label.get_height() // 2
        self.superficie.blit(label, (x, y))


    # ------------------------------------------------------------------
    # Desenho por estado
    # ------------------------------------------------------------------

    def desenhar_menu(self):
        self.desenhar_fundo((30, 120, 40))

        titulo1 = self.fonte_grande.render("Floresta", True, (245, 232, 192))
        titulo2 = self.fonte_grande.render("Ancestral", True, (245, 232, 192))

        self.superficie.blit(titulo1, (self.largura // 2 - titulo1.get_width() // 2, 120))
        self.superficie.blit(titulo2, (self.largura // 2 - titulo2.get_width() // 2, 190))

        fonte_sub = pygame.font.SysFont("Times New Roman", 26, bold=True)
        subtitulo = fonte_sub.render("A JORNADA DA CAPIVARA", True, (184, 216, 154))

        self.superficie.blit(
            subtitulo,
            (self.largura // 2 - subtitulo.get_width() // 2, 275)
        )

        self.desenhar_botao(self.btn_continuar, "Continuar")
        self.desenhar_botao(self.btn_novo_jogo, "Novo Jogo")

        pygame.display.flip()

    def desenhar_jogo(self, entidades: list, camera, hud: dict | None = None):
        offset_x = camera.x if camera else 0
        self.desenhar_fundo(COR_FUNDO, offset_x)

        for entidade in entidades:
            self._desenhar_entidade(entidade, offset_x)

        if hud:
            self._desenhar_hud(hud)

        pygame.display.flip()

    def desenhar_pause(self, fase_atual: int = 1):
        # Overlay semi-transparente sobre o frame atual
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.superficie.blit(overlay, (0, 0))

        self._texto_centralizado("PAUSADO",          self.fonte_grande, COR_TEXTO, self.altura // 3)
        self._texto_centralizado(f"Fase {fase_atual}", self.fonte_media, COR_TEXTO, self.altura // 2)
        self._texto_centralizado("P — Continuar",    self.fonte_media,  COR_TEXTO, self.altura // 2 + 40)
        self._texto_centralizado("ESC — Sair",       self.fonte_media,  COR_TEXTO, self.altura // 2 + 80)
        pygame.display.flip()

    def desenhar_game_over(self, pontuacao: int = 0):
        self.superficie.fill(COR_MENU)
        self._texto_centralizado("GAME OVER",           self.fonte_grande, (220, 50, 50),  self.altura // 3)
        self._texto_centralizado(f"Pontos: {pontuacao}", self.fonte_media,  COR_TEXTO,      self.altura // 2)
        self._texto_centralizado("ENTER — Tentar novamente", self.fonte_media, COR_TEXTO,  self.altura // 2 + 50)
        self._texto_centralizado("ESC   — Sair",        self.fonte_media,  COR_TEXTO,      self.altura // 2 + 90)
        pygame.display.flip()

    # ------------------------------------------------------------------
    # Entidade
    # ------------------------------------------------------------------

    def _desenhar_entidade(self, entidade, offset_x: int):
        pos    = entidade.obter_componente("posicao")
        sprite = entidade.obter_componente("sprite")

        if not pos:
            return

        # Com sprite
        if sprite and sprite.visivel and sprite.imagem:
            imagem = pygame.transform.flip(sprite.imagem, True, False) \
                    if sprite.flip_x else sprite.imagem
            vida = entidade.obter_componente("vida")
            if vida and vida.invencivel and (pygame.time.get_ticks() // 80) % 2 == 0:
                imagem = imagem.copy()
                imagem.fill((200, 0, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
            self.superficie.blit(imagem, (pos.x - offset_x, pos.y))
            return


        # Fallback — retângulo colorido (sem sprite ou sprite não carregado)
        col = entidade.obter_componente("colisao")
        cor = self._cor_fallback(col)
        pygame.draw.rect(self.superficie, cor,
                         (pos.x - offset_x, pos.y, pos.largura, pos.altura))

    def _cor_fallback(self, col) -> tuple:
        """Cor do retângulo de fallback com base no tipo de colisão."""
        if not col:
            return (200, 200, 200)
        return {
            "normal":   (100, 180, 100),  # verde — plataforma
            "dano":     (220,  60,  60),  # vermelho — inimigo
            "gatilho":  (255, 220,   0),  # amarelo — item
        }.get(col.tipo, (200, 200, 200))

    # ------------------------------------------------------------------
    # HUD
    # ------------------------------------------------------------------

    def _desenhar_hud(self, hud: dict):
        """
        hud esperado:
        {
            "vidas": 3,
            "moedas": 7,
            "fase": 1
        }
        """
        padding = 10
        self._texto(f"♥ {hud.get('vidas', 0)}",  self.fonte_media, (220, 60, 60),  (padding, padding))
        self._texto(f"● {hud.get('moedas', 0)}", self.fonte_media, (255, 220, 0),  (padding, padding + 35))
        fase_txt = self.fonte_pequena.render(f"Fase {hud.get('fase', 1)}", True, COR_TEXTO)
        self.superficie.blit(fase_txt, (self.largura - fase_txt.get_width() - padding, padding))

    # ------------------------------------------------------------------
    # Utilitários de texto
    # ------------------------------------------------------------------

    def _texto_centralizado(self, texto: str, fonte, cor: tuple, y: int):
        surface = fonte.render(texto, True, cor)
        x = (self.largura - surface.get_width()) // 2
        self.superficie.blit(surface, (x, y))

    def _texto(self, texto: str, fonte, cor: tuple, pos: tuple):
        surface = fonte.render(texto, True, cor)
        self.superficie.blit(surface, pos)

    # ------------------------------------------------------------------
    # Controle do loop
    # ------------------------------------------------------------------

    def tick(self, fps: int = 60):
        self.clock.tick(fps)

    def fechar(self):
        sys.exit()
        pygame.quit()