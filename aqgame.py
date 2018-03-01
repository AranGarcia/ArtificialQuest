import pygame
from questlogic import maps, constants

terrenum = constants.Terrain

class Game(object):
    """docstring for Game."""

    def __init__(self):

        self.gamemap = maps.Map('src/maps/dungeon')
        self.width = len(self.gamemap.matrix[0]) * 48
        self.height = len(self.gamemap.matrix) * 48 + 30

        # Game intialization
        pygame.init()
        pygame.display.set_caption('Artificial Quest')
        self.gd = pygame.display.set_mode((self.width, self.height))
        self.clk = pygame.time.Clock()
        self.renderer = Renderer(self.gd, self.gamemap, self.width, self.height)

    def run(self):
        ''' Starts rendering game objects and opens the window. '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.renderer.select(event.pos)

            self.renderer.render()
            pygame.display.update()

class Renderer(object):
    """ Manager of the objects to be rendered in the game """
    def __init__(self, gamedisplay, gamemap, width, height):
        self.gd = gamedisplay
        self.gamemap = gamemap
        self.width = width
        self.height = height

        # Map objects

        self.landtiles = {
            terrenum.WALL.value: pygame.image.load('src/img/wall.png'),
            terrenum.ROAD.value: pygame.image.load('src/img/road.png'),
            terrenum.MOUNTAIN.value: pygame.image.load('src/img/mountain.png'),
            terrenum.LAND.value: pygame.image.load('src/img/land.png'),
            terrenum.WATER.value: pygame.image.load('src/img/water.png'),
            terrenum.SAND.value: pygame.image.load('src/img/sand.png'),
            terrenum.FOREST.value: pygame.image.load('src/img/forest.png')
        }

        self.selection = None
        self.selectimg = pygame.image.load('src/img/selectbox.png')
        self.barcorner = pygame.image.load('src/img/corner.png')
        self.bar = pygame.image.load('src/img/bar.png')

    def render(self):
        # Draw map object
        for r, row in enumerate(self.gamemap.matrix):
            for c, value in enumerate(row):
                self.__drawtile(value, c, r)

        # Draw bar
        self.gd.blit(self.barcorner, (0, self.height - 30))
        pygame.draw.rect(self.gd, (185, 183, 170), (48, self.height - 30, self.width, self.height))

        # Selector, if active
        if self.selection:
            self.gd.blit(self.selectimg, self.selection)

    def select(self, coords):
        """ Activates the selection tile """

        x = (coords[0] // 48) * 48
        y = (coords[1] // 48) * 48

        if coords[1] > (self.height - 30):
            self.selection = None
        elif not self.selection or self.selection != coords:
            self.selection = (x,y)
        else:
            self.selection = None

    def __drawtile(self, value, row, column):
        self.gd.blit(self.landtiles[value], (row * 48, column * 48))
