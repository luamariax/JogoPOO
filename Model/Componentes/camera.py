# Guarda o offset do mundo em relação à tela, para a câmera seguir o jogador
# model/componentes/camera.py

class ComponenteCamera:
    """
    Armazena o offset da câmera para renderização.
    O SistemaCamera atualiza este componente a cada frame.
    """
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y