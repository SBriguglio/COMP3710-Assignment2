'''
COMP 3710: Assignment 2
Spencer Briguglio
'''
import collections
import math
import random
import string
from numpy.random import seed


class Vertex:
    def __init__(self, node):
        self.name = node
        self.discovered = False
        self.leaves = {}
        self.ancestor = []
        self.heuristic = 0

    def __str__(self):
        return self.name + 'leaves: ' + str([x.name for x in self.leaves])

    def add_leaf(self, leaf, time):
        self.leaves[leaf] = time

    def add_ancestor(self, anc):
        self.ancestor.append(anc)

    def discover(self):
        self.discovered = True

    def lose(self):
        self.discovered = False

    def get_leaves(self):
        return self.leaves.keys()

    def get_ancestor(self):
        return self.ancestor

    def get_name(self):
        return self.name

    def get_time(self, leaf):
        return self.leaves[leaf]

    def is_discovered(self):
        return self.discovered

    def set_heuristic(self, heuristic_cost):
        self.heuristic = heuristic_cost


def t_list_contains(q, s):
    for t in q:
        if t[1] == s:
            return True
    return False


class Graph:
    def __init__(self):
        self.vertexes = {}
        self.edges = {}
        self.n_vertexes = 0
        self.visited = {}
        self.exact = collections.deque()
        self.traversal = collections.deque()

    def __iter__(self):
        return iter(self.vertexes.values())

    def add_vertex(self, node, heuristic=None):
        self.n_vertexes = self.n_vertexes + 1
        vert = Vertex(node)
        self.vertexes[node] = vert
        vert.heuristic = heuristic
        return vert

    def add_edge(self, node, leaf, time):
        self.edges[(node, leaf)] = time

    def get_edge_time(self, node, leaf):
        return self.edges[(node.get_name(), leaf.get_name())]

    def get_vertex(self, node):
        if node in self.vertexes:
            return self.vertexes[node]
        else:
            return None

    def connect(self, node, leaf, time):
        if node not in self.vertexes:
            self.add_vertex(node)
        if leaf not in self.vertexes:
            self.add_vertex(leaf)
        self.add_edge(node, leaf, time)
        self.vertexes[node].add_leaf(self.vertexes[leaf], time)
        self.vertexes[leaf].add_ancestor(self.vertexes[node])

    def get_vertexes(self):
        return self.vertexes.keys()

    def lose_all(self):
        self.traversal.clear()
        self.exact.clear()
        for u in self.vertexes:
            self.vertexes[u].lose()

    def dfs(self, u):
        u.discover()
        print(u.get_name(), end='')
        for leaf in u.leaves:
            if not leaf.is_discovered():
                self.dfs(leaf)

    def bfs(self, a, z):
        queue = [a]
        exact = []
        ancestors = {a: None}
        print('Traversal Path: ', end='')
        while len(queue) > 0:
            q = queue.pop(0)
            q.discover()
            print(q.get_name(), end='')
            if q == z:
                i = q
                while i is not None:
                    exact.append(i)
                    i = ancestors[i]
                break
            for leaf in q.leaves:
                if not leaf.is_discovered():
                    queue.append(leaf)
                    if not ancestors.__contains__(leaf):
                        ancestors[leaf] = q
        exact.reverse()
        print('\nExact Path: ', end='')
        for i in exact:
            print(i.get_name(), end='')

    def inner(self, a, z, limit):
        flag = []
        self.traversal.append(a.get_name())
        if a == z:
            return True
        if limit == 0:
            return False
        for leaf in a.leaves:
            flag.append(self.inner(leaf, z, limit - 1))
            if flag.__contains__(True):
                self.exact.appendleft(leaf.get_name())
                return True

    def ids(self, a, z, limit):
        if limit > 0:
            if self.ids(a, z, limit - 1):
                self.exact.appendleft(a.get_name())
                return True
            if self.inner(a, z, limit - 1):
                return True
            self.traversal.append("")

    def ucs(self, a, z):
        opened = {a}
        closed = {}
        costs = {a: 0}
        ancestors = {}
        while opened:
            minimum = math.inf
            # select minimum cost state
            for o in opened:
                if costs[o] < minimum:
                    minimum = costs[o]
                    i = o
            opened.remove(self.get_vertex(i.get_name()))
            node = i
            self.traversal.append(node.get_name())
            # check if it is the goal
            if node == z:
                while True:
                    self.exact.appendleft(node.get_name())
                    if node == a:
                        return costs[self.get_vertex('G')]
                    node = ancestors[node]

            # expand leaves
            for leaf in node.leaves:
                # if leaf is not present in opened or closed, add it to opened and add it's costs, add it's ancestor
                if not (opened.__contains__(self.get_vertex(leaf.get_name())) or closed.__contains__(
                        self.get_vertex(leaf.get_name()))):
                    opened.add(self.get_vertex(leaf.get_name()))
                    costs[self.get_vertex(leaf.get_name())] = costs[node] + self.get_edge_time(node, leaf)
                    ancestors[leaf] = node

                # if leaf IS present in opened, update its cost and ancestor if the cost is cheaper
                elif opened.__contains__(self.get_vertex(leaf.get_name())):
                    if costs[self.get_vertex(leaf.get_name())] > costs[node] + self.get_edge_time(node, leaf):
                        costs[self.get_vertex(leaf.get_name())] = costs[node] + self.get_edge_time(node, leaf)
                        ancestors[leaf] = node

                # if leaf IS present in closed and its cost is cheaper, move it back to opened and update its cost
                # and ancestor
                elif closed.__contains__(self.get_vertex(leaf.get_name())):
                    if costs[self.get_vertex(leaf.get_name())] > costs[node] + self.get_edge_time(node, leaf):
                        opened.add(self.get_vertex(leaf.get_name()))
                        closed.pop(self.get_vertex(leaf.get_name()))
                        costs[self.get_vertex(leaf.get_name())] = costs[node] + self.get_edge_time(node, leaf)
                        ancestors[leaf] = node

            closed[node] = 0
        return -1

    def a_star(self, a, z, h_dict):
        opened = {a}
        closed = {}
        costs = {a: 0}
        ancestors = {}
        while opened:
            minimum = math.inf
            # select minimum cost state
            for o in opened:
                if costs[o] < minimum:
                    minimum = costs[o]
                    i = o
            opened.remove(self.get_vertex(i.get_name()))
            node = i
            self.traversal.append(node.get_name())
            # check if it is the goal
            if node == z:
                while True:
                    self.exact.appendleft(node.get_name())
                    if node == a:
                        return costs[self.get_vertex('G')]
                    node = ancestors[node]

            # expand leaves
            for leaf in node.leaves:
                # if leaf is not present in opened or closed, add it to opened and add it's costs, add it's ancestor
                # h(n)
                h = h_dict[self.get_vertex(leaf.get_name()).get_name()]
                if not (opened.__contains__(self.get_vertex(leaf.get_name())) or closed.__contains__(
                        self.get_vertex(leaf.get_name()))):
                    opened.add(self.get_vertex(leaf.get_name()))
                    # f(n) = (g(n)) + h(n)
                    costs[self.get_vertex(leaf.get_name())] = (costs[node] + self.get_edge_time(node, leaf)) + h
                    ancestors[leaf] = node

                # if leaf IS present in opened, update its cost and ancestor if the cost is cheaper
                elif opened.__contains__(self.get_vertex(leaf.get_name())):
                    # F(n) > f(n) --> F(n) = g(n) + h(n)
                    if costs[self.get_vertex(leaf.get_name())] > (costs[node] + self.get_edge_time(node, leaf)) + h:
                        # f(n) = (g(n)) + h(n)
                        costs[self.get_vertex(leaf.get_name())] = costs[node] + self.get_edge_time(node, leaf) + h
                        ancestors[leaf] = node

                # if leaf IS present in closed and its cost is cheaper, move it back to opened and update its cost
                # and ancestor
                elif closed.__contains__(self.get_vertex(leaf.get_name())):
                    if costs[self.get_vertex(leaf.get_name())] > costs[node] + self.get_edge_time(node, leaf) + h:
                        opened.add(self.get_vertex(leaf.get_name()))
                        closed.pop(self.get_vertex(leaf.get_name()))
                        costs[self.get_vertex(leaf.get_name())] = costs[node] + self.get_edge_time(node, leaf) + h
                        ancestors[leaf] = node
            closed[node] = 0
        return -1


