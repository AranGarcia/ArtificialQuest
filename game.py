import pygame
import questdata

# Data intialization
m = questdata.Map()
m.load('src/maps/map1')

width = len(m.matrix[0]) * 48
height = len(m.matrix) * 48

cwall = (0, 0, 0)
cpath = (128, 128, 128)

# Game initialization
pygame.init()


gd = pygame.display.set_mode((width, height))
pygame.display.set_caption('Practica 1')

wallimg = pygame.image.load('src/img/wall.png')
floorimg = pygame.image.load('src/img/floor.png')


def drawtile(tilevalue, row, column):
    if tilevalue == questdata.WALL:
        gd.blit(wallimg, (row * 48, column * 48))
    else:
        gd.blit(floorimg, (row * 48, column * 48))


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for r, row in enumerate(m.matrix):
        for c, value in enumerate(row):
            drawtile(value, c, r)

    pygame.display.update()
