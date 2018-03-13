from . import constants

moves = constants.MoveDir
terrains = constants.Terrain

class Human:
    def __init__(self, name, gmap, pos):
        self.name = name
        self.gmap = gmap
        self.pos = pos
        self.decisions = []
        self.explored = set([(pos[1], pos[0])])

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
        """
        Add surroundings to the explored set
        """
        limx = len(self.gmap.matrix[0])
        limy = len(self.gmap.matrix)

        x,y = self.pos[1], self.pos[0]
        count = 0

        self.explored.add((x, y))

        # Look up
        if (x - 1, y) not in self.explored and 0 <= x - 1:
            self.explored.add((x - 1, y))
            if self.terrain_walkable((x - 1, y)):
                count += 1
        # Look down
        if (x + 1, y) not in self.explored and x + 1 < limy:
            self.explored.add((x + 1, y))
            if self.terrain_walkable((x + 1, y)):
                count += 1
        # Look left
        if (x, y - 1) not in self.explored and 0 <= y - 1:
            self.explored.add((x, y - 1))
            if self.terrain_walkable((x, y - 1)):
                count += 1
        # Look right
        if (x, y + 1) not in self.explored and y + 1 < limx:
            self.explored.add((x, y + 1))
            if self.terrain_walkable((x, y + 1)):
                count += 1

        if count > 1:
            self.decisions.append((self.pos[1], self.pos[0]))

    def terrain_walkable(self, xy):
        return self.gmap.matrix[xy[0]][xy[1]] != terrains.WALL.value
