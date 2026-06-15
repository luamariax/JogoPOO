# model/gerenciador_recursos.py
import pygame
import os

CAMINHO_SPRITES = "Assets/sprites"

class GerenciadorRecursos:
    """
    Carrega imagens uma única vez e distribui para os ComponenteSprite.
    Evita abrir o mesmo arquivo várias vezes por frame.
    """
    _cache: dict[str, pygame.Surface] = {}  # compartilhado entre todas as instâncias

    @classmethod
    def carregar(cls, chave: str, nome_arquivo: str, tamanho: tuple | None = None) -> pygame.Surface:
        """
        Carrega uma imagem e armazena no cache.
        Se já foi carregada antes, retorna do cache sem abrir o arquivo.
        
        tamanho: (largura, altura) para redimensionar. None mantém o original.
        """
        if chave in cls._cache:
            return cls._cache[chave]

        caminho = os.path.join(CAMINHO_SPRITES, nome_arquivo)
        try:
            imagem = pygame.image.load(caminho).convert_alpha()
        except FileNotFoundError:
            # Fallback: quadrado colorido para não crashar sem o asset
            print(f"[GerenciadorRecursos] Imagem não encontrada: {caminho}")
            imagem = cls._criar_placeholder()

        if tamanho:
            imagem = pygame.transform.scale(imagem, tamanho)

        cls._cache[chave] = imagem
        return imagem

    @classmethod
    def obter(cls, chave: str) -> pygame.Surface | None:
        """Retorna imagem já carregada. None se não existir no cache."""
        return cls._cache.get(chave)

    @classmethod
    def aplicar_sprites(cls, entidades: list):
        """
        Percorre entidades e preenche ComponenteSprite.imagem com a Surface correta.
        Chamado uma vez ao carregar a fase.
        """
        for entidade in entidades:
            sprite = entidade.obter_componente("sprite")
            if sprite and sprite.chave_imagem:
                sprite.imagem = cls.obter(sprite.chave_imagem)

    @classmethod
    def _criar_placeholder(cls) -> pygame.Surface:
        """Surface rosa choque para sinalizar asset faltando."""
        surface = pygame.Surface((32, 32))
        surface.fill((255, 0, 255))
        return surface