from connected_components import ConnectedComponents
import pickle
import time


if __name__ == "__main__":

    filenames = ['data/gplus_combined.txt']
    print("Starting graph analysis...")
    start_time = time.time()
    for file in filenames:
        print("---------------------------------------------------------------------------------------------------")
        print("Starting to work with graph {}".format(file))
        start = time.time()
        with open(file) as f:
            edges = [tuple(map(long, i.split())) for i in f]

        wcc = ConnectedComponents(edges, False)
        wcc_edges, largest_wcc = wcc.find_largest_wcc()
        pickle.dump(largest_wcc, open(file + ".wcc.p", "wb"))
        wcc_size = len(list(largest_wcc))

        scc = ConnectedComponents(edges, True)
        scc_edges, largest_scc = scc.find_largest_scc()
        pickle.dump(largest_scc, open(file + ".scc.p", "wb"))
        scc_size = len(largest_scc)

        print(
            "Statistics of the largest weakly connected component in graph {}".format(file))
        print("Node count: {}".format(wcc_size))
        print("Edge count: {}".format(wcc_edges))

        print("----------")
        print("Statistics of the largest strongly connected component in graph {}".format(file))
        print("Node count: {}".format(scc_size))
        print("Edge count: {}".format(scc_edges))

        end = time.time()
        timedelta = end - start
        print("Processing file {} took {} seconds".format(file,  timedelta))
        print("---------------------------------------------------------------------------------------------------")

    end_time = time.time()
    total_time_delta = end_time - start_time
    print("Processing graphs took in total {}".format(total_time_delta))
