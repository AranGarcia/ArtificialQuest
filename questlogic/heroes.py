from constants import MoveDir, Terrain, Algorithm
import ai


class Hero:
    """docstring for Hero."""

    def __init__(self, name, gmap, pos):
        self.name = name
        self.gmap = gmap
        self.pos = pos
        self.__start = None
        self.__goal = None
        self.decisions = set([])
        self.explored = set([])

        # The indexes are the values returned by key pressing events from pygame
        self.movements = {
            273: self.__moveup,
            274: self.__movedown,
            276: self.__moveleft,
            275: self.__moveright
        }

        # The actions that the agent will do in order while doing depth searches
        self.actions = None

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

    def look_around(self, coord):
        """
        Add surroundings to the explored set
        """

        limx = len(self.gmap.matrix[0])
        limy = len(self.gmap.matrix)

        x, y = coord[0], coord[1]

        self.explored.add((x, y))
        w = self.gmap.get_walkable((x, y))

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

    def start_search(self, algorithm, enhance=False):
        """
        Starts a search algorithm from a start state to a goal state using
        breadth first, depth first or iterative deepening search.

        start     : (x,y) coordinates of the start state.
        goal      : (x,y) coordinates of the goal state.
        algorithm : Symbolic constant in Constants representing the type of
                    algorithm.
        enhance   : If true, redundant nodes will not be generated.

        Raises ValueError if:
        - The initial and/or goal coordinate were not defined
        - A depth search algorithm was requested but actions were not defined
          for the hero.
        """

        if not self.__start or not self.__goal:
            raise ValueError(' start/goal')

        problem = ai.MapProblem(self.gmap, self.__start, self.__goal)

        # TODO: Find out why comparison between same Enums returns False
        if algorithm.value == Algorithm.BFS.value:
            self.pos = self.__start
            self.explored = set()

            solution = ai.bf_search(problem, enhance)

            self.update_explored(problem.explored)
            if solution.status == ai.SolStat.SUCCESS:
                self.pos = [solution.node.coord[0], solution.node.coord[1]]
                Hero.__print_path(solution.node)
                return True
            else:
                return False

        # At this point, ony depth searches remain.
        # The hero must define the order of its actions, so if they are not
        # defined an exception will ocurr
        else:
            if(self.actions is None):
                raise ValueError(' actions.')

            if algorithm.value == Algorithm.DFS.value:
                self.pos = self.__start
                self.explored = set()

                solution = ai.df_search(problem, self.actions, enhance)

                self.update_explored(problem.explored)
                if solution.status == ai.SolStat.SUCCESS:
                    self.pos = [solution.node.coord[0], solution.node.coord[1]]
                    Hero.__print_path(solution.node)
                    return True
                else:
                    return False

            elif algorithm.value == Algorithm.IDS.value:
                self.pos = self.__start
                self.explored = set()

                solution = ai.id_search(problem, self.actions, enhance)

                self.update_explored(problem.explored)
                if solution.status == ai.SolStat.SUCCESS:
                    self.pos = [solution.node.coord[0], solution.node.coord[1]]
                    Hero.__print_path(solution.node)
                    return True
                else:
                    return False

    def set_start(self, start):
        self.__start = start

    def set_goal(self, goal):
        self.__goal = goal

    def update_explored(self, explored):
        for exp in explored:
            self.look_around(exp)

    @staticmethod
    def __print_path(node):
        path = [node]
        dad = node.parent

        while dad:
            path.insert(0, dad)
            dad = dad.parent

        for p in path:
            print(p)


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
            Terrain.MOUNTAIN: None,
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
            Terrain.MOUNTAIN: None,
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
            Terrain.MOUNTAIN: None,
            Terrain.LAND: 2,
            Terrain.WATER: 1,
            Terrain.SAND: None,
            Terrain.FOREST: 3
        }
