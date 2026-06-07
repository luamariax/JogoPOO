# Guarda o offset do mundo em relação à tela, para a câmera seguir o jogador

class ComponenteCamera:
    def __init__(self, offset_x: float = 0, offset_y: float = 0):
        self.offset_x = offset_x
        self.offset_y = offset_y