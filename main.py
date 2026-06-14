import pygame

pygame.init()
sheet = pygame.image.load("mini_capy.png").convert_alpha()
LARGURA_SPRITE  = 48   # ajuste conforme o tamanho real
ALTURA_SPRITE   = 48
COLUNAS         = 5
LINHAS          = 8

def recortar_sheet(sheet, larg, alt, colunas, linhas):
    sprites = []
    for linha in range(linhas):
        for col in range(colunas):
            rect = pygame.Rect(col * larg, linha * alt, larg, alt)
            sprites.append(sheet.subsurface(rect))
    return sprites

todos = recortar_sheet(sheet, LARGURA_SPRITE, ALTURA_SPRITE, COLUNAS, LINHAS)