# Separa dados visuais da posição
#Sem ele, a TelaJogo não sabe o que desenhar, só onde.

class ComponenteSprite:
    def __init__(self, imagem: str, animacao: str = None):
        self.imagem = imagem
        self.animacao = animacao
        self.flip_x = False     # virar o sprite conforme direção
        self.visivel = True