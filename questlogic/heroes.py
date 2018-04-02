from constants import MoveDir, Terrain
import ai


class Hero:
    """docstring for Hero."""

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
            if self.gmap.matrix[self.pos[1] - 1][self.pos[0]] != Terrain.WALL.value:
                self.pos[1] -= 1
        except IndexError:
            return False

        return True

    def __movedown(self):
        try:
            if self.gmap.matrix[self.pos[1] + 1][self.pos[0]] != Terrain.WALL.value:
                self.pos[1] += 1
        except IndexError:
            return False

        return True

    def __moveright(self):
        try:
            if self.gmap.matrix[self.pos[1]][self.pos[0] + 1] != Terrain.WALL.value:
                self.pos[0] += 1
        except IndexError:
            return False

        return True

    def __moveleft(self):
        try:
            if self.gmap.matrix[self.pos[1]][self.pos[0] - 1] != Terrain.WALL.value:
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

        x, y = self.pos[0], self.pos[1]
        count = 0

        self.explored.add((x, y))
        w = self.gmap.get_walkable(self.pos)

        # Look up
        if (x, y - 1) not in self.explored and 0 <= y - 1:
            self.explored.add((x, y - 1))
        # Look down
        if (x, y + 1) not in self.explored and y + 1 < limy:
            self.explored.add((x, y + 1))
        # Look left
        if (x - 1, y) not in self.explored and 0 <= x - 1:
            self.explored.add((x - 1, y))
        # Look right
        if (x + 1, y) not in self.explored and x + 1 < limx:
            self.explored.add((x + 1, y))

        if len(w) > 2:
            self.decisions.append((self.pos[0], self.pos[1]))


class Human(Hero):
    def __init__(self, name, gmap, pos):
        super(Human, self).__init__(name, gmap, pos)

        # TODO: Generate the movement costs specific to each being.
