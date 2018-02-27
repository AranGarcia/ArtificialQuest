import pygame
from questlogic import maps, constants

# Data intialization
m = maps.Map()
m.load('src/maps/default')

width = len(m.matrix[0]) * 48
height = len(m.matrix) * 48

# Game initialization
pygame.init()


gd = pygame.display.set_mode((width, height))
pygame.display.set_caption('Artificial Quest')

wallimg = pygame.image.load('src/img/wall.png')
roadimg = pygame.image.load('src/img/road.png')
mountainimg = pygame.image.load('src/img/mountain.png')
landimg = pygame.image.load('src/img/land.png')
waterimg = pygame.image.load('src/img/water.png')
sandimg = pygame.image.load('src/img/sand.png')
forestimg = pygame.image.load('src/img/forest.png')

tiles = {
    0: wallimg,
    1: roadimg,
    2: mountainimg,
    3: landimg,
    4: waterimg,
    5: sandimg,
    6: forestimg
}


def drawtile(tilevalue, row, column):
    gd.blit(tiles[value], (row * 48, column * 48))


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for r, row in enumerate(m.matrix):
        for c, value in enumerate(row):
            drawtile(value, c, r)

    pygame.display.update()
