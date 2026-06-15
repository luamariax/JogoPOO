#Onde a entidade está no mundo

class ComponentePosicao:
    """
    Armazena a posição e as dimensões de uma entidade no mundo.
    Apenas dados – nenhum método de movimento ou colisão.
    """
    def __init__(self, x: int, y: int, largura: int, altura: int):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura

    @property
    def rect(self):
        """Retorna uma tupla no formato (x, y, largura, altura) para uso com pygame.Rect."""
        return (self.x, self.y, self.largura, self.altura)

    @property
    def centro_x(self):
        return self.x + self.largura // 2

    @property
    def centro_y(self):
        return self.y + self.altura // 2