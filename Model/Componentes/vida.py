#Saúde e dano

class ComponenteVida:
    def __init__(self, hp, dano=1):
        self.hp = hp
        self.hp_max = hp
        self.dano = dano
        self.invencivel = False  # para o flash de dano