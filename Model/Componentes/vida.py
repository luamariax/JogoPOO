#Saúde e dano

class ComponenteVida:
    def __init__(self, hp: int, dano: int = 1):
        self.hp = hp
        self.hp_max = hp
        self.dano = dano
        self.invencivel = False  # para o flash de dano
        self.timer_invencivel = 0