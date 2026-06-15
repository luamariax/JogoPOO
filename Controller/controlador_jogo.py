# Máquina de estados do jogo. Controla transições entre menu, jogo, pausa e game over.
# Não sabe quando trocar — os estados é que decidem isso. Ele só sabe como trocar.
# controller/controlador_jogo.py
import pygame
from Controller.controlador_input import ControladorInput
from View.tela_jogo_teste import TelaJogo
from Model.jogador import Jogador

class ControladorJogo:
    """Responsável pelo loop principal e delegação de tarefas."""
    def __init__(self):
        self.tela = TelaJogo()
        self.jogador = Jogador(id=0, x=100, y=100)   # posição inicial perto do chão
        self.rodando = True

    def atualizar_fisica(self):
        """Atualiza a posição do jogador com base na velocidade (sem gravidade na Fase 1)."""
        fisica = self.jogador.obter("fisica")
        pos = self.jogador.obter("posicao")
        if not fisica or not pos:
            return

        # Movimento horizontal
        pos.x += fisica.vel_x

        # Limites simples da tela (impede sair pela borda)
        if pos.x < 0:
            pos.x = 0
        if pos.x + pos.largura > self.tela.largura:
            pos.x = self.tela.largura - pos.largura

        # A gravidade ainda não foi implementada – a posição Y não é alterada

    def processar_eventos(self):
        """Trata evento de fechar a janela."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

    def executar(self):
        """Loop principal do jogo."""
        while self.rodando:
            self.processar_eventos()
            ControladorInput.processar_teclado(self.jogador)
            self.atualizar_fisica()
            self.tela.desenhar(self.jogador)
            self.tela.tick(60)

        self.tela.fechar()