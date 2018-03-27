"""
Artificial intelligence module used by characters to solve their tasks.
"""

print('Imported AI')


class HeapNode:
    """
    Specific nodes structure for the heap that wraps the StateNode.

    The '<', '>' and '==' operators are overloaded so that states may be
    compared with each other in the heap or priority queue.
    """

    def __init__(self, state, cost):
        self.state = state
        self.cost = cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __lt__(self, other):
        return self.cost < other.cost


class StateHeap:
    """
    Implementation of a heap for prioritizing states with minimal costs.
    """

    def __init__(self, initial=None):
        if initial is not None:
            heapify(initial)
        self.heap = initial

    def get_min(self):
        return self.heap[0]

    def push(self, coord, cost):
        heappush(self.heap, HeapNode(coord, cost))

    def pop(self):
        return heappush(self.heap)

    def __len__(self):
        return len(self.heap)


class Node:
    """
    Node data structure used in the MapProblem class. The coordinate is the
    state itself.
    """

    def __init__(self, coord, parent, action, cost):
        self.coord = coord
        self.parent = parent
        self.action = action
        self.cost = cost

    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return 'Node<S:%s, P:%s, A:%s, C:%s>' % (
            self.state,
            self.parent,
            self.action,
            self.cost
        )


class MapProblem:
    """docstring for MapProblem."""

    def __init__(self, initial, goal, gmap):
        self.initial = initial
        self.goal = goal
        self.gmap = gmap
        self.actions = actions

    @staticmethod
    def child_node(node):
        pass

    def is_goal(self, node):
        return node == self.goal


def bfsalgorithm(problem):
    node = problem.initial

    if node == problem.goal:
        return node

    frontier
