import math

from ai import genetics, search
from constants import Algorithm, MoveDir, Terrain, Heroes


class Hero:
    """
    The characters that will be placed on the map. Each Hero can establish a
    goal and can use its searching abilities to get to that goal. Searching constant
    be done by BLIND or HEURISTIC searches.

    Hero(name, gmap, pos)
    name : The name of the hero
    gmap : Map object representing the world in which the hero is in.
    pos  : Initial position of the hero.
    """

    def __init__(self, species, gmap, pos):
        self.species = species
        self.gmap = gmap
        self.pos = pos
        self.cost = {}
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

    def look_around(self, coord):
        """
        Add surroundings to the explored set
        """

        limx = len(self.gmap.matrix[0])
        limy = len(self.gmap.matrix)

        x, y = coord[0], coord[1]

        self.explored.add((x, y))
        w = self.gmap.get_walkable((x, y))

        if len(w) == 1 or len(w) > 2:
            self.decisions.add((x, y))

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
        breadth first, depth first or iterative deepening search. The Initial
        and goal states are defined previously with set_goal and set_start.

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

        problem = search.MapProblem(self.gmap, self.__start, self.__goal)

        # TODO: Find out why comparison between same Enums returns False
        if algorithm.value == Algorithm.BFS.value:
            solution = search.bf_search(problem, enhance)

        # At this point, ony depth searches remain.
        # The hero must define the order of its actions, so if they are not
        # defined an exception will ocurr
        else:
            if(self.actions is None):
                raise ValueError(' actions.')

            elif algorithm.value == Algorithm.DFS.value:
                solution = search.df_search(problem, self.actions, enhance)

            elif algorithm.value == Algorithm.IDS.value:
                solution = search.id_search(
                    problem, self.actions, 1, 1, enhance)

        # This helps the renderer restart the map
        self.pos = self.__start
        self.explored.clear()
        self.decisions.clear()
        self.update_explored(problem.explored)

        if solution.status == search.SolStat.SUCCESS:
            self.pos = [solution.node.coord[0], solution.node.coord[1]]
            path = Hero.__get_path(solution.node)

            print('Path from START to GOAL is: ', end='')
            for p in path:
                print(p.coord, end=' ')
            print('\n')

            print('Tree:')
            Hero.__print_tree(path[0])

            return True
        else:
            return False

    def start_heuristic_search(self):
        if not self.__start or not self.__goal:
            raise ValueError(' start/goal')

        problem = search.MapProblem(self.gmap, self.__start,
                                    self.__goal, self.cost)
        return search.astar_search(problem)

    def set_start(self, start):
        self.__start = (start[0], start[1])

    def set_goal(self, goal):
        self.__goal = (goal[0], goal[1])

    def update_explored(self, explored):
        for exp in explored:
            self.look_around(exp)

    @staticmethod
    def __get_path(node):
        path = [node]
        dad = node.parent

        while dad:
            path.insert(0, dad)
            dad = dad.parent

        return path

    @staticmethod
    def __print_tree(node, level=0):
        print('    ' * level, sep='', end='')
        print('|---', node.coord, sep='')
        for child in node.children:
            Hero.__print_tree(child, level + 1)

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


