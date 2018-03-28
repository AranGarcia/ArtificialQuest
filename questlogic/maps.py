import random
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

import constants


class Map:
    '''
    Map represented by data loaded from a file.

    The file must contain integers separated by spaces. Each line will consist of a row in the map,
    and the row with most columns will define the width of the map (zeroes will be filled in the
    rows to make the matrix rectangular). Each digit must correspond to a terrain.|
    '''

    def __init__(self, fname=''):
        self.fname = fname
        self.matrix = []

        if fname:
            self.load(fname)

    def load(self, fname):
        '''
        Loads data from a file into the map matrix.
        '''
        with open(fname) as fdata:
            lines = fdata.readlines()

        self.matrix = []
        for index, line in enumerate(lines):
            self.matrix.append([])

            for digit in line.split():
                value = int(digit)

                # Treat invalid values as 0 (as a wall)
                if not value in constants.validterrains:
                    self.matrix[index].append(0)
                else:
                    self.matrix[index].append(value)

        # If matrix is not rectangular, add the columns to the rows that are short
        rowsize = lambda l: len(l)

        longest = max(rowsize(i) for i in self.matrix)

        for n, r in enumerate(self.matrix):
            if len(r) < longest:
                r.extend([0 for i in range(longest - len(r))])

    def randomize(self, rows=10, columns=10):
        ''' Create a matrix with random numbers for the terrain types. '''
        self.matrix = [
            [random.randint(0, 1) for i in range(columns)]
            for j in range(rows)
        ]

    def get_walkable(self, coord):
        """
        Returns a list of coordinates where the hero can move from its current
        position (i.e., places where there isn't a wall).
        """
        walkable = []

        # Up
        if self.is_walkable((coord[0], coord[1] - 1)):
            walkable.append((coord[0], coord[1] - 1))
        # Down
        if self.is_walkable((coord[0], coord[1] + 1)):
            walkable.append((coord[0], coord[1] + 1))
        # Left
        if self.is_walkable((coord[0] - 1, coord[1])):
            walkable.append((coord[0] - 1, coord[1]))
        # Right
        if self.is_walkable((coord[0] + 1, coord[1])):
            walkable.append((coord[0] + 1, coord[1]))

        return walkable

    def is_walkable(self, xy):
        try:
            return self.matrix[xy[1]][xy[0]] != constants.Terrain.WALL.value
        except IndexError:
            return False
