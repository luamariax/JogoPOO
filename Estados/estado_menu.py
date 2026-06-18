# Tela inicial, mostra opções de novo jogo e continuar. 
# Transita para EstadoJogo.
import pygame
from Estados.estado import Estado
from Model.jogador import Jogador
from Model.fase import Fase
from Model.Componentes.camera import ComponenteCamera

class EstadoMenu(Estado):
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.controlador.rodando = False
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    self._iniciar_jogo()
                elif evento.key == pygame.K_ESCAPE:
                    self.controlador.rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse = pygame.mouse.get_pos()
                tela = self.controlador.tela
                if tela.btn_continuar.collidepoint(mouse) or tela.btn_novo_jogo.collidepoint(mouse):
                    self._iniciar_jogo()

    def _iniciar_jogo(self):
        c = self.controlador
        c.jogador = Jogador(x=100, y=c.tela.altura - 200)
        c.fase = Fase(c.jogador, c.tela.altura, c.tela.largura)
        c.fase.carregar("fase_tres.json")
        c.camera = ComponenteCamera()
        c.mudar_estado("jogo")

    def desenhar(self):
        self.controlador.tela.desenhar_menu()
