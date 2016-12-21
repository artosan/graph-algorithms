import math


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def percentile(N, percent, key=lambda x: x):
    """

    '''
    This function is taken from:
    https://code.activestate.com/recipes/511478-finding-the-percentile-of-the-values/
    '''

    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the values
    """
    if not N:
        return None
    k = (len(N) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c - k)
    d1 = key(N[int(c)]) * (k - f)
    return d0 + d1


def prune_graph(nodes, edges):
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
