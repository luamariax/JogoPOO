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

CAMINHO_FASES = "Assets/fases"
TAMANHO_TILE = 64  # largura de cada tile de plataforma em pixels

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
        
        # Obtém os sprites das camadas (espera-se duas: superior e inferior)
        camadas = dado.get("camadas", [])
        if len(camadas) < 2:
            # Fallback: se não houver duas camadas definidas, não cria nada
            return entidades
        
        sprite_superior = camadas[0]["sprite"]   # ex: "grama_chao_superior"
        sprite_inferior = camadas[1]["sprite"]   # ex: "grama_chao_inferior"
        altura_tile = TAMANHO_TILE               # 64 pixels
        
        # Itera sobre a largura da tela em passos de TAMANHO_TILE
        for x in range(0, self.chao_x, TAMANHO_TILE):
            # Tile superior (grama)
            tile_sup = Entidade()
            tile_sup.adicionar_componente("posicao", ComponentePosicao(x, y_base, TAMANHO_TILE, altura_tile))
            tile_sup.adicionar_componente("colisao", ComponenteColisao(solido=True, tipo="normal"))
            tile_sup.adicionar_componente("sprite", ComponenteSprite(chave_imagem=sprite_superior))
            entidades.append(tile_sup)
            
            # Tile inferior (terra)
            tile_inf = Entidade()
            tile_inf.adicionar_componente("posicao", ComponentePosicao(x, y_base + altura_tile, TAMANHO_TILE, altura_tile))
            tile_inf.adicionar_componente("colisao", ComponenteColisao(solido=True, tipo="normal"))
            tile_inf.adicionar_componente("sprite", ComponenteSprite(chave_imagem=sprite_inferior))
            entidades.append(tile_inf)
        
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
    
    

    """def _criar_item(self, dado: dict) -> Entidade:
        x = dado["x"]
        y = self.chao_y + dado["y_offset"]
        e = Entidade()
        e.adicionar_componente("posicao", ComponentePosicao(x, y, dado["largura"], dado["altura"]))
        e.adicionar_componente("colisao", ComponenteColisao(solido=False, tipo="gatilho"))
        e.adicionar_componente("sprite", ComponenteSprite(chave_imagem=dado["sprite"]))
        # NOVO: componente de item
        e.adicionar_componente("item", ComponenteItem(tipo=dado["tipo_item"], valor=1))
        return e"""