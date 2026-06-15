#lê ComponenteFisica de todas as entidades → atualiza ComponentePosicao

import pygame
from Model.Componentes.fisica import ComponenteFisica
from Model.Componentes.posicao import ComponentePosicao

class SistemaFisica:
    def atualizar(self, entidades):
        for entidade in entidades:
            fisica = entidade.obter(ComponenteFisica)
            posicao = entidade.obter(ComponentePosicao)

            if fisica and posicao:
                # Aplica gravidade
                if not fisica.no_chao:
                    fisica.vel_y += 0.5  # gravidade

                # Atualiza posição
                posicao.x += fisica.vel_x
                posicao.y += fisica.vel_y

                #Limita para não sair da tela
                if posicao.x < 0:
                    posicao.x = 0
                if posicao.x + posicao.largura > 800:
                    posicao.x = 800 - posicao.largura
