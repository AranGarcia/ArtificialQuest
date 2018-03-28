"""
Artificial intelligence module used by characters to solve their tasks.
"""

from heapq import heapify, heappush, heappop
from  constants import MoveDir


class HeapNode:
    """
    Specific nodes structure for the heap that wraps the StateNode.

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
    Implementation of a heap for prioritizing states with minimal costs.
    """

    def __init__(self):
        self.heap = []

    def get_min(self):
        return self.heap[0]

    def push(self, state):
        heappush(self.heap, HeapNode(state))

    def pop(self):
        return heappop(self.heap).state

    def __len__(self):
        return len(self.heap)


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
        return 'Node<State:%s>' % (
            self.coord,
        )

DIR_DIFF = {
    (-1, 0): MoveDir.RIGHT,
    (1, 0): MoveDir.LEFT,
    (0, -1): MoveDir.DOWN,
    (0, 1): MoveDir.UP

}

DIRECTIONS = {
    MoveDir.RIGHT.value: (-1, 0),
    MoveDir.LEFT.value: (1, 0),
    MoveDir.DOWN.value: (0, -1),
    MoveDir.UP.value: (0, 1)
}

class MapProblem:
    """docstring for MapProblem."""

    def __init__(self, gmap, initial, goal):
        self.gmap = gmap
        self.initial = Node(initial, 0)
        self.goal = goal

    def is_goal(self, node):
        return node.coord == self.goal

    def iter_children(self, node):
        for child in self.gmap.get_walkable(node.coord):
            yield Node(child, (node.cost + 1), node, self.__get_direction(node.coord, child))

    def __get_direction(self, u, v):
        return DIR_DIFF[(u[0] - v[0], u[1] - v[1])]

def bf_search(problem):
    """
    Implemention of breadth-first-search algorithm.
    """
    node = problem.initial
    print('Initial node is', node)

    if node.coord == problem.goal:
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


if __name__ == '__main__':
    import maps

    print('BFS Test')
    print('Loading map...', end='')
    m = maps.Map('../src/maps/dungeon')
    print('done')

    print('Loading problem...', end='')
    prob = MapProblem(m, (0, 9), (15, 1))
    print(' done')

    print('Solving...')
    g = bf_search(prob)

    def print_path(node):
        print('Finding path to', node)

        path = [node]
        dad = node.parent

        while dad:
            path.insert(0, dad)
            dad = dad.parent

        for p in path:
            print(p)

    print_path(g)
