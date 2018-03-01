from enum import Enum

validterrains = set([0, 1, 2, 3, 4, 5, 6])

class Terrain(Enum):
    WALL = 0
    ROAD = 1
    MOUNTAIN = 2
    LAND = 3
    WATER = 4
    SAND = 5
    FOREST = 6