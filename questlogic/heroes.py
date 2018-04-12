from . import constants
from constants import MoveDir, Terrain, Algorithm
import math

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

        # The actions that the agent will do in order while doing depth searches
        self.actions = None

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

    def start_search(self, start, goal, algorithm, enhance):
        """
        Starts a search algorithm from a start state to a goal state using
        breadth first, depth first or iterative deepening search.

        start     : (x,y) coordinates of the start state.
        goal      : (x,y) coordinates of the goal state.
        algorithm : Symbolic constant in Constants representing the type of
                    algorithm.
        enhance   : If true, redundant nodes will not be generated.
        """
        problem = ai.MapProblem(self.gmap, start, goal)

        if algorithm == Algorithm.BFS:
            ai.bf_search(problem, enhance)

        # At this point, ony depth searches remain.
        # The hero must define the order of its actions, so if they are not
        # defined an exception will ocurr
        if(self.actions is None):
            raise ValueError('hero must define actions before depth searches.')

        if algorithm == Algorithm.DFS:
            ai.df_search(problem, self.actions, enhance)
        elif algorithm == Algorithm.IDS:
            ai.id_search(problem, self.actions)

    def define_actions(self, actions):
        self.actions = actions


class Human(Hero):
    """
    A human character. Moves better on LAND tiles.

    It's movement costs are:
    MOUNTAIN: N/A
    LAND: 2
    WATER: 4
    SAND: 3
    FOREST: 1
    """

    def __init__(self, name, gmap, pos):
        super(Human, self).__init__(name, gmap, pos)

        self.cost = {
            Terrain.MOUNTAIN: math.inf,
            Terrain.LAND: 1,
            Terrain.WATER: 2,
            Terrain.SAND: 3,
            Terrain.FOREST: 4
        }


class Monkey(Hero):
    """
    A monkey character. Moves better on FOREST tiles.

    It's movement costs are:
    MOUNTAIN: N/A
    LAND: 2
    WATER: 4
    SAND: 3
    FOREST: 1
    """

    def __init__(self, name, gmap, pos):
        super(Monkey, self).__init__(name, gmap, pos)

        self.cost = {
            Terrain.MOUNTAIN: math.inf,
            Terrain.LAND: 2,
            Terrain.WATER: 4,
            Terrain.SAND: 3,
            Terrain.FOREST: 1
        }


class Octopus(Hero):
    """
    An octopus character. Moves better on WATER tiles.

    It's movement costs are:
    MOUNTAIN: N/A
    LAND: 2
    WATER: 4
    SAND: 3
    FOREST: 1
    """

    def __init__(self, name, gmap, pos):
        super(Octopus, self).__init__(name, gmap, pos)

        self.cost = {
            Terrain.MOUNTAIN: math.inf,
            Terrain.LAND: 2,
            Terrain.WATER: 1,
            Terrain.SAND: math.inf,
            Terrain.FOREST: 3
        }
