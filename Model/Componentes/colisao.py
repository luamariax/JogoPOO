#Para o SistemaColisao trabalhar

class ComponenteColisao:
    def __init__(self, solido: bool = True):
        self.solido = solido
        self.colidindo_com = []  # preenchido pelo SistemaColisao a cada frame