# Máquina de estados do jogo. Controla transições entre menu, jogo, pausa e game over.
# Não sabe quando trocar — os estados é que decidem isso. Ele só sabe como trocar.

import pygame
from View.tela_jogo import TelaJogo
from Controller.controlador_input import ControladorInput
from Model.jogador import Jogador
from Systems.sistema_fisica import SistemaFisica
from Systems.sistema_colisao import SistemaColisao
from Model.plataforma import Plataforma

class ControladorJogo:
    def __init__(self):
        self.tela = TelaJogo()
        self.input = ControladorInput()
        self.jogador = Jogador(id=1, x=400, y=100)
        self.entidades = [self.jogador]
        self.sistema_fisica = SistemaFisica()
        self.sistema_colisao = SistemaColisao()
        self.rodando = True

        plataforma = Plataforma(id=2, x=0, y=500, largura=800, altura=50)
        self.entidades.append(plataforma)

    def trocar_estado(self, novo_estado):
        self.estado_atual = novo_estado

    def iniciar(self):
        while self.rodando:
            self.tela.clock.tick(60)
            eventos = pygame.event.get()
            self.sistema_fisica.atualizar(self.entidades)        
            self.sistema_colisao.verificar(self.entidades, self.jogador)  
            self.input.processar_eventos(self.jogador, eventos)  
            self.tela.desenhar(self.entidades)                   