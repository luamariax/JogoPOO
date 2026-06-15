#Para o SistemaColisao trabalhar
# model/componentes/colisao.py


class ComponenteColisao:
    """
    Indica que a entidade pode colidir com outras.
    'solido' = bloqueio de passagem (plataformas, chão).
    'tipo'   = como o sistema deve tratar essa colisão.
    """
    def __init__(self, solido: bool = True, tipo: str = "normal"):
        self.solido = solido
        self.tipo = tipo   # "normal", "dano", "gatilho"
        