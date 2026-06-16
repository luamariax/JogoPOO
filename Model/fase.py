# model/fase.py
import json
import os
import pygame
from Model.entidade import Entidade
from Model.Componentes.posicao import ComponentePosicao
from Model.Componentes.colisao import ComponenteColisao
from Model.Componentes.sprite import ComponenteSprite
from Model.gerenciador_recursos import GerenciadorRecursos
from Model.Componentes.item import ComponenteItem
from Model.Inimigos.caminhante import Caminhante

CAMINHO_FASES = "Assets/fases"
TAMANHO_TILE = 64  # largura de cada tile de plataforma em pixels

class Fase:
    """Carrega e gerencia as entidades de uma fase a partir de JSON."""

    def __init__(self, jogador: Entidade, tamanho_tela_y: int, tamanho_tela_x: int):
        self.jogador = jogador
        self.entidades = []
        self.plataformas = []
        self.inimigos = []
        self.chao_y = tamanho_tela_y
        self.chao_x = tamanho_tela_x
        self.largura_mundo = tamanho_tela_x   # inicialmente igual à tela

    def adicionar_entidade(self, entidade: Entidade):
        self.entidades.append(entidade)
        col = entidade.obter_componente("colisao")
        if col and col.solido:
            self.plataformas.append(entidade)
        ia = entidade.obter_componente("ia")
        if ia:
            self.inimigos.append(entidade)


    def carregar(self, nome_arquivo: str):
        caminho = os.path.join(CAMINHO_FASES, nome_arquivo)
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except FileNotFoundError:
            print(f"Erro: fase '{nome_arquivo}' não encontrada.")
            return

        # 1. Carrega todos os sprites definidos no JSON
        sprites_dict = dados.get("sprites", {})
        GerenciadorRecursos.carregar_lote(sprites_dict, tamanho_padrao=(TAMANHO_TILE, TAMANHO_TILE))

        # Descobre o tamanho do mundo primeiro pra poder criar o chão
        if "largura_mundo" in dados:
            self.largura_mundo = dados["largura_mundo"]

        # 2. Cria as entidades (chão, plataformas, itens)
        for dado in dados["entidades"]:
            entidades_criadas = self._criar_entidade(dado)
            for ent in entidades_criadas:
                self.adicionar_entidade(ent)

        # 3. Atribui as imagens (Surface) a cada ComponenteSprite
        GerenciadorRecursos.aplicar_sprites(self.entidades)

        # 4. Adiciona o jogador (já existente)
        self.entidades.append(self.jogador)


    def _criar_entidade(self, dado: dict) -> list[Entidade]:
        tipo = dado.get("tipo")
        if tipo == "chao":
            return self._criar_chao(dado)
        if tipo == "plataforma":
            return self._criar_plataforma(dado)
        if tipo == "item":
            return [self._criar_item(dado)]
        if tipo == "caminhante":
            return [self._criar_caminhante(dado)]
        return []

    def _criar_chao(self, dado: dict) -> list[Entidade]:
        """
        Cria o chão como uma sequência de colunas de dois tiles (superior e inferior),
        repetindo ao longo de toda a largura da tela (self.chao_x).
        Cada tile tem tamanho TAMANHO_TILE (64px).
        """
        entidades = []
        # Posição Y base do chão (vinda do JSON)
        y_base = self.chao_y + dado["y_offset"]
        
        # Obtém os sprites das camadas 
        sprites_camadas = dado.get("sprites_camadas", [])
        if not sprites_camadas:
            return entidades
        
        altura_tile = TAMANHO_TILE               # 64 pixels
        
         # Determina a largura do chão
        if dado.get("largura_tela", False):
            largura_chao = self.largura_mundo
        else:
            largura_chao = dado.get("largura", self.largura_mundo)

        # Itera sobre a largura da tela em passos de TAMANHO_TILE
        for x in range(0, largura_chao, TAMANHO_TILE):
            y_atual = y_base
            for idx, chave_sprite in enumerate(sprites_camadas):
                tile = Entidade()
                tile.adicionar_componente("posicao", ComponentePosicao(x, y_atual, TAMANHO_TILE, TAMANHO_TILE))
                tile.adicionar_componente("colisao", ComponenteColisao(solido=True, tipo="normal"))
                tile.adicionar_componente("sprite", ComponenteSprite(chave_imagem=chave_sprite))
                entidades.append(tile)
                y_atual += TAMANHO_TILE
        return entidades

    def _criar_plataforma(self, dado: dict) -> list[Entidade]:
        """
        Plataforma composta por tiles: ponta esquerda, N tiles do meio, ponta direita.
        Cada tile é uma entidade separada com seu próprio sprite.
        """
        entidades = []
        x = dado["x"]
        y = self.chao_y + dado["y_offset"]
        largura_total = dado["largura"]
        altura = dado["altura"]
        sprites = dado["sprites"]

        # Ponta esquerda
        entidades.append(self._criar_tile(x, y, TAMANHO_TILE, altura, sprites["esquerda"], solido=True))
        x += TAMANHO_TILE

        # Tiles do meio
        largura_meio = largura_total - 2 * TAMANHO_TILE
        for _ in range(largura_meio // TAMANHO_TILE):
            entidades.append(self._criar_tile(x, y, TAMANHO_TILE, altura, sprites["meio"], solido=True))
            x += TAMANHO_TILE

        # Ponta direita
        entidades.append(self._criar_tile(x, y, TAMANHO_TILE, altura, sprites["direita"], solido=True))

        return entidades
    
    def _criar_tile(self, x, y, largura, altura, chave_sprite, solido=True) -> Entidade:
        e = Entidade()
        e.adicionar_componente("posicao", ComponentePosicao(x, y, largura, altura))
        e.adicionar_componente("colisao", ComponenteColisao(solido=solido, tipo="normal"))
        e.adicionar_componente("sprite", ComponenteSprite(chave_imagem=chave_sprite))
        return e

    def _criar_item(self, dado: dict) -> Entidade:
        x = dado["x"]
        y = self.chao_y + dado["y_offset"]
        e = Entidade()
        e.adicionar_componente("posicao", ComponentePosicao(x, y, dado["largura"], dado["altura"]))
        e.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="gatilho"))
        e.adicionar_componente("sprite", ComponenteSprite(chave_imagem=dado["sprite"]))
        return e
    
    def _criar_caminhante(self, dado: dict) -> Entidade:
        x = dado["x"]
        y = self.chao_y + dado["y_offset"]
        return Caminhante(x, y)

    

