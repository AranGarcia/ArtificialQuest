from . import constants

moves = constants.MoveDir
terrains = constants.Terrain

class Human:
    def __init__(self, name, gmap, pos):
        self.name = name
        self.gmap = gmap
        self.pos = pos

        self.explored = set([])

        self.look_around()

    def moveup(self):
        try:
            if self.gmap.matrix[self.pos[1] - 1][self.pos[0]] != terrains.WALL.value:
                self.pos[1] -= 1
        except IndexError:
            return False

        return True

    def movedown(self):
        try:
            if self.gmap.matrix[self.pos[1] + 1][self.pos[0]] != terrains.WALL.value:
                self.pos[1] += 1
        except IndexError:
            return False

        return True

    def moveright(self):
        try:
            if self.gmap.matrix[self.pos[1]][self.pos[0] + 1] != terrains.WALL.value:
                self.pos[0] += 1
        except IndexError:
            return False

        return True

    def moveleft(self):
        try:
            if self.gmap.matrix[self.pos[1]][self.pos[0] - 1] != terrains.WALL.value:
                self.pos[0] -= 1
        except IndexError:
            return False

        return True

    def look_around(self):
        limx = len(self.gmap.matrix[0])
        limy = len(self.gmap.matrix)

        # Look up
        if 0 <= self.pos[1] - 1:
            self.explored.add((self.pos[1] - 1, self.pos[0]))
        # Look down
        if self.pos[1] + 1 < limy:
            self.explored.add((self.pos[1] + 1, self.pos[0]))
        # Look left
        if 0 <= self.pos[0] - 1:
            self.explored.add((self.pos[1], self.pos[0] - 1))
        # Look right
        if self.pos[0] + 1 < limx:
            self.explored.add((self.pos[1], self.pos[0] + 1))
