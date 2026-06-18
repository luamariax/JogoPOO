# Máquina de estados do jogo. Controla transições entre menu, jogo, pausa e game over.
# Não sabe quando trocar — os estados é que decidem isso. Ele só sabe como trocar.
import pygame

from View.tela_jogo_teste import TelaJogoTeste # TELA TESTE
from Model.jogador import Jogador
from Model.fase import Fase
from Model.Componentes.camera import ComponenteCamera
from Systems.sistema_fisica import SistemaFisica
from Systems.sistema_colisao import SistemaColisao
from Systems.sistema_camera import SistemaCamera
from Systems.sistema_animacao import SistemaAnimacao
from Systems.sistema_ia import SistemaIA
from Estados.estado_menu import EstadoMenu
from Estados.estado_jogo import EstadoJogo
from Estados.estado_pause import EstadoPause
from Estados.estado_game_over import EstadoGameOver

class ControladorJogo:
    def __init__(self):
        self.tela = TelaJogoTeste()  
        self.jogador = Jogador(x=100, y=self.tela.altura - 600)
        self.fase = Fase(self.jogador, self.tela.altura, self.tela.largura)
        self.fase.carregar("fase_tres.json")
        self.camera = ComponenteCamera()
        self.sistema_fisica = SistemaFisica(gravidade=0.4)
        self.sistema_colisao = SistemaColisao()
        self.sistema_camera = SistemaCamera(self.tela.largura)
        self.sistema_animacao = SistemaAnimacao()
        self.sistema_ia = SistemaIA()
        self.rodando = True
        self.fase_atual = 1

        self._estados = {
            "menu": EstadoMenu(self),
            "jogo": EstadoJogo(self),
            "pause": EstadoPause(self),
            "game_over": EstadoGameOver(self)
        }
        self.estado_atual = self._estados["menu"]

    def mudar_estado(self, nome:str):
        self.estado_atual.sair()
        self.estado_atual = self._estados[nome]
        self.estado_atual.entrar()

    def executar(self):
        while self.rodando:
            self.estado_atual.processar_eventos()
            self.estado_atual.atualizar()
            self.estado_atual.desenhar()
            self.tela.tick(60)
        self.tela.fechar()

    #-------------------------------------------------------

    def _verificar_pisar_inimigos(self):
        self._verificar_contato_inimigos()
        self._atualizar_invencibilidade()
        posicao_jog = self.jogador.obter_componente("posicao")
        fisica_jog = self.jogador.obter_componente("fisica")
        if not posicao_jog or not fisica_jog or fisica_jog.vel_y < 2:
            return
        rect_jog = pygame.Rect(posicao_jog.rect)
        for inimigo in self.fase.inimigos:
            ia = inimigo.obter_componente("ia")
            posicao_ini = inimigo.obter_componente("posicao")
            if not ia or not posicao_ini or ia.estado in ("voando", "morto"):
                continue
            rect_ini = pygame.Rect(posicao_ini.rect)
            if rect_jog.colliderect(rect_ini):
                if rect_jog.bottom <= rect_ini.centery:
                    ia.golpes += 1
                    fisica_jog.vel_y = -6
                    if ia.tipo == "patrulhar":
                        if ia.golpes >= 2:
                            ia.estado = "voando"
                        else:
                            ia.estado = "casco"
                    else:
                        ia.estado = "morto"

    def _verificar_contato_inimigos(self):
        posicao_jog = self.jogador.obter_componente("posicao")
        fisica_jog  = self.jogador.obter_componente("fisica")
        vida_jog    = self.jogador.obter_componente("vida")
        if not posicao_jog or not fisica_jog or not vida_jog:
            return
        if vida_jog.invencivel:
            return
        rect_jog = pygame.Rect(posicao_jog.rect)
        for inimigo in self.fase.inimigos:
            ia          = inimigo.obter_componente("ia")
            posicao_ini = inimigo.obter_componente("posicao")
            if not ia or not posicao_ini or ia.estado in ("voando", "morto"):
                continue
            rect_ini = pygame.Rect(posicao_ini.rect)
            if rect_jog.colliderect(rect_ini):
                foi_pisar = rect_jog.bottom <= rect_ini.centery and fisica_jog.vel_y > 0
                if not foi_pisar:
                    vida_jog.hp -= 1
                    vida_jog.invencivel = True
                    vida_jog.timer_invencivel = 90
                    if vida_jog.hp <= 0:
                        self.mudar_estado("game_over")
                    if ia.tipo == "voar":
                        ia.estado = "morto"

    def _atualizar_invencibilidade(self):
        vida_jog = self.jogador.obter_componente("vida")
        if vida_jog and vida_jog.invencivel:
            vida_jog.timer_invencivel -= 1
            if vida_jog.timer_invencivel <= 0:
                vida_jog.invencivel = False
