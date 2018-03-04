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

class Renderer:
    """ Manager of the objects to be rendered in the game """

    def __init__(self, gamedisplay, gamemap, width, height):
        self.gd = gamedisplay
        self.width = width
        self.height = height

        # Rendered objects
        self.gameobjects = [
            GameMap(self.gd, (0, 0), gamemap),
            InfoBar(self.gd, width, (0, height - 30))
        ]

    def render(self):
        for gobj in self.gameobjects:
            gobj.render()

    def select(self, coords):
        """ Activates the selection tile """

        # Activate cursor if click was on the map
        if coords[1] < (self.height - 30):
            tilecoords = ((coords[0] // 48), (coords[1] // 48))
            if tilecoords != self.gameobjects[0].selectedtile:
                self.gameobjects[0].selectedtile = tilecoords

                terraintype = self.gameobjects[0].getterrain(tilecoords)
                infostring = constants.terrainnames[terraintype] \
                    + ' ' +  str(tilecoords)
                self.gameobjects[1].prepare(infostring)
            else:
                self.gameobjects[0].selectedtile = None
                self.gameobjects[1].reset()

        # Deactivates cursor with click off map
        else:
            self.gameobjects[0].selectedtile = None
            self.gameobjects[1].reset()

class ScreenSection:
    """docstring for Render."""
    def __init__(self, gd, coords):
        self.coords = coords
        self.gd = gd

    def render(self):
        """ Abstract method for rendered objects """
        raise NotImplementedError

class GameMap(ScreenSection):
    """docstring for GameMap."""
    def __init__(self, gd, coords, gamemap):
        super(GameMap, self).__init__(gd, coords)
        self.gamemap = gamemap

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

        # Map cursor
        self.selectedtile = None
        self.selectimg = pygame.image.load('src/img/selectbox.png')

    def render(self):
        for r, row in enumerate(self.gamemap.matrix):
            for c, value in enumerate(row):
                self.gd.blit(self.landtiles[value], (c * 48, r * 48))

        if self.selectedtile:
            self.gd.blit(self.selectimg, (self.selectedtile[0] * 48, self.selectedtile[1] * 48))

    def getterrain(self, coords):
        return self.gamemap.matrix[coords[1]][coords[0]]

class InfoBar(ScreenSection):
    """docstring for GameInfo."""
    def __init__(self, gd, width, coords):
        super(InfoBar, self).__init__(gd, coords)
        self.width = width

        # Info section
        self.selected = False
        self.color = (0, 0, 0)
        self.txtcolor = (255, 255, 255)
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.txtsurf = None
        self.textrect = None

    def render(self):
        pygame.draw.rect(self.gd, self.color, (
            self.coords[0],
            self.coords[1],
            self.width,
            30
        ))

        if self.selected:
            self.txtrect.topleft = (self.coords[0] + 5, self.coords[1] + 5)
            self.gd.blit(self.txtsurf, self.txtrect)

    def prepare(self, text):
        self.selected = True
        self.txtsurf = self.font.render('Info: ' + text, True, self.txtcolor)
        self.txtrect  = self.txtsurf.get_rect()

    def reset(self):
        self.selected = False
        self.txtsurf = None
        self.txtrect = None
