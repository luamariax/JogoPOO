# "Chão" do jogo

from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.colisao import ComponenteColisao

class Plataforma(Entidade):
    def __init__(self, id: int, x: float, y: float, largura: float, altura: float):
        super().__init__(id)
        self.adicionar(ComponentePosicao(x, y, largura, altura))
        self.adicionar(ComponenteColisao())

    