#lê ComponenteFisica de todas as entidades → atualiza ComponentePosicao
# systems/sistema_fisica.py
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.posicao import ComponentePosicao

class SistemaFisica:
    """Aplica gravidade e atualiza posição com base na velocidade."""
    def __init__(self, gravidade: float = 0.5):
        self.gravidade = gravidade

    def atualizar(self, entidades: list):
        for entidade in entidades:
            fisica = entidade.obter_componente("fisica")
            posicao = entidade.obter_componente("posicao")
            if not fisica or not posicao:
                continue

            # Aplica gravidade se necessário
            if fisica.gravidade:
                fisica.vel_y += self.gravidade

            # Atualiza posição com base na velocidade
            posicao.x += fisica.vel_x
            posicao.y += fisica.vel_y
