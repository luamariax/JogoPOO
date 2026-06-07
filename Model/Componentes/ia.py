#Qual comportamento o SistemaIA vai executar

class ComponenteIA:
    def __init__(self, tipo):
        self.tipo = tipo        # "patrulhar", "voar", "pular", "combinar"
        self.direcao = 1        # 1 = direita, -1 = esquerda
        self.raio_deteccao = 200
        self.alvo = None        # referência ao jogador quando detectado