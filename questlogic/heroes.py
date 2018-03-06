from . import constants

moves = constants.MoveDir
terrains = constants.Terrain

class Human:
    def __init__(self, name, gmap, pos):
        self.name = name
        self.gmap = gmap
        self.pos = pos

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

if __name__ == '__main__':
    print(constants.MoveDir.UP.value)
