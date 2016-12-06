from dijkstar import Graph, find_path
import pickle
import sys
from itertools import islice
import time

class ExactStatistics(object):
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


    def calculate_full_statistics(self):
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
        
    


if __name__ == "__main__":

    filenames = ['data/gplus_combined.txt']
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

        s = ExactStatistics(wcc_nodes, edges, False)
        r = s.calculate_full_statistics()

        pickle.dump(r, open(file + ".wcc.statistics.p", "wb"))

        print("WCC done!")
        s = ExactStatistics(scc_nodes, edges, True)
        r = s.calculate_full_statistics()

        pickle.dump(r, open(file + ".scc.statistics.p", "wb"))


        end = time.time()
        timedelta = end - start
        print("Processing file {} took {} seconds".format(file,  timedelta))
        print("---------------------------------------------------------------------------------------------------")

    end_time = time.time()
    total_time_delta = end_time - start_time
    print("Processing graphs took in total {}".format(total_time_delta))
