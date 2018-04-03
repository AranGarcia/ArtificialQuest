"""
Artificial intelligence module used by characters to solve their tasks.

Currently, this module  provides a hero with search methods to find their goal.
The search algorithms implemented are:

- Breadth first search
- Depth first searches
- Iterative depth limited search

It also abstracts the problem into a class, which will provide the means with
establishing and verifying goals, generating nodes given a state and check what
actions can be done. A problem should be instanced every time a hero has a goal
to reach.

Each search algorithm returns a Solution object that can represent a FAILURE or
a SUCCESS.
"""

from enum import Enum
from heapq import heapify, heappush, heappop
from constants import MoveDir

#####################################
# Data structures used in searching #
#####################################


class HeapNode:
    """
    Wrapper class for state Nodes that are used in the StateHeap.

    The '<', '>' and '==' operators are overloaded so that states may be
    compared with each other in the heap or priority queue.
    """

    def __init__(self, state):
        self.state = state

    def __eq__(self, other):
        return self.state.cost == other.state.cost

    def __gt__(self, other):
        return self.state.cost > other.state.cost

    def __lt__(self, other):
        return self.state.cost < other.state.cost


class StateHeap:
    """
    Implementation of a heap for prioritizing states with minimal costs. The
    operations are those of a usual heap:

    - Push a node in the heap.
    - Pop a node out of the heap.
    - Peek at the smallest cost node in the heap.
    """

    def __init__(self):
        self.heap = []

    def get_min(self):
        """ Get the smallest cost node (the node on top of the heap). """
        return self.heap[0]

    def push(self, state):
        """
        Insert a node into the heap. The heap's state is automatically updated
        in such a way that the structure is not lost.
        """
        heappush(self.heap, HeapNode(state))

    def pop(self):
        """
        Insert a node into the heap. The heap's state is automatically updated
        in such a way that the structure is not lost.
        """
        return heappop(self.heap).state

    def __len__(self):
        return len(self.heap)

##############################################
# Data structures for problem representation #
##############################################


class Node:
    """
    Node data structure used in the MapProblem class. The coordinate is the
    state itself.
    """

    def __init__(self, coord, cost, parent=None, action=None):
        self.coord = coord
        self.parent = parent
        self.action = action
        self.cost = cost

    def __eq__(self, other):
        return self.coord == other.coord

    def __str__(self):
        par = self.parent.coord if self.parent else None
        act = self.action if self.action else None
        return 'Node<State:%s, Parent:%s, Action%s>' % (
            self.coord,
            par,
            act
        )


class SolStat(Enum):
    """
    Symbolic constants that represent the status of the solution.

    CUTOFF is only used internally for iterative deepening search algorithm.
    """
    SUCCESS = 1
    FAILURE = 2
    CUTOFF = 3


class Solution:
    """
    A Solution structure, used as a result of any of the search algorithms. It's
    purpose is to maintain two fields:

    - Status: A symbolic constant representing the result of the search.
    - Node:   This field will be set with a node only if the status is SUCCESS.
    """

    def __init__(self, status, node=None):
        self.status = status
        self.node = node

    def __str__(self):
        return 'Solution<%s - %s>' % (self.status, self.node)

    def __eq__(self, other):
        return self.status == other


DIR_DIFF = {
    (-1, 0): MoveDir.RIGHT,
    (1, 0): MoveDir.LEFT,
    (0, -1): MoveDir.DOWN,
    (0, 1): MoveDir.UP
}

DIRECTIONS = {
    MoveDir.RIGHT.value: (1, 0),
    MoveDir.LEFT.value: (-1, 0),
    MoveDir.DOWN.value: (0, 1),
    MoveDir.UP.value: (0, -1)
}


