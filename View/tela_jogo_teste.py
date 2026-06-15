# view/tela_jogo.py
import pygame
from Model.gerenciador_recursos import GerenciadorRecursos

COR_FUNDO    = (30, 30, 60)   # azul escuro — céu noturno
COR_MENU     = (20, 20, 40)
COR_TEXTO    = (255, 255, 255)
COR_PAUSE    = (0, 0, 0, 150) # semi-transparente


class TelaJogoTeste:
    """Inicializa pygame e desenha o estado atual do jogo."""

    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.largura = info.current_w
        self.altura = info.current_h
        self.superficie = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("JOGO_APPOO")
        self.clock = pygame.time.Clock()
        self.fonte_grande = pygame.font.SysFont("Arial", 48, bold=True)
        self.fonte_media  = pygame.font.SysFont("Arial", 28)
        self.fonte_pequena = pygame.font.SysFont("Arial", 18)

    # ------------------------------------------------------------------
    # Desenho por estado
    # ------------------------------------------------------------------

    def desenhar_menu(self):
        self.superficie.fill(COR_MENU)
        self._texto_centralizado("JogoPOO",       self.fonte_grande, COR_TEXTO, self.altura // 3)
        self._texto_centralizado("ENTER — Jogar", self.fonte_media,  COR_TEXTO, self.altura // 2)
        self._texto_centralizado("ESC   — Sair",  self.fonte_media,  COR_TEXTO, self.altura // 2 + 40)
        pygame.display.flip()

    def desenhar_jogo(self, entidades: list, camera, hud: dict | None = None):
        self.superficie.fill(COR_FUNDO)
        offset_x = camera.x if camera else 0

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
        pygame.quit()