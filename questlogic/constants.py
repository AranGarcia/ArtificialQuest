"""
Symbolic constants for questlogic.
"""
from enum import Enum

validterrains = set([0, 1, 2, 3, 4, 5, 6])

TERRAIN_NAMES = {
    0: 'Wall',
    1: 'Road',
    2: 'Mountain',
    3: 'Land',
    4: 'Water',
    5: 'Sand',
    6: 'Forest'
}

class Terrain(Enum):
    """ Terrain type constants """
    WALL = 0
    ROAD = 1
    MOUNTAIN = 2
    LAND = 3
    WATER = 4
    SAND = 5
    FOREST = 6

class MoveDir(Enum):
    """ Character movement constants """
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
