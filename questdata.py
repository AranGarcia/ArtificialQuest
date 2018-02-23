''' Loads matrix of data from a text file '''

import random

WALL = 0
FLOOR = 1

class Map:
    ''' A map containing '''
    def __init__(self):
        self.matrix = []

    def load(self, fname):
        with open(fname) as fdata:
            lines = fdata.readlines()

        self.matrix = []
        for line in lines:
            self.matrix.append(
                [int(digit) for digit in line.split()]
            )

    def randomize(self, rows=10, columns=10):
        self.matrix = [
            [random.randint(0, 1) for i in range(columns)]
            for j in range(rows)
        ]