def random_graph(a, z, e, n):
    seed(1)
    r = Graph()
    r.add_vertex(a)
    r.add_vertex(z)
    alphabet = [a, z]
    while len(alphabet) < n - 2:
        a = random.choice(string.ascii_letters)
        if not alphabet.__contains__(a):
            alphabet.append(a)
            r.add_vertex(a)
    random.shuffle(alphabet)
    for i in range(e):
        while True:
            b = random.choice(alphabet)
            c = random.choice(alphabet)
            if not b == c:
                break
        r.connect(b, c, random.randint(1, 11))
    return r


if __name__ == '__main__':
    g = Graph()
    #"""
    g.add_vertex('S')
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_vertex('C')
    g.add_vertex('D')
    g.add_vertex('G')

    g.connect('S', 'A', 3)
    g.connect('S', 'B', 2)
    g.connect('A', 'B', 1)
    g.connect('A', 'D', 5)
    g.connect('B', 'C', 2)
    g.connect('B', 'D', 3)
    g.connect('C', 'D', 3)
    g.connect('C', 'G', 4)
    g.connect('D', 'G', 1)
    
    h_dict = {'S': 6, 'A': 4, 'B': 3, 'C': 3, 'D': 1, 'G': 0}
    """
    g.add_vertex('S')
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_vertex('C')
    g.add_vertex('D')
    g.add_vertex('E')
    g.add_vertex('G')

    g.connect('S', 'A', 6)
    g.connect('S', 'B', 5)
    g.connect('S', 'C', 10)
    g.connect('A', 'D', 6)
    g.connect('B', 'D', 6)
    g.connect('B', 'E', 7)
    g.connect('C', 'E', 6)
    g.connect('D', 'C', 4)
    g.connect('D', 'G', 4)
    g.connect('E', 'A', 3)
    g.connect('E', 'G', 6)

    h_dict = {'S': 14, 'A': 7, 'B': 10, 'C': 4, 'D': 2, 'E': 4, 'G': 0}
    """
    print("[DFS]\nTraversal and Exact path:", end='')
    g.dfs(g.get_vertex('S'))
    g.lose_all()
    print()
    print("\n[BFS]")
    g.bfs(g.get_vertex('S'), g.get_vertex('G'))
    g.lose_all()
    print()
    print("\n[IDS]")
    g.ids(g.get_vertex('S'), g.get_vertex('G'), 5)
    print("Traversal Path: ", *list(g.traversal), sep=' ')
    print("Exact Path: ", *list(g.exact))
    g.lose_all()
    print()
    print("[UCS]")
    cost = g.ucs(g.get_vertex('S'), g.get_vertex('G'))
    print("Traversal Path: ", *list(g.traversal))
    print("Exact Path: ", *list(g.exact))
    print("Cost: {}".format(cost))
    g.lose_all()
    print()
    print("[A*]")
    cost = g.a_star(g.get_vertex('S'), g.get_vertex('G'), h_dict)
    print("Traversal Path: ", *list(g.traversal))
    print("Exact Path: ", *list(g.exact))
    print("Cost: {}".format(cost))
"""
    print("\n\n[Generating Random Graph]---------------------------")
    r = random_graph('S', 'G', 35, 10)
    print("35 edges, 15 nodes")
    print("[DFS]\nTraversal and Exact path:", end='')
    r.dfs(r.get_vertex('S'))
    r.lose_all()
    print()
    print("\n[BFS]")
    r.bfs(r.get_vertex('S'), r.get_vertex('G'))
    r.lose_all()
    print()
    print("\n[IDS]")
    r.ids(r.get_vertex('S'), r.get_vertex('G'), 5)
    print("Traversal Path: ", *list(r.traversal), sep=' ')
    print("Exact Path: ", *list(r.exact))
    r.lose_all()
    print()
    print("[UCS]")
    r.ucs(r.get_vertex('S'), r.get_vertex('G'))
    print("Traversal Path: ", *list(r.traversal))
    print("Exact Path: ", *list(r.exact))
"""
