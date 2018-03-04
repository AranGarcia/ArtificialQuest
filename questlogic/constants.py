from enum import Enum

validterrains = set([0, 1, 2, 3, 4, 5, 6])

terrainnames = {
    0: 'Wall',
    1: 'Road',
    2: 'Mountain',
    3: 'Land',
    4: 'Water',
    5: 'Sand',
    6: 'Forest'
}

class Terrain(Enum):
    WALL = 0
    ROAD = 1
    MOUNTAIN = 2
    LAND = 3
    WATER = 4
    SAND = 5
    FOREST = 6
