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
    """ Manager of the objects to be rendered in the game. """

    def __init__(self, gamedisplay, gamemap, width, height):
        self.screen = gamedisplay
        self.width = width
        self.height = height

        # Rendered objects
        self.gameobjects = [
            GameMap(self.screen, (0, 0), gamemap),
            InfoBar(self.screen, height, (width - 200, 0)),
            BarButton(self.screen, width, (0, len(gamemap.matrix)*48))
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
        if coords[0] < (self.width - 200) and coords[1] < (self.height - 48):
            tilecoords = ((coords[0] // 48), (coords[1] // 48))
            if tilecoords != self.gameobjects[0].selectedtile:
                # Selection cursor on map
                self.gameobjects[0].selectedtile = tilecoords

                # Info of the selected tile
                terraintype = self.gameobjects[0].getterrain(tilecoords)
                self.gameobjects[1].prepare(
                    constants.TERRAIN_NAMES[terraintype], str(tilecoords))
            else:
                # Deactivates cursor if clicked on same selected tile
                self.gameobjects[0].selectedtile = None
                self.gameobjects[1].reset()
        elif coords[1] > (self.height - 48):
            if coords[0] < (48):
                print ("RunAll")
            elif coords[0] < (48*2):
                print ("StepByStep")
            elif coords[0] < (48*3):
                print ("Start")
                self.gameobjects[0].hero.pos= \
                    self.gameobjects[0].putStart(coords, (self.width,self.height))

                self.gameobjects[0].hero.explored= \
                    set([(self.gameobjects[0].hero.pos[0],
                          self.gameobjects[0].hero.pos[1])])
            elif coords[0] < (48*4):
                print ("End")
                self.gameobjects[0].putEnd(coords, (self.width,self.height))
            elif coords[0] < (48*5):
                print ("Algoritmo 1")
                self.__changedImg()
                self.gameobjects[2].algo[0]= True
            elif coords[0] < (48*6):
                print ("Algoritmo 2")
                self.__changedImg()
                self.gameobjects[2].algo[1]= True
            elif coords[0] < (48*7):
                print ("Algoritmo 3")
                self.__changedImg()
                self.gameobjects[2].algo[2]= True

        # Deactivates cursor with click off map
        else:
            self.gameobjects[0].selectedtile = None
            self.gameobjects[1].reset()

    def __changedImg(self):
        # for val in self.gameobjects[2].algo:
        #     val= False
        self.gameobjects[2].algo[0]= False
        self.gameobjects[2].algo[1]= False
        self.gameobjects[2].algo[2]= False


    def keypressed(self, event):
        """ Render on key press event. """
        # Movement
        if self.gameobjects[0].flagMap[0] and self.gameobjects[0].flagMap[1]:
            if event.key in ARROWEVENTS:
                self.gameobjects[0].movehero(event.key)

                # Terrain change
            elif self.gameobjects[1].selected and event.unicode in KPEVENTS:
                self.gameobjects[0].changeterrain(int(event.unicode))
                terraintype = self.gameobjects[0].getselected()
                self.gameobjects[1].prepare(constants.TERRAIN_NAMES[terraintype],
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

        # Decision indicator
        self.decisionimg = pygame.image.load('src/img/decision.png')
        # Hero position
        # heropos -> (x,y)
        self.hero = heroes.Human(
            'Isildur',
            gamemap,
            (0,0)
        )
        self.heroimg = pygame.image.load('src/img/hero.png')

        # Imagen Mouse
        self.imgMouseStart= pygame.image.load("src/img/ButtonStart.png")
        self.imgMouseEnd= pygame.image.load("src/img/ButtonEnd.png")

        #Flag ButtonStart and ButtonEnd Pos1= start, Pos2= end
        self.flagMap= [False, False]

    def render(self):
        """
        Implemented method of a ScreenSection that renders the map tiles,
        characters and the cursor
        """

        # NOTE:
        # When obtaining any info from the data matrix of the map, the Y
        # coordinates go first (e.g. matirx[y][x]).
        # On the other hand, when blitting coordinates are normal (e.g. (x,y))

        # Si no estan los puntos de meta y fin no se activa la niebla.
        if not (self.flagMap[0] and self.flagMap[1]):
            # Render map as background
            for r, row in enumerate(self.gamemap.matrix):
                for c, value in enumerate(row):
                    self.screen.blit(self.landtiles[value], (c * 48, r * 48))

        else:
            # Fog of war
            self.screen.fill((0, 0, 0))

            # Render only explored parts of the map
            for exp in self.hero.explored:
                terr = self.gamemap.matrix[exp[1]][exp[0]]
                self.screen.blit(self.landtiles[terr], (exp[0] * 48, exp[1] * 48))

        # Draw indicator where decisions where made
        for dcs in self.hero.decisions:
            self.screen.blit(self.decisionimg, (dcs[0] * 48, dcs[1] * 48))

        # Render hero
        if self.flagMap[0] and self.flagMap[1]:

            self.screen.blit(
                self.heroimg, (self.hero.pos[0] * 48, self.hero.pos[1] * 48))

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
        self.hero.move(value)

        self.hero.look_around()

    def __set_hero_pos(self, gmap):
        """
        set_hero_pos(GameMap) -> (x, y)

        Looks for the leftmost walkable tile on which to place the hero. If None
        is returned, then there is no available place for the hero to be placed.
        """
        numrows = len(gmap.matrix)
        numcols = len(gmap.matrix[0])

        for i in range(numcols):
            for j in range(numrows):
                if gmap.matrix[j][i] != TERRAINS.WALL.value:
                    return [i, j]
        return None

    def putStart(self, coords, size):
        """
        Poner el punto de inicio en el mapa.
        """
        print ("putStart")

        self.flagMap[0]= False
        while not self.flagMap[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Activate cursor if click was on the map
                    coordsAux= event.pos
                    if coordsAux[0] < (size[0] - 200) and coordsAux[1] < (size[1] - 48):
                        print (coordsAux, "ButtonStart", self.flagMap)
                        self.flagMap[0]= True
                        print ((coordsAux[0] // 48, coordsAux[1] // 48))
        return (coordsAux[0] // 48, coordsAux[1] // 48)


    def putEnd(self, coords, size):
        """
        Poner la meta en el mapa.
        """
        print ("putEnd")

        self.flagMap[1]= False
        while not self.flagMap[1]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Activate cursor if click was on the map
                    coordsAux= event.pos
                    if coordsAux[0] < (size[0] - 200) and coordsAux[1] < (size[1] - 48):
                        print (coordsAux, "ButtonEnd")
                        self.flagMap[1]= True
                        print ((coordsAux[0] // 48, coordsAux[1] // 48))
        return (coordsAux[0] // 48, coordsAux[1] // 48)


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

class BarButton(ScreenSection):
    """
    Bar for Buttons and Actions (Start and Finish)
    """

    def __init__(self, gd, width, coords):
        super(BarButton, self).__init__(gd, coords)

        # Info section
        self.selected = False
        self.color = (80, 80, 80)
        self.txtcolor = (255, 255, 255)
        self.width= width

        # Text attributes
        self.font = pygame.font.Font(PIXELFONT, 12)
        self.texts = []

        # Info button
        self.buttonStep= pygame.image.load("src/img/ButtonStep.png")
        self.buttonAll= pygame.image.load("src/img/ButtonAll.png")
        self.buttonStart= pygame.image.load("src/img/ButtonStart.png")
        self.buttonEnd= pygame.image.load("src/img/ButtonEnd.png")

        # # Buttons Algoritmos
        self.algo= [False, False, False]

        self.algo1a= pygame.image.load("src/img/algo1a.png")
        self.algo2a= pygame.image.load("src/img/algo2a.png")
        self.algo3a= pygame.image.load("src/img/algo3a.png")

        self.algo1b= pygame.image.load("src/img/algo1b.png")
        self.algo2b= pygame.image.load("src/img/algo2b.png")
        self.algo3b= pygame.image.load("src/img/algo3b.png")

    def render(self):
        pygame.draw.rect(self.screen, self.color, (
            self.coords[0],
            self.coords[1],
            self.width,
            48
        ))


        self.screen.blit(self.buttonAll,(self.coords[0],self.coords[1]))
        self.screen.blit(self.buttonStep,(self.coords[0]+48,self.coords[1]))
        self.screen.blit(self.buttonStart,(self.coords[0]+48*2,self.coords[1]))
        self.screen.blit(self.buttonEnd,(self.coords[0]+48*3,self.coords[1]))

        if not self.algo[0]:
            self.screen.blit(self.algo1a,(self.coords[0]+48*4,self.coords[1]))
        else:
            self.screen.blit(self.algo1b,(self.coords[0]+48*4,self.coords[1]))

        if not self.algo[1]:
            self.screen.blit(self.algo2a,(self.coords[0]+48*5,self.coords[1]))
        else:
            self.screen.blit(self.algo2b,(self.coords[0]+48*5,self.coords[1]))

        if not self.algo[2]:
            self.screen.blit(self.algo3a,(self.coords[0]+48*6,self.coords[1]))
        else:
            self.screen.blit(self.algo3b,(self.coords[0]+48*6,self.coords[1]))