class Human(Hero):
    """
    A human character. Moves better on LAND tiles.

    It's movement costs are:
    MOUNTAIN: N/A
    LAND: 1
    WATER: 2
    SAND: 3
    FOREST: 4
    SWAMP : 5
    SNOW : 5
    """

    def __init__(self, name, gmap, pos):
        super(Human, self).__init__(name, gmap, pos)

        self.cost = {
            Terrain.MOUNTAIN: math.inf,
            Terrain.LAND: 1,
            Terrain.WATER: 2,
            Terrain.SAND: 3,
            Terrain.FOREST: 4,
            Terrain.SWAMP: 5,
            Terrain.SNOW: 5,
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
    SWAMP: 5
    SNOW: N/A
    """

    def __init__(self, name, gmap, pos):
        super(Monkey, self).__init__(name, gmap, pos)

        self.cost = {
            Terrain.MOUNTAIN: math.inf,
            Terrain.LAND: 2,
            Terrain.WATER: 4,
            Terrain.SAND: 3,
            Terrain.FOREST: 1,
            Terrain.SWAMP: 5,
            Terrain.SNOW: math.inf
        }


class Octopus(Hero):
    """
    An octopus character. Moves better on WATER tiles.

    It's movement costs are:
    MOUNTAIN: N/A
    LAND: 2
    WATER: 1
    SAND: N/A
    FOREST: 3
    SWAMP: 2
    SNOW: N/A
    """

    def __init__(self, name, gmap, pos):
        super(Octopus, self).__init__(name, gmap, pos)

        self.cost = {
            Terrain.MOUNTAIN: math.inf,
            Terrain.LAND: 2,
            Terrain.WATER: 1,
            Terrain.SAND: math.inf,
            Terrain.FOREST: 3,
            Terrain.SWAMP: 2,
            Terrain.SNOW: math.inf
        }


class Crocodile(Hero):
    def __init__(self, name, gmap, pos):
        super(Crocodile, self).__init__(name, gmap, pos)

        self.cost = {
            Terrain.MOUNTAIN: math.inf,
            Terrain.LAND: 2,
            Terrain.WATER: 1,
            Terrain.SAND: math.inf,
            Terrain.FOREST: 3,
            Terrain.SWAMP: 2,
            Terrain.SNOW: math.inf
        }


class Sasquatch(Hero):

    def __init__(self, name, gmap, pos):
        super(Sasquatch, self).__init__(name, gmap, pos)

        self.cost = {
            Terrain.MOUNTAIN: 15,
            Terrain.LAND: 4,
            Terrain.WATER: math.inf,
            Terrain.SAND: math.inf,
            Terrain.FOREST: 4,
            Terrain.SWAMP: 5,
            Terrain.SNOW: 3
        }


class Werewolf(Hero):

    def __init__(self, name, gmap, pos):
        super(Werewolf, self).__init__(name, gmap, pos)

        self.cost = {
            Terrain.MOUNTAIN: math.inf,
            Terrain.LAND: 1,
            Terrain.WATER: 3,
            Terrain.SAND: 4,
            Terrain.FOREST: 2,
            Terrain.SWAMP: math.inf,
            Terrain.SNOW: 3
        }


def assign_missions(chrs, gls):
    """
    Given a list of Heroes and a list of tuples that represent a goal, this
    method will return a list of for each Hero in the order that they were
    declared.

    Each list for every hero contains tuples that represent the coordinate of
    their path to a mission. The assignment calcualtes the best possible outcome
    for the whole team of heroes (the total cost of the missions is the lowest
    possible).
    """

    print('\nCalculating costs of each mission...\n')
    print('The portal will open at', gls['portal'])
    print('The temple is at', gls['temple'])
    print('The stones are at', gls['stones'])
    print('The key is at' + str(gls['key']) + '\n')

    results = []
    for hero in chrs:
        hero.set_start(hero.pos)
        c_results = []

        # Calculate Start - Temple
        hero.set_goal(gls['temple'])
        solution = hero.start_heuristic_search()
        node = solution.node
        c_results.append(node)

        # Start - Temple - portal
        hero.set_start(gls['temple'])
        hero.set_goal(gls['portal'])
        solution = hero.start_heuristic_search()
        node = solution.node
        c_results.append(node)

        # Start - Magic Stones
        hero.set_start(hero.pos)
        hero.set_goal(gls['stones'])
        solution = hero.start_heuristic_search()
        node = solution.node
        c_results.append(node)

        # Start - Magic Stones - Portal
        hero.set_start(gls['stones'])
        hero.set_goal(gls['portal'])
        solution = hero.start_heuristic_search()
        node = solution.node
        c_results.append(node)

        # Start - Key
        hero.set_start(hero.pos)
        hero.set_goal(gls['key'])
        solution = hero.start_heuristic_search()
        node = solution.node
        c_results.append(node)

        # Start - Key - Portal
        hero.set_start(gls['key'])
        hero.set_goal(gls['portal'])
        solution = hero.start_heuristic_search()
        node = solution.node
        c_results.append(node)

        results.append(c_results)

    # Print results
    print('%-10s|%-7s|%-7s|%-7s|%-7s|%-7s|%-7s' %
          ('HERO', 'I-T', 'I-T-P', 'I-S', 'I-S-P', 'I-K', 'I-K-P'),
          '-' * 57, sep='\n'
          )

    costs = []
    for i, tr in enumerate(results):
        print('%-10s|  %-5s|  %-5s|  %-5s|  %-5s|  %-5s|  %-5s' %
              (chrs[i].species,
               tr[0].acc_cost, tr[1].acc_cost + tr[0].acc_cost,
               tr[2].acc_cost, tr[3].acc_cost + tr[2].acc_cost,
               tr[4].acc_cost, tr[5].acc_cost + tr[4].acc_cost)
              )
        costs.append([
            (0, tr[1].acc_cost + tr[0].acc_cost),
            (1, tr[3].acc_cost + tr[2].acc_cost),
            (2, tr[5].acc_cost + tr[4].acc_cost)
        ])
    print()

    assignments = search.schedule(costs)
    assignment_names = ['Temple', 'Stones', 'Key']

    print('\nMission assignment:')
    for i, c in enumerate(chrs):
        print('%-10s:%s' % (c.species, assignment_names[assignments[i]]))

    return __build_paths(
        (results[0][assignments[0] * 2], results[0][assignments[0] * 2 + 1]),
        (results[1][assignments[1] * 2], results[1][assignments[1] * 2 + 1]),
        (results[2][assignments[2] * 2], results[2][assignments[2] * 2 + 1]),
    )


def use_genetic_search(heroes, starts, goals):
    """
    Returns an estimated but quite good solution of assigning the 4 missions to
    the 3 selected heroes using genetic algorithms.
    """
    print("Search for optimal assignments of missions...")
    print('The portal will open at', goals['PORTAL'])
    print('The temple is at', goals['TEMPLE'])
    print('The stones are at', goals['STONES'])
    print('The key is at', str(goals['KEY']))
    print('Your friend is at' + str(goals['FRIEND']) + '\n')

    print("Party selected:",  ' '.join(
        [h.species.name for h in heroes]), end='')

    # Dictionary of costs for every character
    costs = {}

    # First get all possible costs for every hero
    # (X should not be calculated)
    # _|1|2|3|k|t|s|f|p
    # 1|X|X|X| | | | |
    # 2|X|X|X| | | | |
    # 3|X|X|X| | | | |
    # k| | | |X| | | |
    # t| | | | |X| | |
    # s| | | | | |X| |
    # p| | | | | | |X|

    print('Calculating costs (this may take a while)...')
    for h in heroes:
        hero_costs = {}

        for index, st in enumerate(starts):
            # Each starting point will map to destination.
            # (The value will be a search node with the path cost)
            start_dict = {}

            # Iterate to all possible goals
            for k, v in goals.items():
                h.set_start(st)
                h.set_goal(v)
                solution = h.start_heuristic_search()
                start_dict[k] = solution.node

            hero_costs[index] = start_dict
        # Also calculate paths between objectives, except to itself
        for k, v in goals.items():
            goal_dict = {}
            for j, w in goals.items():
                if k != j:
                    h.set_start(v)
                    h.set_goal(w)
                    solution = h.start_heuristic_search()
                    goal_dict[j] = solution.node
            hero_costs[k] = goal_dict

        print_gen_costs(hero_costs, h.species.name)

        costs[h.species.name] = hero_costs
    print("DONE. Now using genetic algorithm...")

    # The result is an dictionary mapping a hero to another dictionary,
    # which in turn maps one of the keys to another key from the goal
    # dictionary

    result = genetics.genetic_search(costs, starts)
    print("\nGenetic algorithm done. Result is")

    # Print results
    paths = {}
    for k, v in result.items():
        if v:
            print(k)
            print('\t', starts[v[0]])
            for i in v[1:]:
                print('\t', i)

            __path_for_hero(k, v, costs)


def __build_paths(*missions):
    paths = []

    for m in missions:
        paths.append(__build_path(m))

    return paths


def __path_for_hero(hero, missions, costs):
    """
    Returns a list of tuples which are the coordinates of the path to take.
    """

    # Since search algorihtm returns a leaf node, iteration will made from the portal
    # to last objective, to second last, etc...
    node = costs[hero][missions[-1]]["PORTAL"]
    total = [p for p in node.get_path()]

    # Add path from last objective to portal
    node = costs[hero]

    for i in range(len(missions) - 1, 0, -1):
        node = costs[hero][missions[i - 1]][missions[i]]
        path = node.get_path()

        for a in path[::-1]:
            total.insert(0, a)

    return total


def __build_path(s_i_p):
    """ Builds path from start point, to item and then to portal. """
    path = []

    # Builds the path in reverse.
    # From portal to item
    aux = s_i_p[1]
    while aux:
        path.insert(0, aux.coord)
        aux = aux.parent

    # From item to start point
    aux = s_i_p[0]
    while aux:
        path.insert(0, aux.coord)
        aux = aux.parent

    # print('Path made:', path)

    return path


def __build_genetic_path(individual):
    pass


def print_gen_costs(costs, name):
    g = [0, 1, 2, "KEY", "TEMPLE", "STONES", "FRIEND", "PORTAL"]

    print("Costs for", name.capitalize())
    print("______", end='')
    for i in g[3:]:
        print("|%6s" % str(i), end='')
    print()

    for i in g:
        print("%6s" % str(i), end='')
        for j in g[3:]:
            if not isinstance(j, int) and i != j:
                print("|%6s" % str(costs[i][j].acc_cost), end='')
            else:
                print("|------", end='')
        print()
    print()
