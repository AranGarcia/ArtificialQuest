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

    def count_walkable(self, coord):
        walkable = 0

        # Up
        if self.is_walkable((coord[0], coord[1] - 1)):
            walkable += 1
        # Down
        if self.is_walkable((coord[0], coord[1] + 1)):
            walkable += 1
        # Left
        if self.is_walkable((coord[0] - 1, coord[1])):
            walkable += 1
        # Right
        if self.is_walkable((coord[0] + 1, coord[1])):
            walkable += 1

        return walkable

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

                # Invalid values will be treated as 0 (as a wall)
                if not value in constants.valid_terrains:
                    self.matrix[index].append(0)
                else:
                    self.matrix[index].append(value)

        # If matrix is not rectangular, add the columns to the rows that are short
        def rowsize(l): return len(l)

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

    def get_terrains(self, coord):
        """
        get_terrains(coord) -> [(coord_1, TERRAIN_TYPE)...]
        coord       : A bidimensional list or tuple
        TERRAIN_TYPE: Constant defined in constants.py indicating the type of
                      terrain.

        Just like the get_walkable method, this method returns a list of
        surrounding terrains of a coordinate in the map that contain the
        coordinate and the type of terrain.
        """
        succesors = []

        # Up
        if coord[1] > 0:
            succesors.append(
                ((coord[0], coord[1] - 1),
                 constants.Terrain(self.matrix[coord[1] - 1][coord[0]]))
            )
        # Down
        if coord[1] < len(self.matrix) - 1:
            succesors.append(
                ((coord[0], coord[1] + 1),
                 constants.Terrain(self.matrix[coord[1] + 1][coord[0]]))
            )
        # Left
        if coord[0] > 0:
            succesors.append(
                ((coord[0] - 1, coord[1]),
                 constants.Terrain(self.matrix[coord[1]][coord[0] - 1]))
            )
        # Right
        if coord[0] < len(self.matrix[0]) - 1:
            succesors.append(
                ((coord[0] + 1, coord[1]),
                 constants.Terrain(self.matrix[coord[1]][coord[0] + 1]))
            )

        return succesors

    def is_walkable(self, xy):
        try:
            return self.matrix[xy[1]][xy[0]] != constants.Terrain.WALL.value
        except IndexError:
            return False
