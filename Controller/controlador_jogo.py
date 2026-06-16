# Máquina de estados do jogo. Controla transições entre menu, jogo, pausa e game over.
# Não sabe quando trocar — os estados é que decidem isso. Ele só sabe como trocar.
import pygame
import sys
from Controller.controlador_input import ControladorInput
from View.tela_jogo import TelaJogo
from View.tela_jogo_teste import TelaJogoTeste # TELA TESTE
from Model.jogador import Jogador
from Model.fase import Fase
from Model.Componentes.camera import ComponenteCamera
from Systems.sistema_fisica import SistemaFisica
from Systems.sistema_colisao import SistemaColisao
from Systems.sistema_camera import SistemaCamera
from Systems.sistema_animacao import SistemaAnimacao
from Systems.sistema_ia import SistemaIA

class ControladorJogo:
    def __init__(self):
        self.tela = TelaJogoTeste()   # <== MUDE AQUI!
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
        self.estado = "menu"          # estados: menu, jogo, pause
        self.fase_atual = 1


    def processar_eventos(self):
        """Processa eventos de teclado e fechamento da janela."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                return

            if evento.type == pygame.KEYDOWN:
                # Estado MENU
                if self.estado == "menu":
                    if evento.key == pygame.K_RETURN:
                        self.jogador = Jogador(x=100, y=self.tela.altura - 200)
                        self.fase = Fase(self.jogador, self.tela.altura, self.tela.largura)
                        self.fase.carregar("fase_tres.json")
                        self.camera = ComponenteCamera()
                        self.estado = "jogo"
                    elif evento.key == pygame.K_ESCAPE:
                        self.rodando = False

                # Estado JOGO
                elif self.estado == "jogo":
                    if evento.key == pygame.K_p:
                        self.estado = "pause"
                    elif evento.key == pygame.K_ESCAPE:
                        self.rodando = False

                # Estado PAUSE
                elif self.estado == "pause":
                    if evento.key == pygame.K_p:
                        self.estado = "jogo"
                    elif evento.key == pygame.K_ESCAPE:
                        self.rodando = False
                        
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.estado == "menu":
                    mouse = pygame.mouse.get_pos()
                    if self.tela.btn_continuar.collidepoint(mouse) or self.tela.btn_novo_jogo.collidepoint(mouse):
                        self.jogador = Jogador(x=100, y=self.tela.altura - 200)
                        self.fase = Fase(self.jogador, self.tela.altura, self.tela.largura)
                        self.fase.carregar("fase_dois.json")
                        self.camera = ComponenteCamera()
                        self.estado = "jogo"


        # Movimento contínuo (setas) apenas no estado jogo
        if self.estado == "jogo":
            ControladorInput.processar_teclado(self.jogador)
        else:
            # Se não estiver no jogo, garante que o jogador não receba velocidade
            fisica = self.jogador.obter_componente("fisica")
            if fisica:
                fisica.vel_x = 0

    def atualizar_jogo(self):
        if self.estado != "jogo":
            return
        self.sistema_fisica.atualizar_x(self.fase.entidades)
        self.sistema_colisao.resolver_colisoes_x(self.jogador, self.fase.plataformas)
        self.sistema_colisao.resolver_colisoes_inimigos_x(self.fase.inimigos, self.fase.plataformas)
        self.sistema_fisica.atualizar_y(self.fase.entidades)
        self.sistema_colisao.resolver_colisoes_y(self.jogador, self.fase.plataformas)
        self.sistema_colisao.resolver_colisoes_inimigos_y(self.fase.inimigos, self.fase.plataformas)
        self.sistema_ia.atualizar(self.fase.inimigos, self.fase.plataformas)
        self._verificar_pisar_inimigos()
        self.sistema_animacao.atualizar(self.fase.entidades) 
        pos_jog = self.jogador.obter_componente("posicao")
        self.sistema_camera.atualizar(self.camera, pos_jog)

    def verificar_coleta_itens(self):
        for entidade in self.fase.entidades[:]:  # iterar sobre cópia
            item = entidade.obter_componente("item")
            if item and not item.coletado:
                # Verifica colisão com o jogador
                pos_jog = self.jogador.obter_componente("posicao")
                pos_item = entidade.obter_componente("posicao")
                if pos_jog and pos_item and pos_jog.rect.colliderect(pos_item.rect):
                    item.coletado = True
                    self.fase.entidades.remove(entidade)
                    if item.tipo == "moeda":
                        self.moedas += item.valor
                        print(f"Moeda coletada! Total: {self.moedas}")

    def _verificar_pisar_inimigos(self):
        self._verificar_contato_inimigos()
        self._atualizar_invencibilidade()
        posicao_jog = self.jogador.obter_componente("posicao")
        fisica_jog = self.jogador.obter_componente("fisica")
        if not posicao_jog or not fisica_jog or fisica_jog.vel_y <= 0:
            return
        rect_jog = pygame.Rect(posicao_jog.rect)
        for inimigo in self.fase.inimigos:
            ia = inimigo.obter_componente("ia")
            posicao_ini = inimigo.obter_componente("posicao")
            if not ia or not posicao_ini or ia.estado == "voando":
                continue
            rect_ini = pygame.Rect(posicao_ini.rect)
            if rect_jog.colliderect(rect_ini):
                if rect_jog.bottom - fisica_jog.vel_y <= rect_ini.top + 4:
                    ia.golpes += 1
                    fisica_jog.vel_y = -6
                    if ia.golpes >= 2:
                        ia.estado = "voando"
                    else:
                        ia.estado = "casco"

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
            if not ia or not posicao_ini or ia.estado == "voando":
                continue
            rect_ini = pygame.Rect(posicao_ini.rect)
            if rect_jog.colliderect(rect_ini):
                foi_pisar = rect_jog.centery < rect_ini.centery
                if not foi_pisar:
                    vida_jog.hp -= 1
                    vida_jog.invencivel = True
                    vida_jog.timer_invencivel = 90

    def _atualizar_invencibilidade(self):
        vida_jog = self.jogador.obter_componente("vida")
        if vida_jog and vida_jog.invencivel:
            vida_jog.timer_invencivel -= 1
            if vida_jog.timer_invencivel <= 0:
                vida_jog.invencivel = False


    def executar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar_jogo()

            # Desenha a tela correta com base no estado
            if self.estado == "menu":
                self.tela.desenhar_menu()
            elif self.estado == "jogo":
                self.tela.desenhar_jogo(self.fase.entidades, self.camera)
            elif self.estado == "pause":
                self.tela.desenhar_pause(self.fase_atual)

            self.tela.tick(60)

        self.tela.fechar()
