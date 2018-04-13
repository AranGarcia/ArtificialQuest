'''
Altough refered to as a game because of pygame, this module actually manages
all the event handling and rendering of the simulation.
'''
import pygame
from questlogic import maps
from . import renders

class Game(object):
    """
    Main class of the simulation. It includes the logic part of the project,
    such as map data and characters, and a rendering object to manage all the
    images on screen
    """

    def __init__(self):

        self.gamemap = maps.Map('src/maps/dungeon')
        self.width = len(self.gamemap.matrix[0]) * 48 + 200
        self.height = len(self.gamemap.matrix) * 48 + 48

        # Game intialization
        pygame.init()
        pygame.display.set_caption('Artificial Quest')
        icon = pygame.image.load('src/img/icon.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.clk = pygame.time.Clock()
        self.renderer = \
            renders.Renderer(self.screen, self.gamemap, self.width, self.height)

    def run(self):
        ''' Starts rendering game objects and opens the window. '''

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.renderer.clicked(event.pos)

                if event.type == pygame.KEYDOWN:
                    self.renderer.keypressed(event)

            self.renderer.render()
            pygame.display.update()
