'''
Altough refered to as a game because of pygame, this module actually manages
all the event handling and rendering of the simulation.
'''
import pygame
from questlogic import maps
from . import renders, world1renderer, world2renderer, world3renderer
from enum import Enum

class GameType(Enum):
    DUNGEON = 1
    WORLD1 = 2
    WORLD2 = 3
    WORLD3 = 4


class Game:
    """
    Main class of the simulation. It includes the logic part of the project,
    such as map data and characters, and a rendering object to manage all the
    images on screen.
    """

    def __init__(self, typeGame):
        self.gamemap = Game.get_map(typeGame)
        self.width = len(self.gamemap.matrix[0]) * 48 + 300
        self.height = len(self.gamemap.matrix) * 48 + 48

        # Game intialization
        pygame.init()
        pygame.display.set_caption('Artificial Quest')
        icon = pygame.image.load('src/img/icon.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.clk = pygame.time.Clock()
        rend = Game.get_renderer(typeGame)
        self.renderer = rend(self.screen, self.gamemap, self.width, self.height)

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

    @staticmethod
    def get_renderer(gtype):
        if gtype == GameType.DUNGEON:
            return renders.Renderer
        elif gtype == GameType.WORLD1:
            return world1renderer.World1Renderer
        elif gtype == GameType.WORLD2:
            return world2renderer.World2Renderer
        elif gtype == GameType.WORLD3:
            return world3renderer.World3Renderer

    @staticmethod
    def get_map(gmap):
        if gmap == GameType.DUNGEON:
            return maps.Map('src/maps/dungeon')
        elif gmap == GameType.WORLD1:
            return maps.Map('src/maps/mission1')
        elif gmap == GameType.WORLD2:
            return maps.Map('src/maps/mission2')
        elif gmap == GameType.WORLD3:
            return maps.Map('src/maps/mission3')
