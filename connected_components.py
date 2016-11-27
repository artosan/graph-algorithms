import itertools
import copy


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

    def _find_scc(self):
        identified = set()
        stack = []
        index = {}
        boundaries = []
        result = list()

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

        return list(result)

    def _find_wcc(self, start):
        """
        Iterative function which performs depth first search
        """
        path = []
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

    def _find_one_wcc(self, v, vertices):
        wcc = self._find_wcc(v)
        remaining_vertices = copy.deepcopy(vertices)
        remaining_vertices = remaining_vertices - set(wcc)
        return (wcc, remaining_vertices)


    def find_largest_scc(self):
        return self._find_scc()


    def find_largest_wcc(self):
        """
        Finds largest strongly connected component of the graph.
        """
        v = self.vertices.pop()
        self.vertices.add(v)
        wcc, remaining_vertices = self._find_one_wcc(v, self.vertices)

        while True:
            try:
                v = remaining_vertices.pop()
                remaining_vertices.add(v)
            except Exception as err:
                break
            w, remaining_vertices = self._find_one_wcc(v, remaining_vertices)
            if len(w) > len(wcc):
                wcc = w

        return wcc
