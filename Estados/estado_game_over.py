# Mostra pontuação final, opção de reiniciar ou voltar ao menu. 
# Transita para EstadoMenu ou EstadoJogo.
import pygame
from Estados.estado import Estado
from Model.jogador import Jogador
from Model.fase import Fase
from Model.Componentes.camera import ComponenteCamera

class EstadoGameOver(Estado):
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.controlador.rodando = False
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    self._reiniciar()
                elif evento.key == pygame.K_ESCAPE:
                    self.controlador.rodando = False

    def _reiniciar(self):
        c = self.controlador
        c.jogador = Jogador(x=100, y=c.tela.altura - 200)
        c.fase = Fase(c.jogador, c.tela.altura, c.tela.largura)
        c.fase.carregar("fase_tres.json")
        c.camera = ComponenteCamera()
        c.mudar_estado("jogo")

    def desenhar(self):
        self.controlador.tela.desenhar_game_over()
