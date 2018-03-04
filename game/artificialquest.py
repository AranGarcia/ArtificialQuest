'''
Altough refered to as a game because of pygame, this module actually manages
all the event handling and rendering of the simulation.
'''
import pygame
from questlogic import maps, constants

terrenum = constants.Terrain
pixelfont = r'/home/aran/Documents/Escuela/Artificial_Intelligence/Practica1/src/fonts/PressStart2P.ttf'
kpevents = set(['0', '1', '2', '3', '4', '5', '6'])

class Game(object):
    """
    Main class of the simulation. It includes the logic part of the project,
    such as map data and characters, and a rendering object to manage all the
    images on screen
    """

    def __init__(self):

        self.gamemap = maps.Map('src/maps/dungeon')
        self.width = len(self.gamemap.matrix[0]) * 48 + 200
        self.height = len(self.gamemap.matrix) * 48

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
                    self.renderer.clicked(event.pos)

                if event.type == pygame.KEYDOWN:
                    self.renderer.keypressed(event.unicode)

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
            InfoBar(self.gd, height, (width - 200, 0))
        ]

    def render(self):
        """
        Call the implemented render method on each overridden render object.
        """
        for gobj in self.gameobjects:
            gobj.render()

    def clicked(self, coords):
        """ Activates event on mouse click. """

        # Activate cursor if click was on the map
        if coords[0] < (self.width - 200):
            tilecoords = ((coords[0] // 48), (coords[1] // 48))
            if tilecoords != self.gameobjects[0].selectedtile:
                # Selection cursor on map
                self.gameobjects[0].selectedtile = tilecoords

                # Info of the selected tile
                terraintype = self.gameobjects[0].getterrain(tilecoords)
                self.gameobjects[1].prepare(constants.terrainnames[terraintype],
                    str(tilecoords))
            else:
                # Deactivates cursor if clicked on same selected tile
                self.gameobjects[0].selectedtile = None
                self.gameobjects[1].reset()

        # Deactivates cursor with click off map
        else:
            self.gameobjects[0].selectedtile = None
            self.gameobjects[1].reset()

    def keypressed(self, value):
        """ Process event on key press. """
        if self.gameobjects[1].selected and value in kpevents:
            self.gameobjects[0].changeterrain(int(value))
            terraintype = self.gameobjects[0].getselected()
            self.gameobjects[1].prepare(constants.terrainnames[terraintype],
                str(self.gameobjects[0].selectedtile))

class ScreenSection:
    """
    Abstract class for rendered objects. All objects that appear on screen must
    implement this class and redefine their own render method
    """
    def __init__(self, gd, coords):
        self.coords = coords
        self.gd = gd

    def render(self):
        """ Virtual method for rendered objects """
        raise NotImplementedError

class GameMap(ScreenSection):
    """
    Rendering object for the GameMap class. It will draw a tile according to the
    type of terrain in the data matrix.
    """
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
        """ Gets current value in the data matrix of the map. """
        return self.gamemap.matrix[coords[1]][coords[0]]

    def getselected(self):
        if self.selectedtile:
            x = self.selectedtile[0]
            y = self.selectedtile[1]
            return self.gamemap.matrix[y][x]

    def changeterrain(self, value):
        """  """
        x = self.selectedtile[0]
        y = self.selectedtile[1]
        self.gamemap.matrix[y][x] = value

class InfoBar(ScreenSection):
    """
    Rendered class for the information section on the right of the screen.
    It will display information of a selected tile.
    """
    def __init__(self, gd, height, coords):
        super(InfoBar, self).__init__(gd, coords)
        self.height = height

        # Info section
        self.selected = False
        self.color = (128, 128, 128)
        self.txtcolor = (255, 255, 255)

        # Text attributes
        self.font = pygame.font.Font(pixelfont, 12)
        self.texts = []

    def render(self):
        pygame.draw.rect(self.gd, self.color, (
            self.coords[0],
            self.coords[1],
            200,
            self.height
        ))

        if self.selected:
            for i, t in enumerate(self.texts):
                self.gd.blit(t, (self.coords[0] + 10, 20 * i + 10))

    def prepare(self, name, txtcoords):
        """
        Updates status of the info section. Information must not be displayed
        if a tile is not selected, or it must be updated if another tile is
        selected.
        """
        self.selected = True

        self.texts = [
            self.font.render('INFO ', True, self.txtcolor),
            self.font.render('Type: ' + name, True, self.txtcolor),
            self.font.render('Coords: ' + txtcoords, True, self.txtcolor)
        ]

    def reset(self):
        """
        Resets to default status when selection is deactivated.
        """
        self.selected = False
        self.texts = []
