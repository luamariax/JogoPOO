#Como ela se move, responsável por guardar os dados
#O Voador recebe gravidade=False. O Saltador recebe gravidade=True. Mesma classe, comportamento diferente.


class ComponenteFisica:
    """
    Armazena dados de movimento: velocidade, se sofre gravidade,
    se está no chão, etc. Nenhuma lógica de atualização está aqui.
    """
    def __init__(self, vel_x: float = 0, vel_y: float = 0,
                 gravidade: bool = False, no_chao: bool = True):
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.gravidade = gravidade   # se True, o sistema de física aplica aceleração
        self.no_chao = no_chao       # usado para permitir pulo, etc.