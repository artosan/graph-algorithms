import itertools


class ConnectedComponents(object):

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

    def _find_scc(self):
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

    def _find_wcc(self, start, path=[]):
        """
        Iterative function which performs depth first search
        """
        graph = self.edges
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

    def find_largest_scc(self):
        return self._find_scc()


    def find_largest_wcc(self):
        """
        Finds largest strongly connected component of the graph.
        """
        checked_vertices = set()
        largest_wcc = list()
        for vertex in self.vertices:
            # if vertex is not already in one of the scc's go for it!
            if vertex not in checked_vertices:
                wcc = self._find_wcc(vertex)
                if len(wcc) > len(largest_wcc):
                    largest_wcc = wcc
                for v in wcc:
                    checked_vertices.add(v)
            else:
                next
        return largest_wcc
