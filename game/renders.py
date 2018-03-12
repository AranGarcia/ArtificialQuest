"""
Rendering module of the game. The main class Renderer handles various parts of
the screen and receives the events for them.
"""
import pygame
from questlogic import constants, heroes

TERRAINS = constants.Terrain
PIXELFONT = \
    r'src/fonts/PressStart2P.ttf'
KPEVENTS = set(['0', '1', '2', '3', '4', '5', '6'])
ARROWEVENTS = set([273, 274, 275, 276])


class Renderer:
    """ Manager of the objects to be rendered in the game """

    def __init__(self, gamedisplay, gamemap, width, height):
        self.screen = gamedisplay
        self.width = width
        self.height = height

        # Rendered objects
        self.gameobjects = [
            GameMap(self.screen, (0, 0), gamemap),
            InfoBar(self.screen, height, (width - 200, 0))
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
                self.gameobjects[1].prepare(
                    constants.terrainnames[terraintype], str(tilecoords))
            else:
                # Deactivates cursor if clicked on same selected tile
                self.gameobjects[0].selectedtile = None
                self.gameobjects[1].reset()

        # Deactivates cursor with click off map
        else:
            self.gameobjects[0].selectedtile = None
            self.gameobjects[1].reset()

    def keypressed(self, event):
        """ Render on key press event. """
        # Movement
        if event.key in ARROWEVENTS:
            self.gameobjects[0].movehero(event.key)

        # Terrain change
        elif self.gameobjects[1].selected and event.unicode in KPEVENTS:
            self.gameobjects[0].changeterrain(int(event.unicode))
            terraintype = self.gameobjects[0].getselected()
            self.gameobjects[1].prepare(constants.terrainnames[terraintype],
                                        str(self.gameobjects[0].selectedtile))


class ScreenSection:
    """
    Abstract class for rendered objects. All objects that appear on screen must
    implement this class and redefine their own render method
    """

    def __init__(self, screen, coords):
        self.coords = coords
        self.screen = screen

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
            TERRAINS.WALL.value: pygame.image.load('src/img/wall.png'),
            TERRAINS.ROAD.value: pygame.image.load('src/img/road.png'),
            TERRAINS.MOUNTAIN.value: pygame.image.load('src/img/mountain.png'),
            TERRAINS.LAND.value: pygame.image.load('src/img/land.png'),
            TERRAINS.WATER.value: pygame.image.load('src/img/water.png'),
            TERRAINS.SAND.value: pygame.image.load('src/img/sand.png'),
            TERRAINS.FOREST.value: pygame.image.load('src/img/forest.png')
        }

        # Map cursor
        # selectedtile -> (x,y)
        self.selectedtile = None
        self.selectimg = pygame.image.load('src/img/selectbox.png')

        # Hero position
        # heropos -> (x,y)

        self.hero = heroes.Human('Isildur',
                                 gamemap, self.__set_hero_pos(gamemap))
        self.heroimg = pygame.image.load('src/img/hero.png')

    def render(self):
        # Fog of war
        self.screen.fill((0, 0, 0))

        # Render only explored parts of the map
        for exp in self.hero.explored:
            terr = self.gamemap.matrix[exp[0]][exp[1]]
            self.screen.blit(self.landtiles[terr], (exp[1] * 48, exp[0] * 48))

        # Render hero
        self.screen.blit(
            self.heroimg, (self.hero.pos[0] * 48, self.hero.pos[1] * 48))

        # If seleciton active, render cursor
        if self.selectedtile:
            self.screen.blit(
                self.selectimg, (self.selectedtile[0] * 48, self.selectedtile[1] * 48))

    def getterrain(self, coords):
        """ Gets current value in the data matrix of the map. """
        return self.gamemap.matrix[coords[1]][coords[0]]

    def getselected(self):
        if self.selectedtile:
            x = self.selectedtile[0]
            y = self.selectedtile[1]
            return self.gamemap.matrix[y][x]

    def changeterrain(self, value):
        """ Changes the terrain selected by the cursor on the map """
        x = self.selectedtile[0]
        y = self.selectedtile[1]
        self.gamemap.matrix[y][x] = value

    def movehero(self, value):
        # Move up
        if value == 273:
            self.hero.moveup()
        # Move down
        elif value == 274:
            self.hero.movedown()
        # Move right
        elif value == 275:
            self.hero.moveright()
        # Move left
        elif value == 276:
            self.hero.moveleft()

        self.hero.look_around()

    def __set_hero_pos(self, gmap):
        numrows = len(gmap.matrix)
        numcols = len(gmap.matrix[0])

        for i in range(numcols):
            for j in range(numrows):
                if gmap.matrix[j][i] != TERRAINS.WALL.value:
                    return [i, j]
        return None


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
        self.font = pygame.font.Font(PIXELFONT, 12)
        self.texts = []

    def render(self):
        pygame.draw.rect(self.screen, self.color, (
            self.coords[0],
            self.coords[1],
            200,
            self.height
        ))

        if self.selected:
            for i, t in enumerate(self.texts):
                self.screen.blit(t, (self.coords[0] + 10, 20 * i + 10))

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
