# Separa dados visuais da posição
#Sem ele, a TelaJogo não sabe o que desenhar, só onde.
# model/componentes/sprite.py
import pygame

class ComponenteSprite:
    """
    Armazena a imagem de uma entidade para ser desenhada pela TelaJogo.
    Apenas dados — quem desenha é a View, quem troca frames é o SistemaAnimacao.
    """
    def __init__(self, chave_imagem: str, flip_x: bool = False, visivel: bool = True):
        self.chave_imagem = chave_imagem  # chave no GerenciadorRecursos, ex: "jogador_idle"
        self.imagem: pygame.Surface | None = None  # preenchido pelo GerenciadorRecursos
        self.flip_x = flip_x      # espelha horizontalmente (jogador olhando para esquerda)
        self.visivel = visivel    # False = entidade existe mas não é desenhada