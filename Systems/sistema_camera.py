# Atualiza o offset seguindo o jogador
# systems/sistema_camera.py
class SistemaCamera:
    """Atualiza o offset da câmera para seguir o jogador no eixo X."""
    def __init__(self, tela_largura: int):
        self.tela_largura = tela_largura

    def atualizar(self, camera_comp, jogador_pos, largura_mundo: int = 0):
        if not camera_comp or not jogador_pos:
            return
        # Centraliza o jogador horizontalmente
        camera_comp.x = jogador_pos.x + jogador_pos.largura // 2 - self.tela_largura // 2
        # Limita para não mostrar áreas vazias
        if camera_comp.x < 0:
            camera_comp.x = 0
        limite_direita = largura_mundo - self.tela_largura
        if largura_mundo > 0 and camera_comp.x > limite_direita:
            camera_comp.x = limite_direita