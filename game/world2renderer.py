"""
Rendering module of the game. The main class Renderer handles various parts of
the screen and receives the events for them.
"""
import pygame
import pygame.locals
import time
from questlogic import constants as const, heroes

TERRAINS = const.Terrain
PIXELFONT = \
    r'src/fonts/PressStart2P.ttf'
KPEVENTS = set(['0', '1', '2', '3', '4', '5', '6'])
ARROWEVENTS = set([273, 274, 275, 276])


class World2Renderer:
    """ Manager of the objects to be rendered in the game. """

    def __init__(self, gamedisplay, gamemap, width, height):
        self.screen = gamedisplay
        self.width = width
        self.height = height
        self.gamemap = gamemap

        # Rendered objects
        self.gameobjects = [
            GameMap(self.screen, (0, 0), self.gamemap),
            LogSection(self.screen, height - 48, (width - 300, 0)),
            ButtonSection(self.screen, width, (0, len(gamemap.matrix) * 48))
        ]

        # Attributes for blocking clicks and keyboard events
        self.keyboard_block = False
        self.block_start = 0
        self.input_actions = []
        self.flagStone = 0

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
            tilecoordsImgs = ((coords[0]), (coords[1]))

            # Setting hero or objective on map
            if self.block_start >= 0:
                # Human
                if self.block_start == 0:
                    human = heroes.Human(
                        const.Heroes.HUMAN, self.gamemap, list(tilecoords))
                    human.set_start(tilecoords)

                    if not const.Heroes.HUMAN.value in self.gameobjects[0].selected_heroes:
                        self.gameobjects[0].heroes.append(human)
                        self.gameobjects[0].selected_heroes.add(
                            const.Heroes.HUMAN.value)

                    self.gameobjects[1].insert_log(
                        '>SET human: ' + str(tilecoords))

                # Monkey
                elif self.block_start == 1:
                    monkey = heroes.Monkey(
                        const.Heroes.MONKEY, self.gamemap, list(tilecoords))
                    monkey.set_start(tilecoords)

                    if not const.Heroes.MONKEY.value in self.gameobjects[0].selected_heroes:
                        self.gameobjects[0].heroes.append(monkey)
                        self.gameobjects[0].selected_heroes.add(
                            const.Heroes.MONKEY.value)

                    self.gameobjects[1].insert_log(
                        '>SET monkey: ' + str(tilecoords))

                # Octopus
                elif self.block_start == 2:
                    octopus = heroes.Octopus(
                        const.Heroes.OCTOPUS, self.gamemap, list(tilecoords))
                    octopus.set_start(tilecoords)

                    if not const.Heroes.OCTOPUS.value in self.gameobjects[0].selected_heroes:
                        self.gameobjects[0].heroes.append(octopus)
                        self.gameobjects[0].selected_heroes.add(
                            const.Heroes.OCTOPUS.value)

                    self.gameobjects[1].insert_log(
                        '>SET octopus: ' + str(tilecoords))

                # Crocodile
                elif self.block_start == 3:
                    crocodile = heroes.Crocodile(
                        const.Heroes.CROCODILE, self.gamemap, list(tilecoords))
                    crocodile.set_start(tilecoords)

                    if not const.Heroes.CROCODILE.value in self.gameobjects[0].selected_heroes:
                        self.gameobjects[0].heroes.append(crocodile)
                        self.gameobjects[0].selected_heroes.add(
                            const.Heroes.CROCODILE.value)

                    self.gameobjects[1].insert_log(
                        '>SET crocodile: ' + str(tilecoords))

                # Sasquatch
                elif self.block_start == 4:
                    sasquatch = heroes.Sasquatch(
                        const.Heroes.SASQUATCH, self.gamemap, list(tilecoords))
                    sasquatch.set_start(tilecoords)

                    if not const.Heroes.SASQUATCH.value in self.gameobjects[0].selected_heroes:
                        self.gameobjects[0].heroes.append(sasquatch)
                        self.gameobjects[0].selected_heroes.add(
                            const.Heroes.SASQUATCH.value)

                    self.gameobjects[1].insert_log(
                        '>SET sasquatch: ' + str(tilecoords))

                # Werewolf
                elif self.block_start == 5:
                    werewolf = heroes.Werewolf(
                        const.Heroes.WEREWOLF, self.gamemap, list(tilecoords))
                    werewolf.set_start(tilecoords)

                    if not const.Heroes.WEREWOLF.value in self.gameobjects[0].selected_heroes:
                        self.gameobjects[0].heroes.append(werewolf)
                        self.gameobjects[0].selected_heroes.add(
                            const.Heroes.WEREWOLF.value)

                    self.gameobjects[1].insert_log(
                        '>SET werewolf: ' + str(tilecoords))

                # Entrance
                elif self.block_start == 6:
                    self.gameobjects[0].entrances.append(tilecoords)

                    if len(self.gameobjects[0].entrances) > 3:
                        self.gameobjects[0].entrances.pop(0)

                    self.gameobjects[1].insert_log(
                        '>SET Entrance: ' + str(tilecoords))

                # Portal
                elif self.block_start == 7:
                    self.gameobjects[0].portal_pos = tilecoords
                    self.gameobjects[1].insert_log(
                        '>SET Portal: ' + str(tilecoords))

                # Key
                elif self.block_start == 8:
                    self.gameobjects[0].key_pos = tilecoords
                    self.gameobjects[1].insert_log(
                        '>SET Key: ' + str(tilecoords))

                # Stones
                elif self.block_start == 9:
                    self.gameobjects[0].stone_pos = tilecoords
                    self.gameobjects[1].insert_log(
                        '>SET Stones: ' + str(tilecoords))

                # Temple
                elif self.block_start == 10:
                    self.gameobjects[0].temple_pos = tilecoords
                    self.gameobjects[1].insert_log(
                        '>SET Temple: ' + str(tilecoords))

                #  Friend
                elif self.block_start == 11:
                    self.gameobjects[0].friend_pos = tilecoords
                    self.gameobjects[1].insert_log(
                        '>SET Friend: ' + str(tilecoords))

                # Verify that only three heroes have been chosen
                if len(self.gameobjects[0].heroes) > 3:
                    ht = self.gameobjects[0].heroes.pop(0)
                    self.gameobjects[0].selected_heroes.remove(
                        ht.species.value)

                self.block_start = -1
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

        # Button section
        elif coords[1] > (self.height - 48):
            self.gameobjects[0].selectedtile = None

            self.block_start = (coords[0] // 48)

            # Start algorithm
            if self.block_start == 12:
                if len(self.gameobjects[0].entrances) < 3:
                    self.gameobjects[1].insert_log('>STARTS missing on map.')
                    self.gameobjects[1].insert_log(
                        ' Only ' + str(len(self.gameobjects[0].entrances)) + ' set.')

                goals = {
                    'KEY': self.gameobjects[0].key_pos,
                    'STONES': self.gameobjects[0].stone_pos,
                    'TEMPLE': self.gameobjects[0].temple_pos,
                    'PORTAL': self.gameobjects[0].portal_pos,
                    'FRIEND': self.gameobjects[0].friend_pos
                }

                if not goals['KEY'] or not goals['TEMPLE'] or \
                        not goals['STONES'] or not goals['PORTAL'] or not goals['FRIEND']:
                    self.gameobjects[1].insert_log('>ITEMS missing on map.')
                    self.gameobjects[1].insert_log(
                        ' Only ' + str(len([g for g in goals.values() if g is not None])) + ' set.')

                elif len(self.gameobjects[0].heroes) < 3:
                    self.gameobjects[1].insert_log('>ITEMS missing on map.')
                    self.gameobjects[1].insert_log(
                        ' Only ' + str(len(self.gameobjects[0].heroes)) + ' are set.')

                # Everything should be set to start the genetic algorithm
                else:
                    heroes.use_genetic_search(
                        self.gameobjects[0].heroes, self.gameobjects[0].entrances, goals)
                self.block_start = -1

            # Game reset
            elif self.block_start == 13:
                self.gameobjects = [
                    GameMap(self.screen, (0, 0), self.gamemap),
                    LogSection(self.screen, self.height -
                               48, (self.width - 300, 0)),
                    ButtonSection(self.screen, self.width,
                                  (0, len(self.gamemap.matrix) * 48))
                ]
                self.block_start = -1

    def keypressed(self, event):
        """ Render on key press event. """

        if self.gameobjects[0].selectedtile and event.unicode in KPEVENTS:
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
        """ Virtual method for renderable objects """
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
            TERRAINS.FOREST.value: pygame.image.load('src/img/forest.png'),
            TERRAINS.SWAMP.value: pygame.image.load('src/img/swamp.png'),
            TERRAINS.SNOW.value: pygame.image.load('src/img/snow.png')
        }

        # Map cursor
        # selectedtile -> (x,y)
        self.selectedtile = None
        self.selectimg = pygame.image.load('src/img/selectbox.png')

        # Decision indicator
        self.decisionimg = pygame.image.load('src/img/decision.png')

        # Character instances
        self.heroes = []
        self.selected_heroes = set()

        # Heroes
        self.hero_imgs = {
            const.Heroes.HUMAN.value: pygame.image.load('src/img/human.png'),
            const.Heroes.MONKEY.value: pygame.image.load('src/img/monkey.png'),
            const.Heroes.OCTOPUS.value: pygame.image.load('src/img/octopus.png'),
            const.Heroes.CROCODILE.value: pygame.image.load('src/img/crocodile.png'),
            const.Heroes.SASQUATCH.value: pygame.image.load("src/img/sasquatch.png"),
            const.Heroes.WEREWOLF.value: pygame.image.load("src/img/werewolf.png")
        }
        # Other buttons
        self.starImg = pygame.image.load("src/img/star.png")
        self.eImg = pygame.image.load("src/img/entrance.png")
        self.pImg = pygame.image.load("src/img/portal.png")
        self.kImg = pygame.image.load("src/img/key.png")
        self.sImg = pygame.image.load("src/img/stones.png")
        self.tImg = pygame.image.load("src/img/temple.png")
        self.fImg = pygame.image.load("src/img/friend.png")

        # Block for don't print images
        self.blockImg = True

        # Item positions
        self.entrances = []
        self.portal_pos = None
        self.key_pos = None
        self.stone_pos = None
        self.temple_pos = None
        self.friend_pos = None

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

        # Render Items when they have positions
        for e in self.entrances:
            self.screen.blit(self.eImg, (e[0] * 48, e[1] * 48))

        if self.portal_pos:
            self.screen.blit(
                self.pImg, (self.portal_pos[0] * 48, self.portal_pos[1] * 48))

        if self.key_pos:
            self.screen.blit(
                self.kImg, (self.key_pos[0] * 48, self.key_pos[1] * 48))

        if self.stone_pos:
            self.screen.blit(
                self.sImg, (self.stone_pos[0] * 48, self.stone_pos[1] * 48))

        if self.temple_pos:
            self.screen.blit(
                self.tImg, (self.temple_pos[0] * 48, self.temple_pos[1] * 48))

        if self.friend_pos:
            self.screen.blit(
                self.fImg, (self.friend_pos[0] * 48, self.friend_pos[1] * 48))

        for h in self.heroes:
            self.screen.blit(
                self.hero_imgs[h.species.value], (h.pos[0] * 48, h.pos[1] * 48))

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

    # TODO: Apply the method to selected heroes selecte
    def movehero(self, value):
        pass
        # self.human.move(value)
        # self.monkey.move(value)
        # self.octopus.move(value)


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


