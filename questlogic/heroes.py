from . import constants

moves = constants.MoveDir
terrains = constants.Terrain

class Human:
    """
    Basic character class that explores and walks upon a map
    """
    def __init__(self, name, gmap, pos):
        self.name = name
        self.gmap = gmap
        self.pos = pos
        self.decisions = []
        self.explored = set([(pos[0], pos[1])])

        # The indexes are the values returned by key pressing events from pygame
        self.movements = {
            273: self.__moveup,
            274: self.__movedown,
            276: self.__moveleft,
            275: self.__moveright
        }

        # Initialize the explored set with the current position
        self.look_around()

    def move(self, direction):
        """
        Method called by the game renderer when a key-press event is triggered
        and the display updates the position of the character.
        """
        
        return self.movements[direction]()

    def __moveup(self):
        try:
            if self.gmap.matrix[self.pos[1] - 1][self.pos[0]] != terrains.WALL.value:
                self.pos[1] -= 1
        except IndexError:
            return False

        return True

    def __movedown(self):
        try:
            if self.gmap.matrix[self.pos[1] + 1][self.pos[0]] != terrains.WALL.value:
                self.pos[1] += 1
        except IndexError:
            return False

        return True

    def __moveright(self):
        try:
            if self.gmap.matrix[self.pos[1]][self.pos[0] + 1] != terrains.WALL.value:
                self.pos[0] += 1
        except IndexError:
            return False

        return True

    def __moveleft(self):
        try:
            if self.gmap.matrix[self.pos[1]][self.pos[0] - 1] != terrains.WALL.value:
                self.pos[0] -= 1
        except IndexError:
            return False

        return True

    def look_around(self):
        """
        Add surroundings to the explored set
        """
        limx = len(self.gmap.matrix[0])
        limy = len(self.gmap.matrix)

        x,y = self.pos[0], self.pos[1]
        count = 0

        self.explored.add((x, y))

        # Look left
        if (x - 1, y) not in self.explored and 0 <= x - 1:
            self.explored.add((x - 1, y))
            if self.__terrain_walkable((x - 1, y)):
                count += 1
        # Look right
        if (x + 1, y) not in self.explored and x + 1 < limx:
            self.explored.add((x + 1, y))
            if self.__terrain_walkable((x + 1, y)):
                count += 1
        # Look up
        if (x, y - 1) not in self.explored and 0 <= y - 1:
            self.explored.add((x, y - 1))
            if self.__terrain_walkable((x, y - 1)):
                count += 1
        # Look down
        if (x, y + 1) not in self.explored and y + 1 < limy:
            self.explored.add((x, y + 1))
            if self.__terrain_walkable((x, y + 1)):
                count += 1

        if count > 1:
            self.decisions.append((self.pos[0], self.pos[1]))

    def __terrain_walkable(self, xy):
        """
        terrain_walkable((x, y)) -> boolean

        Explores which of the surroundings is not a wall.
        """
        return self.gmap.matrix[xy[1]][xy[0]] != terrains.WALL.value