class MapProblem:
    """
    Formulation of the problem that heroes will encounter on a map. Such
    problems consist of an initial state, actions that an agent can do on that
    state, and a goal state.
    """

    def __init__(self, gmap, initial, goal):
        self.gmap = gmap
        self.initial = Node(initial, 0)
        self.goal = goal
        self.explored = set([initial])

    def is_goal(self, node):
        """ Validates if node is the goal """
        return node.coord == self.goal

    def get_children(self, node):
        """
        Returns a list containing immediate children nodes.
        """
        return [Node(child, (node.cost + 1), node,
                     self.__get_direction(node.coord, child))
                for child in self.gmap.get_walkable(node.coord)
                ]

    def get_children_enhanced(self, node):
        walkable = [Node(w, 0, node, self.__get_direction(node.coord, w))
                    for w in self.gmap.get_walkable(node.coord)]

        walked = set([node.coord])

        def exp(n): return n not in walked

        for w in walkable:
            aux = w.coord
            while True:
                others = self.gmap.get_walkable(aux)
                if len(others) != 2 or aux == self.goal:
                    w.coord = aux
                    break
                # "Walking" to next node. Others is supposed to be empty if then
                # amount of neighbor nodes is equal to 2 (one of them is the
                # node from which it came from).
                walked.add(aux)
                aux, *others \
                    = [c for c in
                        filter(exp, self.gmap.get_walkable(aux))]

        self.explored.update(walked)
        # print('\tReturning')
        # for w in walkable:
        #     print('\t\t', w)
        return walkable

    def get_child(self, node, action):
        d = DIRECTIONS[action.value]
        child = (node.coord[0] + d[0], node.coord[1] + d[1])
        return Node(child, (node.cost + 1), node, action) \
            if self.gmap.is_walkable(child) else None

    def __get_direction(self, u, v):
        return DIR_DIFF[(u[0] - v[0], u[1] - v[1])]

#####################
# Search algorithms #
#####################

# Breadth first search


def bf_search(problem):
    """
    Implementation of the breadth first search algorithm.

    bf_search(problem) -> solution

    solution can have a status of:
    - SUCCESS: A goal node has been reached.
    - FAILURE: A goal cannot be reached from the initial state.
    """
    node = problem.initial

    if problem.is_goal(node):
        return Solution(SolStat.SUCCESS, node)

    frontier = StateHeap()
    frontier.push(node)

    while frontier:
        node = frontier.pop()
        problem.explored.add(node.coord)

        for child in problem.get_children(node):
            if child.coord not in problem.explored:
                if problem.is_goal(child):
                    return Solution(SolStat.SUCCESS, child)
                frontier.push(child)

    return Solution(SolStat.FAILURE)


def bf_search_enhanced(problem):
    """
    Implementation of the breadth first search algorithm.

    bf_search(problem) -> solution

    solution can have a status of:
    - SUCCESS: A goal node has been reached.
    - FAILURE: A goal cannot be reached from the initial state.
    """
    node = problem.initial
    print('\nStarting at', node, '\n')

    if problem.is_goal(node):
        return Solution(SolStat.SUCCESS, node)

    frontier = []
    frontier.append(node)

    while frontier:
        node = frontier.pop(0)
        problem.explored.add(node.coord)

        for child in problem.get_children_enhanced(node):
            if child.coord not in problem.explored:
                if problem.is_goal(child):
                    return Solution(SolStat.SUCCESS, child)

                frontier.append(child)
    return Solution(SolStat.FAILURE)


# Depth first search


def df_search(problem, actions):
    """
    df_search(problem, action) -> solution

    solution can hava a status of:
    - SUCCESS: A goal node has been reached.
    - FAILURE: A goal cannot be reached from the initial state.

    Implementation of depth first search using graph search (the explored states
    are stored so to avoid infinite loops). The solution returned is a node with
    the parent information and therefore the path from the initial point; if a
    solution doesn't exist, None is returned.

    One important thing to notice is that depth searches will generate states
    in the order that the agent has established it's ACTIONS. In other words, if
    an agent always will move up and then down, it will first try to generate a
    state with an upward movement and then downward.
    """

    explored = set([problem.initial])
    return dfs_recursive(problem, actions, problem.initial, explored)


def dfs_recursive(problem, actions, node, explored):
    """
    Recursive auxiliary function for the df_search.
    """
    if problem.is_goal(node):
        return node

    # The generation of states should be according to the order of the actions.
    for action in actions:
        child = problem.get_child(node, action)

        # Not all states generate another state with all actions.
        if child and child not in explored:
            explored.add(child)
            result = dfs_recursive(problem, actions, child, explored)

            # If the the goal was found on a child, return that child
            if result and problem.is_goal(result):
                return result

    # Dead end
    return None

