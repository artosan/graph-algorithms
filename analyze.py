from connected_components import ConnectedComponents
import pickle
import time
import tarjan


if __name__ == "__main__":

    filenames = ['data/wiki-Vote.txt']

    for file in filenames:
        print("---------------------------------------------------------------------------------------------------")
        print("Starting to work with graph {}".format(file))
        start = time.time()
        with open(file) as f:
            edges = [tuple(map(long, i.split())) for i in f]

        wcc = ConnectedComponents(edges, False)
        largest_wcc = wcc.find_largest_wcc()
        pickle.dump(largest_wcc, open(file + ".wcc.p", "wb"))
        wcc_size = len(list(set(largest_wcc)))
        print("Got wcc {}".format(wcc_size))
        print(largest_wcc[555])

        scc = ConnectedComponents(edges, True)
        candidates = list(scc.find_largest_scc())
        candidates.sort(key=len, reverse=True)
        largest_scc = candidates[0]
        pickle.dump(largest_scc, open(file + ".scc.p", "wb"))
        scc_size = len(largest_scc)

        print("Size of the largest weakly connected component of {} is: {}".format(file, wcc_size))
        print("Size of the lergest strongly connected component of {} is: {}".format(file, scc_size))

        end = time.time()
        timedelta = end - start
        print("Processing file {} took {} seconds".format(file,  timedelta))
        print("---------------------------------------------------------------------------------------------------")
