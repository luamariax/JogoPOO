# model/fase.py
import json
import os
from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.colisao import ComponenteColisao

CAMINHO_FASES = "Assets/fases"

class Fase:
    """Carrega e gerencia as entidades de uma fase a partir de JSON."""

    def __init__(self, jogador: Entidade, tamanho_tela_y: int, tamanho_tela_x: int):
        self.jogador = jogador
        self.entidades = []
        self.plataformas = []
        self.chao_y = tamanho_tela_y
        self.chao_x = tamanho_tela_x

    def adicionar_entidade(self, entidade: Entidade):
        self.entidades.append(entidade)
        col = entidade.obter_componente("colisao")
        if col and col.solido:
            self.plataformas.append(entidade)

    def carregar(self, nome_arquivo: str):
        """Carrega fase a partir de um arquivo JSON."""
        caminho = os.path.join(CAMINHO_FASES, nome_arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        for dado in dados["entidades"]:
            entidade = self._criar_entidade(dado)
            if entidade:
                self.adicionar_entidade(entidade)

        self.entidades.append(self.jogador)

    def _criar_entidade(self, dado: dict) -> Entidade | None:
        """Cria uma entidade a partir de um dicionário JSON."""
        tipo = dado.get("tipo")

        if tipo == "plataforma":
            return self._criar_plataforma(dado)

        # futuramente: "inimigo", "item", "boss"
        return None

    def _criar_plataforma(self, dado: dict) -> Entidade:
        x = dado["x"]
        y = self.chao_y + dado["y_offset"]
        largura = self.chao_x if dado.get("largura_tela") else dado["largura"]
        altura = dado["altura"]
        solido = dado.get("solido", True)
        tipo_colisao = dado.get("tipo_colisao", "normal")

        plataforma = Entidade()
        plataforma.adicionar_componente("posicao", ComponentePosicao(x, y, largura, altura))
        plataforma.adicionar_componente("colisao", ComponenteColisao(solido=solido, tipo=tipo_colisao))
        return plataforma