class ButtonSection(ScreenSection):
    """
    Buttons section
    """

    def __init__(self, gd, width, coords):
        super(ButtonSection, self).__init__(gd, coords)

        # Info section
        self.color = (80, 80, 80)
        self.width = width

        # Info button
        self.buttonHuman = pygame.image.load("src/img/human.png")
        self.buttonMonkey = pygame.image.load("src/img/monkey.png")
        self.buttonOctopus = pygame.image.load("src/img/octopus.png")
        self.buttonCroc = pygame.image.load("src/img/crocodile.png")
        self.buttonSasq = pygame.image.load("src/img/sasquatch.png")
        self.buttonWolf = pygame.image.load("src/img/werewolf.png")
        self.buttonEntrance = pygame.image.load("src/img/entrance.png")
        self.buttonPortal = pygame.image.load("src/img/portal.png")
        self.buttonKey = pygame.image.load("src/img/key.png")
        self.buttonStones = pygame.image.load("src/img/stones.png")
        self.buttonTemple = pygame.image.load("src/img/temple.png")
        self.buttonFriend = pygame.image.load("src/img/friend.png")
        self.buttonStar = pygame.image.load("src/img/star.png")
        self.buttonRestart = pygame.image.load("src/img/restart.png")

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
        self.screen.blit(
            self.buttonCroc, (self.coords[0] + 48 * 3, self.coords[1]))
        self.screen.blit(
            self.buttonSasq, (self.coords[0] + 48 * 4, self.coords[1]))
        self.screen.blit(
            self.buttonWolf, (self.coords[0] + 48 * 5, self.coords[1]))

        # Objectives
        self.screen.blit(
            self.buttonEntrance, (self.coords[0] + 48 * 6, self.coords[1]))
        self.screen.blit(
            self.buttonPortal, (self.coords[0] + 48 * 7, self.coords[1]))
        self.screen.blit(
            self.buttonKey, (self.coords[0] + 48 * 8, self.coords[1]))
        self.screen.blit(
            self.buttonStones, (self.coords[0] + 48 * 9, self.coords[1]))
        self.screen.blit(
            self.buttonTemple, (self.coords[0] + 48 * 10, self.coords[1]))
        self.screen.blit(
            self.buttonFriend, (self.coords[0] + 48 * 11, self.coords[1]))

        # Start search
        self.screen.blit(
            self.buttonStar, (self.coords[0] + 48 * 12, self.coords[1]))

        # Reset GameMap
        self.screen.blit(
            self.buttonRestart, (self.coords[0] + 48 * 13, self.coords[1]))
