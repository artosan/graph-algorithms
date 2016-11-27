from connected_components import ConnectedComponents
import pickle
import time


if __name__ == "__main__":

    filenames = ['data/wiki-Vote.txt']
    print("Starting graph analysis...")
    start_time = time.time()
    for file in filenames:
        print("---------------------------------------------------------------------------------------------------")
        print("Starting to work with graph {}".format(file))
        start = time.time()
        with open(file) as f:
            edges = [tuple(map(long, i.split())) for i in f]

        wcc = ConnectedComponents(edges, False)
        largest_wcc = wcc.find_largest_wcc()
        pickle.dump(largest_wcc, open(file + ".wcc.p", "wb"))
        wcc_size = len(list(largest_wcc))

        scc = ConnectedComponents(edges, True)
        largest_scc = scc.find_largest_scc()
        pickle.dump(largest_scc, open(file + ".scc.p", "wb"))
        scc_size = len(largest_scc)

        print("Node count of the largest weakly connected component in graph {} is: {}".format(file, wcc_size))
        print("Node count of the lergest strongly connected component in graph {} is: {}".format(file, scc_size))

        end = time.time()
        timedelta = end - start
        print("Processing file {} took {} seconds".format(file,  timedelta))
        print("---------------------------------------------------------------------------------------------------")

    end_time = time.time()
    total_time_delta = end_time - start_time
    print("Processing graphs took in total {}".format(total_time_delta))
