import itertools
import copy


class ConnectedComponents(object):
    """
    This class implements connected components calculations on graph
    it provides functions to get largest strongly connected component and
    largest weakly connected component from the given graph
    """
    def __init__(self, edges, directed):
        """
        Constructor to initialize tha graph structure which is different for
        directed and non-directed graphs.
        """
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

    def _find_scc(self):
        """
        This function finds the largest strongly connected component from the graph,
        it is an implementation of tarjans algorithm. 

        This implementation is modified version from:
        https://code.activestate.com/recipes/578507-strongly-connected-components-of-a-directed-graph/
        """
        identified = set()
        stack = []
        index = {}
        boundaries = []
        result = list()
        edgecount = 0
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
                            if len(scc) > len(result):
                                result = scc

        result = list(result)
        for v in result:
            edges = self.edges[v]
            for e in edges:
                if e in result:
                    edgecount += 1

        return (edgecount, result)

    def _find_wcc(self, start):
        """
        Iterative function which performs depth first search and finds single
        weakly connected component
        """
        path = set()
        graph = self.edges
        vertices = [start]
        edgecount = 0
        while vertices:
            v = vertices.pop()
            if v not in path:
                path|= set([v])
                try:
                    vertices += graph[v]
                except Exception as err:
                    # if key does not exist we can just ignore the exception
                    pass

        # count edges
        for v in path:
            edgecount = edgecount + len(graph[v])
        # division by two since we have undirected graph
        # i.e. same edge is twice in graph
        return (edgecount / 2, path)

    def _find_one_wcc(self, v, vertices):
        """
        Helper function which finds one wcc and returns it. 
        Moreover we return set of vertices which we did not traverse yet.
        """
        edgecount, wcc = self._find_wcc(v)
        # is this deepcopy necessary?
        remaining_vertices = copy.deepcopy(vertices)
        remaining_vertices = remaining_vertices - set(wcc)
        return (edgecount, wcc, remaining_vertices)

    def find_largest_scc(self):
        """
        Wrapper function for find scc
        """
        return self._find_scc()

    def find_largest_wcc(self):
        """
        Finds largest strongly connected component of the graph.
        This id done by 
        """
        v = self.vertices.pop()
        self.vertices.add(v)
        curr_edgecount, wcc, remaining_vertices = self._find_one_wcc(
            v, self.vertices)

        while True:
            try:
                v = remaining_vertices.pop()
                remaining_vertices.add(v)
            except Exception as err:
                break
            edgecount, w, remaining_vertices = self._find_one_wcc(
                v, remaining_vertices)
            if len(w) > len(wcc):
                wcc = w
                curr_edgecount = edgecount

        return (curr_edgecount, wcc)
