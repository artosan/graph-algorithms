from exact_computation import calculate_statistics, calculate_all_paths
from approximate_computation import RandomPairs, RandomBFS
from connected_components import ConnectedComponents
import pickle
import time


def generate_connected_components():
    filenames = ['data/wiki-Vote.txt', 'data/soc-Epinions1.txt', 'data/gplus_combined.txt',
                 'data/soc-pokec-relationships.txt', 'data/soc-Livejournal1.txt']
    print("Starting graph analysis...")
    start_time = time.time()
    for file in filenames:
        print("-" * 99)
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

        print("-" * 99)
        print("Statistics of the largest strongly connected component in graph {}".format(file))
        print("Node count: {}".format(scc_size))
        print("Edge count: {}".format(scc_edges))

        end = time.time()
        timedelta = end - start
        print("Processing file {} took {} seconds".format(file,  timedelta))
        print("-" * 99)

    end_time = time.time()
    total_time_delta = end_time - start_time
    print("Processing graphs took in total {}".format(total_time_delta))


def exact_stats(filename):
    print("-" * 99)
    print("EXACT STATISTICS")
    print("-" * 99)
    print("graph: {}".format(filename))

    # Exact stats for wcc
    wcc_distances = pickle.load(open(filename + ".wcc.statistics.p", "rb"))
    d_median, d_mean, d_diameter, d_effective_diameter = calculate_statistics(
        wcc_distances)
    print("EXACT STATS FOR WCC: Median {}\nMean {}\nDiameter {}\nEffective Diameter {}"
          .format(d_median, d_mean, d_diameter, d_effective_diameter))

    # Exact stats for scc
    scc_distances = pickle.load(
        open(filename + ".scc.statistics.p", "rb"))
    d_median, d_mean, d_diameter, d_effective_diameter = calculate_statistics(
        scc_distances)
    print("EXACT STATS FOR SCC: Median {}\nMean {}\nDiameter {}\nEffective Diameter {}"
          .format(d_median, d_mean, d_diameter, d_effective_diameter))


def run_stats(filenames):

    # exact stats only for wiki-Vote.txt
    exact_stats("data/wiki-Vote.txt")

    # Loop to approximate the stats of the graphs
    print("APPROXIMATE STATISTICS")
    for file in filenames:
        print("-" * 99)
        print("-" * 99)
        print("Statistics for graph: {}".format(file))
        print("-" * 99)
        print("-" * 99)

        wcc_nodes = pickle.load(open(file + ".wcc.p", "rb"))
        scc_nodes = pickle.load(open(file + ".scc.p", "rb"))
        with open(file) as f:
            edges = [tuple(map(long, i.split())) for i in f]

        sampler = RandomPairs(scc_nodes, edges, True)
        random_pairs_stats_scc = list()
        iterations = [1000]
        for iter in iterations:
            print("Approximating by randomly choosing {} pairs.".format(iter))
            random_pairs_stats_scc.append(
                {'iter': iter, 'stats': sampler.approximate(iter)})

        bfs_sampler = RandomBFS(scc_nodes, edges, True)
        iterations = [50]
        random_bfs_stats_scc = list()
        for iter in iterations:
            print("Approximating by randomly starting BFS {} times.".format(iter))
            random_bfs_stats_scc.append(
                {'iter': iter, 'stats': bfs_sampler.approximate(iter)})

        sampler = RandomPairs(wcc_nodes, edges, False)
        random_pairs_stats_wcc = list()
        iterations = [1000]
        for iter in iterations:
            print("Approximating by randomly choosing {} pairs.".format(iter))
            random_pairs_stats_wcc.append(
                {'iter': iter, 'stats': sampler.approximate(iter)})

        bfs_sampler = RandomBFS(wcc_nodes, edges, False)
        iterations = [50]
        random_bfs_stats_wcc = list()
        for iter in iterations:
            print("Approximating by randomly starting BFS {} times.".format(iter))
            random_bfs_stats_wcc.append(
                {'iter': iter, 'stats': bfs_sampler.approximate(iter)})

        print("-" * 99)
        print("-" * 99)
        print("RANDOM PAIR STATS")

        for stat in random_pairs_stats_scc:
            d_median, d_mean, d_diameter, d_effective_diameter = stat['stats']
            iterations = stat['iter']
            print("-" * 99)
            print("ITERATIONS {}".format(iterations))
            print("SCC STATS:\nMedian {}\nMean {}\nDiameter {}\nEffective Diameter {}".format(
                d_median, d_mean, d_diameter, d_effective_diameter))
            print("-" * 99)

        for stat in random_pairs_stats_wcc:
            d_median, d_mean, d_diameter, d_effective_diameter = stat['stats']
            iterations = stat['iter']
            print("-" * 99)
            print("ITERATIONS {}".format(iterations))
            print("WCC STATS:\nMedian {}\nMean {}\nDiameter {}\nEffective Diameter {}".format(
                d_median, d_mean, d_diameter, d_effective_diameter))
            print("-" * 99)

        print("BFS STATS")
        for stat in random_bfs_stats_scc:
            d_median, d_mean, d_diameter, d_effective_diameter = stat['stats']
            iterations = stat['iter']
            print("-" * 99)
            print("ITERATIONS {}".format(iterations))
            print("SCC STATS:\nMedian {}\nMean {}\nDiameter {}\nEffective Diameter {}".format(
                d_median, d_mean, d_diameter, d_effective_diameter))
            print("-" * 99)

        for stat in random_bfs_stats_wcc:
            d_median, d_mean, d_diameter, d_effective_diameter = stat['stats']
            iterations = stat['iter']
            print("-" * 99)
            print("ITERATIONS {}".format(iterations))
            print("WCC STATS:\nMedian {}\nMean {}\nDiameter {}\nEffective Diameter {}".format(
                d_median, d_mean, d_diameter, d_effective_diameter))
            print("-" * 99)


if __name__ == "__main__":
    """
    Run the graph analysis!
    """

    # generate wcc and scc for every graph, prepare for a long wait if you run
    # this
    generate_connected_components()

    """

    """
    calculate_all_paths()

    """
    Run exact and approximated statistics for the given graph
    """
    files = ['data/wiki-Vote.txt',
             'data/soc-Epinions1.txt', 'data/gplus_combined.txt']
    run_stats(files)
