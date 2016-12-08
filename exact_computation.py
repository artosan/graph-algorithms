from dijkstar import Graph, find_path
import pickle
import sys
from itertools import islice
import time


class ExactStatisticsDjikstra(object):
    """
    This class calculates exact statistics from the given graph by using Dijkstra's shortest path algorithm.
    """
    def __init__(self, nodes, full_set_of_edges, directed):
        """
        We need to construct Graph object for the djikstar lib.
        """
        edges = self._prune_graph(nodes, full_set_of_edges)
        self.g = Graph()
        self.nodes = set()
        self.results = list()
        for e in edges:
            self.g.add_edge(int(e[0]),int(e[1]), {'cost': 1})
            if not directed:
                self.g.add_edge(int(e[1]),int(e[0]), {'cost': 1})

            self.nodes.add(e[0])
            self.nodes.add(e[1])
        
        print("Graph built with {} edges and {} nodes.".format(len(edges),len(nodes)))


    def _find_shortest_path(self, n1, n2):
        cost_func = lambda u, v, e, prev_e: e['cost']
        return find_path(self.g, n1, n2, cost_func=cost_func)


    def calculate(self):
        iters = (len(self.nodes) * len(self.nodes)) / 2;
        curr = 0
        print("Total {} iterations".format(iters))
        #print(self.nodes)
        for i, n1 in enumerate(self.nodes):
            for n2 in islice(self.nodes, i, None):
                if n1 == n2:
                    next

                r = self._find_shortest_path(n1, n2)
                self.results.append((len(r[0]) - 1))
                curr = curr + 1
                if curr % 10000 == 0:
                    sys.stdout.write(" " + str(curr/float(iters)) + " ")
                    sys.stdout.flush()

        return self.results

    def _prune_graph(self, nodes, edges):
        """
        Removes the unnecessary parts of the full graph i.e. when nodes of the scc
        are given it removes all edges that are not part of it
        """
        pruned_edges = list()
        check_nodes = set(nodes)
        for e in edges:
            if e[0] in check_nodes and e[1] in check_nodes:
                pruned_edges.append(e)

        return pruned_edges



class ExactStatisticsFW(object):
    """
    This class calculates exact statistics by Floyd-Warshall algorithm.
    """
    def __init__(self, nodes, full_set_of_edges, directed):
        """
        We need to construct Graph object for the djikstar lib.
        """
        edges = self._prune_graph(nodes, full_set_of_edges)
        self.g = {}
        self.nodes = set()
        self.results = list()
        for e in edges:
            #self.g.add_edge(int(e[0]),int(e[1]), {'cost': 1})
            #if not directed:
            #    self.g.add_edge(int(e[1]),int(e[0]), {'cost': 1})
            if e[0] not in self.g:
                self.g[e[0]] = {}
            else:
                self.g[e[0]][e[1]] = 1

            if not directed:
                if e[1] not in self.g:
                    self.g[e[1]] = {}
                else:
                    self.g[e[1]][e[0]] = 1

            self.nodes.add(e[0])
            self.nodes.add(e[1])

        self.g = self._adj(self.g)
        print("Graph built with {} edges and {} nodes.".format(len(edges),len(nodes)))


    def calculate(self):
        print("Starting to find cost between all pairs of vertices...")
        return self.fw(self.g)

            
    def _prune_graph(self, nodes, edges):
        """
        Removes the unnecessary parts of the full graph i.e. when nodes of the scc
        are given it removes all edges that are not part of it
        """
        pruned_edges = list()
        check_nodes = set(nodes)
        for e in edges:
            if e[0] in check_nodes and e[1] in check_nodes:
                pruned_edges.append(e)
                
        return pruned_edges

    def _adj(self, g):
        vertices = g.keys()

        dist = {}
        for i in vertices:
            dist[i] = {}
            for j in vertices:
                try:
                    dist[i][j] = g[i][j]
                except KeyError:
                    # the distance from a node to itself is 0
                    if i == j:
                        dist[i][j] = 0
                    # the distance from a node to an unconnected node is infinity
                    else:
                        dist[i][j] = float('inf')
        return dist


    def fw(self, g):
        vertices = g.keys()
        d = dict(g)  # copy g
        count = 0
        total_iters = len(vertices)
        print(total_iters)
        for k in vertices:
            if count % 20 == 0:
                sys.stdout.write(" " + str(count/float(total_iters)) + " ")
                sys.stdout.flush()
            for i in vertices:
                for j in vertices:
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])

            count = count + 1
        return d
        
    


if __name__ == "__main__":

    filenames = ['data/soc-Epinions1.txt']
    print("Starting exact graph stats computations...")
    start_time = time.time()
    for file in filenames:
        print("---------------------------------------------------------------------------------------------------")
        print("Starting to work with graph {}".format(file))
        start = time.time()


        wcc_nodes = pickle.load(open(file + ".wcc.p", "rb"))
        scc_nodes = pickle.load(open(file + ".scc.p", "rb"))
        with open(file) as f:
            edges = [tuple(map(long, i.split())) for i in f]

        r = ExactStatisticsDjikstra(wcc_nodes, edges, False)
        res = r.calculate()
        pickle.dump(res, open(file + ".wcc.statistics.p", "wb"))

        print("WCC done!")
        r = ExactStatisticsDjikstra(scc_nodes, edges, True)
        res = r.calculate()
        pickle.dump(res, open(file + ".scc.statistics.p", "wb"))


        end = time.time()
        timedelta = end - start
        print("Processing file {} took {} seconds".format(file,  timedelta))
        print("---------------------------------------------------------------------------------------------------")

    end_time = time.time()
    total_time_delta = end_time - start_time
    print("Processing graphs took in total {}".format(total_time_delta))
