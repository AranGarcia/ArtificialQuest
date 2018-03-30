"""
Artificial intelligence module used by characters to solve their tasks.

Currently, this module  provides a hero with search methods to find their goal.
The search algorithms implemented are:

- Breadth first search
- Depth first searches
- Iterative depth limited search

It also abstracts the problem into a class, which will provide the means with
establishing and verifying goals, generating nodes given a state and check what
actions can be done.
"""

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

    def __hash__(self):
        return hash(self.coord)

    def __str__(self):
        p = self.parent.coord if self.parent is not None else None
        return 'Node<State:%s, Parent:%s>' % (
            self.coord,
            p
        )


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
    problems consist of an initial state, actions that an agent can do,
    """

    def __init__(self, gmap, initial, goal):
        self.gmap = gmap
        self.initial = Node(initial, 0)
        self.goal = goal

    def is_goal(self, node):
        return node.coord == self.goal

    def iter_children(self, node):
        for child in self.gmap.get_walkable(node.coord):
            yield Node(child, (node.cost + 1), node, self.__get_direction(node.coord, child))

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


def bf_search(problem):
    """
    Implemention of breadth-first-search algorithm.
    """
    node = problem.initial

    if problem.is_goal(node):
        return node

    frontier = StateHeap()
    frontier.push(node)
    explored = set()

    while frontier:
        node = frontier.pop()
        explored.add(node)

        for child in problem.iter_children(node):
            if child not in explored:
                if problem.is_goal(child):
                    return child
                frontier.push(child)
    return Node(False, -1)


def df_search(problem, actions):
    """
    df_search(problem, action) -> solution

    Implementation of depth first search using graph search (the explored states
    are stored so to avoid infinite loops). The solution returned is a node with
    the parent information and therefore the path from the initial point; if a
    solution doesn't exist, None is returned.

    One important thing to notice is that depth searches will generate states
    in the order that the agent has established it's actions. In other words, if
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
        if child:
            if child not in explored:
                explored.add(child)
                result = dfs_recursive(problem, actions, child, explored)

                # If the the goal was found on a child, return that child
                if result and problem.is_goal(result):
                    return result

    # Dead end
    return None


def dl_search(problem, actions, limit):
    """
    df_search(problem, action) -> solution

    Implementation of depth first search using graph search (the explored states
    are stored so to avoid infinite loops). The solution returned is a node with
    the parent information and therefore the path from the initial point; if a
    solution doesn't exist, None is returned.

    One important thing to notice is that depth searches will generate states
    in the order that the agent has established it's actions. In other words, if
    an agent always will move up and then down, it will first try to generate a
    state with an upward movement and then downward.
    """

    explored = set([problem.initial])
    return dls_recursive(problem, actions, problem.initial, limit, explored)


def dls_recursive(problem, actions, node, limit, explored):
    """
    Recursive auxiliary function for the df_search.
    """
    if problem.is_goal(node):
        return node

    # Cutoff
    if limit == 0:
        return False

    # The generation of states should be according to the order of the actions.
    for action in actions:
        child = problem.get_child(node, action)
        cutoff_ocurred = False

        # Not all states generate another state with all actions.
        if child:
            if child not in explored:
                explored.add(child)
                result = \
                    dls_recursive(problem, actions, child, limit - 1, explored)

                # If False is return, cutoff has ocurred
                # Otherwise, check if the the goal was found on a child, and
                # return that child
                if result is False:
                    cutoff_ocurred = True
                elif problem.is_goal(result):
                    return result

    # Limit has been reached
    if cutoff_ocurred:
        return False
    # Node with a dead end
    return None


def idf_search(problem, actions, initial_limit=0, increment=1):
    pass


if __name__ == '__main__':
    import maps

    def testbfs():
        print('BFS Test')
        print('Loading map...', end='')
        m = maps.Map('../src/maps/dungeon')
        print('done')

        print('Loading problem...', end='')
        prob = MapProblem(m, (0, 9), (15, 1))
        print(' done')

        print('Solving...')
        return bf_search(prob)

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

        print('Solving:\nStart', start, '\nEnd', end, '\n')
        return idf_search(
            prob,
            [
                MoveDir.UP,
                MoveDir.DOWN,
                MoveDir.LEFT,
                MoveDir.RIGHT
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

    g = testidfs()
    # print_path(g)
