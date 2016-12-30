import itertools
import pickle


class SCC(object):

    def __init__(self, edges, directed):

        self.edges = {}
        if directed:
            for e in edges:
                try:
                    self.edges[e[0]].append(e[1])
                except Exception as err:
                    self.edges[e[0]] = list()
                    self.edges[e[0]].append(e[1])
        else:
            for e in edges:
                try:
                    self.edges[e[0]].append(e[1])
                except Exception as err:
                    self.edges[e[0]] = list()
                    self.edges[e[0]].append(e[1])

                try:
                    self.edges[e[1]].append(e[0])
                except Exception as err:
                    self.edges[e[1]] = list()
                    self.edges[e[1]].append(e[0])

        self.vertices = set(v for v in itertools.chain(*edges))
        print("Graph preprocessing done!")

    def find_scc(self):
        identified = set()
        stack = []
        index = {}
        boundaries = []

        for v in self.vertices:
            if v not in index:
                to_do = [('V', v)]
                while to_do:
                    operation_type, v = to_do.pop()
                    if operation_type == 'V':
                        index[v] = len(stack)
                        stack.append(v)
                        boundaries.append(index[v])
                        to_do.append(('P', v))
                        try:
                            to_do.extend([('E', w) for w in self.edges[v]])
                        except KeyError as e:
                            pass
                    elif operation_type == 'E':
                        if v not in index:
                            to_do.append(('V', v))
                        elif v not in identified:
                            while index[v] < boundaries[-1]:
                                boundaries.pop()
                    else:
                        if boundaries[-1] == index[v]:
                            boundaries.pop()
                            scc = set(stack[index[v]:])
                            del stack[index[v]:]
                            identified.update(scc)
                            yield scc

    def dfs_iter(self, graph, start, path=[]):
        """
        Iterative version of depth first search.
        Arguments:
            graph - a dictionary of lists that is your graph and who you're connected to.
            start - the node you wish to start at
            path - a list of already visited nodes for a path
        Returns:
            path - a list of strings that equal a valid path in the graph
        """
        q = [start]
        while q:
            v = q.pop()
            if v not in path:
                path += [v]
                try:
                    q += graph[v]
                except Exception as err:
                    # if key does not exist we can just ignore the exception
                    pass
        return path


if __name__ == "__main__":
    #edges = [(1,2),(2,3),(2,8),(3,4),(3,7),(4,5),(5,3),(5,6),(7,4),(7,6), (8,1),(8,7)]
    #edges = [(1,2),(1,3), (2,3),(2,4),(4,3),(4,5),(5,2),(5,6),(6,3),(6,4)]
    #edges = [(1,777),(1,3),(2,1),(666,777)]
    with open('data/soc-Epinions1.txt') as f:
        edges = [tuple(map(long, i.split())) for i in f]

    s = SCC(edges, False)
    #res = s.find_scc()
    #res = list(res)
    # res = s.dfs_iter(s.edges, 666) # from 666 Did read 75877 items
    res = s.dfs_iter(s.edges, 22652)

    #pickle.dump(res, open("data/gplus_combined.txt.dump", "wb"))
    print(res)
    print("Did read {} items".format(len(res)))
