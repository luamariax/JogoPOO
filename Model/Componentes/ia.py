#Qual comportamento o SistemaIA vai executar

class ComponenteIA:
    def __init__(self, tipo: str, velocidade: float = 2):
        self.tipo = tipo        # "patrulhar", "voar", "pular", "combinar"
        self.velocidade = velocidade
        self.direcao = 1        # 1 = direita, -1 = esquerda
        self.raio_deteccao = 200
        self.alvo = None        # referência ao jogador quando detectado
        self.estado = "vivo"
        self.golpes = 0
        self.timer_pulo = 60