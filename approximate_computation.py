from dijkstar import Graph, find_path
import pickle
from helpers import mean, percentile, prune_graph
import time
import sys
from bitstring import BitArray
from math import floor, log, pow
from random import random, choice, sample
from bisect import bisect


class ANF0(object):
    """
    This class implements anf0 algorithm to approximate graph stats
    """

    def weighted_choice(self, choices):
        """
        This function returns weighted choices, for instance:
        weighted_choice([(1,0.9),(0,0.1)]) would return 1 by 90% change
        and 0 by 10% change.

        This function is taken from:
        https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
        """
        values, weights = zip(*choices)
        total = 0
        cum_weights = []
        for w in weights:
            total += w
            cum_weights.append(total)
        x = random() * total
        i = bisect(cum_weights, x)
        return values[i]

    def build_bitmask(self, bits):
        """
        Build bitmask, we use n bits where n is the lowest number
        of bits required to represent number of nodes in the graph as binary.as

        This function return one bitvector and the bitvector is guaranteed to have one and only one bit set to 1.
        """
        bs = BitArray(bits)
        working = True
        while working:
            for b in range(bits):
                bs[b] = self.weighted_choice(
                    [(1, pow(0.5, b + 1)), (0, (1 - pow(0.5, b + 1)))])
                if bs[b] == 1:
                    working = False
                    break
        # sanity check, only one bit set!
        assert bs.count(True) == 1
        return bs

    def try_get(self, val, bits):
        try:
            v = val[0]
        except Exception as e:
            v = bits
        return v

    def anf0(self, edges, X, distances, k):
        """
        ANF-0 In-core ANF approximation algorithm, for details see:
        https://www.cs.cmu.edu/~christos/PUBLICATIONS/kdd02-anf.pdf

        Required edges, nodes X, distances to cover as an integer as parameter.
        """
        start_time = time.time()
        nodes = len(X)
        Mcur = {}
        Mlast = {}
        bits = int(floor(log(nodes, 2) + 1))
        IN = {}
        N = {}
        vals = list()
        for x in X:
            Mcur[x] = self.build_bitmask(bits)
            for i in range(1, k):
                Mcur[x] = Mcur[x] + self.build_bitmask(bits)

        # do distances from 1 to distances + 1
        for h in range(1, distances + 1):
            IN[h] = {}
            for x in X:
                Mlast[x] = Mcur[x]
            for x in X:
                for e in edges:
                    if e[0] == x:
                        Mcur[x] = (Mcur[x] | Mlast[e[1]])

            values = list()

            for x in X:
                vals = list()
                for i in range(0, k):
                    vals.append(Mcur[x][(i * bits):((i + 1) * bits)])

                positions = list()
                for val in vals:
                    tmp = val.find('0b0')
                    positions.append(self.try_get(tmp, bits))

                m = mean(positions)

                IN[h][x] = (pow(2, m)) / float(0.77351)
                values.append(IN[h][x])

            N[h] = sum(values)
            print("Distance {} N[h] {}".format(h, N[h]))

        end = time.time()
        timedelta = end - start_time
        print("\nANF0 took {} seconds\n".format(timedelta))
        return IN


class RandomPairs(object):
    """
    This class calculates statistics of the graph by randomly picking node pairs
    from the graph and calculating distance between those node pairs by Djikstras algorithm.
    """

    def __init__(self, nodes, full_set_of_edges, directed):
        """
        We need to construct Graph object for the djikstar lib.
        """
        edges = prune_graph(nodes, full_set_of_edges)
        self.g = Graph()
        self.nodes = set()
        self.results = list()
        for e in edges:
            self.g.add_edge(int(e[0]), int(e[1]), {'cost': 1})
            if not directed:
                self.g.add_edge(int(e[1]), int(e[0]), {'cost': 1})

            self.nodes.add(e[0])
            self.nodes.add(e[1])

    def _find_shortest_path(self, n1, n2):
        cost_func = lambda u, v, e, prev_e: e['cost']
        return find_path(self.g, n1, n2, cost_func=cost_func)

    def approximate(self, iter):
        """
        Runs iter number of iterations of Djikstras algorithm and
        calculates stats
        """
        start_time = time.time()

        values = list()
        for i in range(1, iter):
            if i % 100 == 0:
                sys.stdout.write(" " + str(i / float(iter)) + " ")
                sys.stdout.flush()
            a = sample(self.nodes, 1)
            b = sample(self.nodes, 1)
            r = self._find_shortest_path(a[0], b[0])
            values.append((len(r[0]) - 1))

        values = sorted(values)
        d_median = percentile(values, 0.5)
        d_mean = mean(values)
        d_diameter = max(values)
        d_effective_diameter = percentile(values, 0.9)

        end = time.time()
        timedelta = end - start_time
        print("\nApproximating statistics took {} seconds\n".format(timedelta))
        return (d_median, d_mean, d_diameter, d_effective_diameter)


class RandomBFS(object):
    """
    This class calculates statistics of the graph by randomly picking node pairs
    from the graph and calculating distance between those node pairs by Djikstras algorithm.
    """

    def __init__(self, nodes, full_set_of_edges, directed):
        """
        We need to construct Graph object for the djikstar lib.
        """
        edges = prune_graph(nodes, full_set_of_edges)
        self.graph = {}
        self.nodes = set()
        for e in edges:
            self.nodes.add(e[0])
            self.nodes.add(e[1])
            if e[0] not in self.graph:
                self.graph[e[0]] = list()
                self.graph[e[0]].append(e[1])
            else:
                self.graph[e[0]].append(e[1])

            if not directed:
                if e[1] not in self.graph:
                    self.graph[e[1]] = list()
                    self.graph[e[1]].append(e[0])
                else:
                    self.graph[e[1]].append(e[0])

    def _bfs(self, start):
        '''iterative breadth first search from start'''
        dist = {}
        q = [start]
        dist[start] = 0
        path = list()
        while q:
            v = q.pop(0)
            if v not in path:
                path = path + [v]
                q = q + self.graph[v]
                for ve in self.graph[v]:
                    if ve not in dist:
                        dist[ve] = dist[v] + 1

        return (path, dist)

    def approximate(self, iter):
        """
        Runs iter number of iterations of Djikstras algorithm and
        calculates stats
        """
        start_time = time.time()
        values = list()
        for i in range(1, iter):
            if i % 100 == 0:
                sys.stdout.write(" " + str(i / float(iter)) + " ")
                sys.stdout.flush()
            a = sample(self.nodes, 1)
            r = self._bfs(a[0])

            values.append(r[1].values())

        values = [item for sublist in values for item in sublist]
        values = sorted(values)
        d_median = percentile(values, 0.5)
        d_mean = mean(values)
        d_diameter = max(values)
        d_effective_diameter = percentile(values, 0.9)

        end = time.time()
        timedelta = end - start_time
        print("\nApproximating statistics took {} seconds\n".format(timedelta))
        return (d_median, d_mean, d_diameter, d_effective_diameter)
