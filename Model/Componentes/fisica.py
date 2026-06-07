#Como ela se move, responsável por guardar os dados
#O Voador recebe gravidade=False. O Saltador recebe gravidade=True. Mesma classe, comportamento diferente.

class ComponenteFisica:
    def __init__(self, velocidade=0, gravidade=True):
        self.vel_x = 0
        self.vel_y = 0
        self.velocidade = velocidade
        self.gravidade = gravidade
        self.no_chao = False