# Depth limited search


def dl_search(problem, actions, limit):
    """
    dl_search(problem, action, limit) -> solution

    solution can hava a status of:
    - SUCCESS: A goal node has been reached.
    - FAILURE: A goal cannot be reached from the initial state.
    - CUTOFF : A goal cannot be reached from the initial state within the depth
               limit.

    Implementation of the depth limited search. The algorithm is similar to the
    depth first search, except that also considers a depth limit; if a solution
    is not found within that limit then a CUTOFF solution is returned.

    ACTIONS are also considered in order.
    """

    explored = set([problem.initial])
    return dls_recursive(problem, actions, problem.initial, limit, explored)


def dls_recursive(problem, actions, node, limit, explored):
    """
    Recursive auxiliary function for the dl_search.
    """
    if problem.is_goal(node):
        return Solution(SolStat.SUCCESS, node)
    elif limit == 0:
        return Solution(SolStat.CUTOFF)

    cutoff_ocurred = False
    for action in actions:
        child = problem.get_child(node, action)

        if child and child not in explored:
            explored.add(child)
            result = \
                dls_recursive(problem, actions, child, limit - 1, explored)
            if result is SolStat.CUTOFF:
                cutoff_ocurred = True

            elif result != SolStat.FAILURE:
                return result

    if cutoff_ocurred:
        return Solution(SolStat.CUTOFF)

    return Solution(SolStat.FAILURE)

# Iterative deepening search


def id_search(problem, actions, depth=1, increment=1):
    """
    id_search(problem, actions, depth, increment) -> solution

    solution can hava a status of:
    - SUCCESS: A goal node has been reached.
    - FAILURE: A goal cannot be reached from the initial state.

    Impementation of the iterative deepening search. The search starts
    considering a DEPTH limit in which a solution must be found. If a CUTOFF
    solution, then the depth limit is INCREMENTED and the search algorithm
    is invoked with the new depth limit, either a SUCCESS or FAILURE is returned.
    """
    while True:
        result = dl_search(problem, actions, depth)

        if result != SolStat.CUTOFF:
            return result
        else:
            depth += increment


if __name__ == '__main__':
    import maps

    def testbfs():
        print('BFS Test')
        print('Loading map...', end='')
        m = maps.Map('../src/maps/dungeon')
        print('done')

        print('Loading problem...', end='')
        prob = MapProblem(m, (1, 6), (15, 1))
        print(' done')

        print('Solving...')
        return bf_search_enhanced(prob)

    def testdfs():
        print('DFS Test')
        print('Loading map...', end='')
        m = maps.Map('../src/maps/dungeon')
        print('done')

        print('Loading problem...', end='')
        start = (0, 9)
        end = (15, 1)
        prob = MapProblem(m, start, end)
        print(' done')

        print('Solving:\nStart', start, '\nEnd', end, '\n')
        return df_search(
            prob,
            [
                MoveDir.UP,
                MoveDir.DOWN,
                MoveDir.LEFT,
                MoveDir.RIGHT
            ]
        )

    def testidfs():
        print('IDFS Test')
        print('Loading map...', end='')
        m = maps.Map('../src/maps/dungeon')
        print('done')

        print('Loading problem...', end='')
        start = (0, 9)
        end = (15, 1)
        prob = MapProblem(m, start, end)
        print(' done')

        print('Solving:\nStart', start, '\nEnd', end)
        return id_search(
            prob,
            [
                MoveDir.RIGHT,
                MoveDir.UP,
                MoveDir.LEFT,
                MoveDir.DOWN
            ],
            1,
            1
        )

    def print_path(node):
        print('Finding path to', node)

        path = [node]
        dad = node.parent

        while dad:
            path.insert(0, dad)
            dad = dad.parent

        for p in path:
            print(p)

    g = testbfs()
    print('\n\nDONE SEARCH:', g)
    print_path(g.node)
