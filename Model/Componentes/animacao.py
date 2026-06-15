

class ComponenteAnimacao:
    """
    Armazena as sequências de frames e controla qual está ativa.
    Apenas dados — quem avança o frame é o SistemaAnimacao.
    """
    def __init__(self, animacoes: dict, velocidade: int = 8):
        # animacoes = {"andar_direita": ["chave_0", "chave_1"], "andar_esquerda": [...]}
        self.animacoes = animacoes
        self.velocidade = velocidade      # frames de jogo entre cada troca de sprite
        self.estado_atual = "andar_direita"
        self.frame_atual = 0
        self.contador = 0                 # conta frames até trocar o sprite