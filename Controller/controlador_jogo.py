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

class ControladorJogo:
    def __init__(self):
        self.tela = TelaJogoTeste()   # <== MUDE AQUI!
        self.jogador = Jogador(x=100, y=self.tela.altura - 600)
        self.fase = Fase(self.jogador, self.tela.altura, self.tela.largura)
        self.fase.carregar("fase_dois.json")
        self.camera = ComponenteCamera()
        self.sistema_fisica = SistemaFisica(gravidade=0.5)
        self.sistema_colisao = SistemaColisao()
        self.sistema_camera = SistemaCamera(self.tela.largura)
        self.sistema_animacao = SistemaAnimacao()
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
                        self.fase.carregar("fase_dois.json")
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
        # Aplica física em todas entidades (inclui jogador e possíveis inimigos futuros)
        self.sistema_fisica.atualizar(self.fase.entidades)
        # Resolve colisão do jogador com plataformas
        self.sistema_colisao.resolver_colisoes(self.jogador, self.fase.plataformas)
        #Atualiza a sprite de movimento
        self.sistema_animacao.atualizar(self.fase.entidades) 
        # Atualiza câmera
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
