"""
Rendering module of the game. The main class Renderer handles various parts of
the screen and receives the events for them.
"""
import pygame
from questlogic import constants as const, heroes
from pygame.locals import *

TERRAINS = const.Terrain
PIXELFONT = \
    r'src/fonts/PressStart2P.ttf'
KPEVENTS = set(['0', '1', '2', '3', '4', '5', '6'])
ARROWEVENTS = set([273, 274, 275, 276])


class RendererProject:
    """ Manager of the objects to be rendered in the game. """

    def __init__(self, gamedisplay, gamemap, width, height):
        self.screen = gamedisplay
        self.width = width
        self.height = height

        # Rendered objects
        self.gameobjects = [
            GameMap(self.screen, (0, 0), gamemap),
            LogSection(self.screen, height - 48, (width - 300, 0)),
            BarButton(self.screen, width, (0, len(gamemap.matrix) * 48))
        ]

        # Attributes for blocking clicks and keyboard events
        self.keyboard_block = False
        self.block_start = False
        self.block_goal = False
        self.input_actions = []

        # Key event mapping to constants
        self.key_actions = {
            273: const.MoveDir.UP,
            274: const.MoveDir.DOWN,
            276: const.MoveDir.LEFT,
            275: const.MoveDir.RIGHT
        }

    def render(self):
        """
        Call the implemented render method on each overridden render object.
        """
        for gobj in self.gameobjects:
            gobj.render()

    def clicked(self, coords):
        """ Activates event on mouse click. """
        # Activate cursor if click was on the map
        if coords[0] < (self.width - 300) and coords[1] < (self.height - 48):
            tilecoords = ((coords[0] // 48), (coords[1] // 48))

            if self.block_start:
                self.block_start = False
                self.gameobjects[0].human.set_start(tilecoords)
                self.gameobjects[1].insert_log(
                    '>SET start: ' + str(tilecoords))
            elif self.block_goal:
                self.block_goal = False
                self.gameobjects[0].human.set_goal(tilecoords)
                self.gameobjects[1].insert_log('>SET goal: ' + str(tilecoords))
            else:
                if tilecoords != self.gameobjects[0].selectedtile:
                    # Selection cursor on map
                    self.gameobjects[0].selectedtile = tilecoords

                    # Info of the selected tile
                    terraintype = self.gameobjects[0].getterrain(tilecoords)
                    self.gameobjects[1].insert_log(
                        '>INFO: ' +
                        const.TERRAIN_NAMES[terraintype] +
                        ' ' + str(tilecoords)
                    )
                else:
                    # Deactivates cursor if clicked on same selected tile
                    self.gameobjects[0].selectedtile = None

        # Algorithm Buttons
        elif coords[1] > (self.height - 48):
            self.click_block = False
            self.gameobjects[0].selectedtile = None

            # Start algorithm using enhanced mode
            if coords[0] < (48):
                print ("Human")
            elif coords[0] < (48 * 2):
                print ("Monkey")
            elif coords[0] < (48 * 3):
                print ("Octopus")
            elif coords[0] < (48 * 4):
                print ("P")
            elif coords[0] < (48 * 5):
                print ("K")
            elif coords[0] < (48 * 6):
                print ("S")
            elif coords[0] < (48 * 7):
                print ("T")
            elif coords[0] < (48 * 8):
                print ("Star")

    def keypressed(self, event):
        """ Render on key press event. """

        if self.keyboard_block:
            if event.key in ARROWEVENTS:
                act = self.key_actions[event.key]
                if act not in self.input_actions:
                    self.input_actions.append(act)
                if len(self.input_actions) == 4:
                    self.keyboard_block = False
                    self.gameobjects[0].human.actions = self.input_actions
                    self.gameobjects[1].insert_log('>DONE receiving actions.')
                    self.gameobjects[1].insert_log(' Depth algorithm ready.')
            else:
                self.keyboard_block = False
                self.gameobjects[1].insert_log('>ERROR: use only arrows')
                self.gameobjects[1].insert_log(' to input directions.')
                self.gameobjects[2].selected_algorithm = None
                self.input_actions.clear()
        else:
            # Movement
            if event.key in ARROWEVENTS:
                self.gameobjects[0].movehero(event.key)

            # Terrain change
            elif self.gameobjects[0].selectedtile and event.unicode in KPEVENTS:
                self.gameobjects[0].changeterrain(int(event.unicode))
                terraintype = self.gameobjects[0].getselected()
                self.gameobjects[1].insert_log(
                    '>' + const.TERRAIN_NAMES[terraintype] +
                    ' ' + str(self.gameobjects[0].selectedtile) + ' CHANGED'
                )


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
            TERRAINS.MOUNTAIN.value: pygame.image.load('src/img/mountain.jpeg'),
            TERRAINS.LAND.value: pygame.image.load('src/img/land.png'),
            TERRAINS.WATER.value: pygame.image.load('src/img/water.png'),
            TERRAINS.SAND.value: pygame.image.load('src/img/sand.png'),
            TERRAINS.FOREST.value: pygame.image.load('src/img/forest.png')
        }

        # Map cursor
        # selectedtile -> (x,y)
        self.selectedtile = None
        self.selectimg = pygame.image.load('src/img/selectbox.png')

        # Decision indicator
        self.decisionimg = pygame.image.load('src/img/decision.png')

        # Character features
        self.human = None
        self.monkey = None
        self.octopus = None

        self.humanImg = pygame.image.load('src/img/human.png')
        self.monkeyImg = pygame.image.load('src/img/monkey.png')
        self.octopusImg = pygame.image.load('src/img/octopus.png')

    def render(self):
        """
        Implemented method of a ScreenSection that renders the map tiles,
        characters and the cursor
        """

        # NOTE:
        # When obtaining any info from the data matrix of the map, the Y
        # coordinates go first (e.g. matirx[y][x]).
        # On the other hand, when blitting coordinates are normal (e.g. (x,y))

        for r, row in enumerate(self.gamemap.matrix):
            for c, value in enumerate(row):
                self.screen.blit(self.landtiles[value], (c * 48, r * 48))

        # When they have positions
        if self.human != None:
            # Render human
            self.screen.blit(
                self.humanImg, (self.human.pos[0] * 48, self.human.pos[1] * 48))

            # Draw indicator where decisions where made
            for dcs in self.human.decisions:
                self.screen.blit(self.decisionimg, (dcs[0] * 48, dcs[1] * 48))
        if self.monkey != None:
            # Render monkey
            self.screen.blit(
                self.monkeyImg,
                (self.monkey.pos[0] * 48, self.monkey.pos[1] * 48))

            # Draw indicator where decisions where made
            for dcs in self.monkey.decisions:
                self.screen.blit(self.decisionimg, (dcs[0] * 48, dcs[1] * 48))
        if self.octopus != None:
            # Render octopus
            self.screen.blit(
                self.octopusImg,
                (self.octopus.pos[0] * 48, self.octopus.pos[1] * 48))

            # Draw indicator where decisions where made
            for dcs in self.octopus.decisions:
                self.screen.blit(self.decisionimg, (dcs[0] * 48, dcs[1] * 48))

        # If seleciton active, render cursor
        if self.selectedtile:
            self.screen.blit(
                self.selectimg,
                (self.selectedtile[0] * 48, self.selectedtile[1] * 48)
            )

    def getterrain(self, coords):
        """ Gets current value in the data matrix of the map. """
        return self.gamemap.matrix[coords[1]][coords[0]]

    def getselected(self):
        """
        Returns the tile that was clicked and now has the cursor tile upon it.
        """
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
        self.human.move(value)
        self.monkey.move(value)
        self.octopus.move(value)

class LogSection(ScreenSection):
    """
    Rendered class for the information section on the right of the screen.
    It will display information of a selected tile.
    """

    def __init__(self, gd, height, coords):
        super(LogSection, self).__init__(gd, coords)
        self.height = height

        # Info section
        self.color = (128, 128, 128)
        self.txtcolor = (255, 255, 255)

        # Text attributes
        self.font = pygame.font.Font(PIXELFONT, 12)
        self.max_log_size = (height - 10) // 20
        self.logs = []

    def render(self):
        pygame.draw.rect(self.screen, self.color, (
            self.coords[0],
            self.coords[1],
            300,
            self.height
        ))

        for i, t in enumerate(self.logs):
            self.screen.blit(t, (self.coords[0] + 10, 20 * i + 10))

    def insert_log(self, message):
        """
        Adds a line to the log on the LogSection
        """
        if len(self.logs) > self.max_log_size:
            self.logs.pop(0)

        self.logs.append(self.font.render(message, True, self.txtcolor))

    def reset_logs(self):
        """
        Resets to default status when selection is deactivated.
        """
        self.texts = []


class BarButton(ScreenSection):
    """
    Bar for Buttons and Actions (Start and Finish)
    """

    def __init__(self, gd, width, coords):
        super(BarButton, self).__init__(gd, coords)

        # Info section
        self.color = (80, 80, 80)
        self.width = width

        # Info button
        self.buttonHuman = pygame.image.load("src/img/human.png")
        self.buttonMonkey = pygame.image.load("src/img/monkey.png")
        self.buttonOctopus = pygame.image.load("src/img/octopus.png")
        self.buttonStar = pygame.image.load("src/img/star.png")
        self.buttonP = pygame.image.load("src/img/letterP.png")
        self.buttonK = pygame.image.load("src/img/letterK.png")
        self.buttonS = pygame.image.load("src/img/letterS.png")
        self.buttonT = pygame.image.load("src/img/letterT.png")


    def render(self):
        pygame.draw.rect(self.screen, self.color, (
            self.coords[0],
            self.coords[1],
            self.width,
            48
        ))

        # Position of characters
        self.screen.blit(self.buttonHuman, (self.coords[0], self.coords[1]))
        self.screen.blit(
            self.buttonMonkey, (self.coords[0] + 48, self.coords[1]))
        self.screen.blit(
            self.buttonOctopus, (self.coords[0] + 48 * 2, self.coords[1]))

        # Game's features
        self.screen.blit(
            self.buttonP, (self.coords[0] + 48 * 3, self.coords[1]))
        self.screen.blit(
            self.buttonK, (self.coords[0] + 48 * 4, self.coords[1]))
        self.screen.blit(
            self.buttonS, (self.coords[0] + 48 * 5, self.coords[1]))
        self.screen.blit(
            self.buttonT, (self.coords[0] + 48 * 6, self.coords[1]))

        # Algorithm A*
        self.screen.blit(
        self.buttonStar, (self.coords[0] + 48 * 7, self.coords[1]))