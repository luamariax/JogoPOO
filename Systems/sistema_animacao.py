

from Model.gerenciador_recursos import GerenciadorRecursos

class SistemaAnimacao:
    """
    A cada frame:
    1. Decide qual estado de animação usar com base na física do jogador
    2. Avança o contador e troca o frame quando necessário
    3. Atualiza ComponenteSprite com a imagem correta
    """

    def atualizar(self, entidades: list):
        for entidade in entidades:
            anim   = entidade.obter_componente("animacao")
            sprite = entidade.obter_componente("sprite")
            fisica = entidade.obter_componente("fisica")
            if not anim or not sprite:
                continue

            if fisica and not entidade.obter_componente("ia"):
                self._definir_estado(anim, fisica, sprite)

            self._avancar_frame(anim, sprite)

    def _definir_estado(self, anim, fisica, sprite):
        """Escolhe a animação com base na velocidade e direção do jogador."""
        if fisica.vel_x > 0:
            novo_estado = "andar_direita"
            sprite.flip_x = False
        elif fisica.vel_x < 0:
            novo_estado = "andar_esquerda"
            sprite.flip_x = True
        else:
            # parado — congela no primeiro frame da última direção
            return

        # Só reinicia o frame se trocou de estado
        if novo_estado != anim.estado_atual:
            anim.estado_atual = novo_estado
            anim.frame_atual = 0
            anim.contador = 0

    def _avancar_frame(self, anim, sprite):
        """Avança o contador e atualiza a imagem quando necessário."""
        anim.contador += 1
        if anim.contador < anim.velocidade:
            return

        anim.contador = 0
        frames = anim.animacoes.get(anim.estado_atual, [])
        if not frames:
            return

        anim.frame_atual = (anim.frame_atual + 1) % len(frames)
        chave = frames[anim.frame_atual]
        sprite.imagem = GerenciadorRecursos.obter(chave)