# Guarda o offset do mundo em relação à tela, para a câmera seguir o jogador

"""class ComponenteCamera:
    def __init__(self, offset_x: float = 0, offset_y: float = 0):
        self.offset_x = offset_x
        self.offset_y = offset_y"""

# model/componentes/camera.py

class ComponenteCamera:
    """
    Armazena o offset da câmera para renderização.
    O SistemaCamera atualiza este componente a cada frame.
    """
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y