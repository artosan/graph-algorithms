import pickle
from helpers import prune_graph, percentile

from approximate_computation import ANF0

files = ['data/wiki-Vote.txt',
         'data/soc-Epinions1.txt', 'data/gplus_combined.txt']

for file in files:
    print("Working with graph {}".format(file))
    scc_nodes = pickle.load(open(file + ".scc.p", "rb"))
    wcc_nodes = pickle.load(open(file + ".wcc.p", "rb"))
    with open(file) as f:
        full_set_of_edges = [tuple(map(long, i.split())) for i in f]

    edges_scc = prune_graph(scc_nodes, full_set_of_edges)
    edges_wcc = prune_graph(wcc_nodes, full_set_of_edges)

    edges_wcc_ = list()
    for e in edges_wcc:
        edges_wcc_.append((e[0], e[1]))
        edges_wcc_.append((e[1], e[0]))

    a = ANF0()
    print("SCC")
    r = a.anf0(edges_scc, scc_nodes, 12, 36)
    for i in range(1, 13):
        md = percentile(r[i].values(), 0.5)
        print("Distance {} min {} max {} median {}".format(
            i, min(r[i].values()), max(r[i].values()), md))

    print("WCC")
    r = a.anf0(edges_wcc, wcc_nodes, 12, 36)
    for i in range(1, 13):
        md = percentile(r[i].values(), 0.5)
        print("Distance {} min {} max {} median {}".format(
            i, min(r[i].values()), max(r[i].values()), md))
