from random import random
from timeit import timeit
from matplotlib import pyplot as plt
from alg_cluster import Cluster
from alg_project3_solution import slow_closest_pairs
from alg_project3_solution import fast_closest_pair
from alg_project3_solution import hierarchical_clustering
from alg_project3_solution import kmeans_clustering
from alg_project3_viz import visualize
from alg_project3_viz import load_data_table


def get_random_clusters(num_clusters):
    def make(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return Cluster(set(['0']), x, y, 1, 1)

    return map(make, range(num_clusters))


def question1(filename):
    xs = range(2, 201)
    ys_fast, ys_slow = [], []
    for n in xs:
        clusters = get_random_clusters(n)
        ys_fast.append(timeit(lambda: fast_closest_pair(clusters), number=1))
        ys_slow.append(timeit(lambda: slow_closest_pairs(clusters), number=1))

    plt.plot(xs, ys_fast, '-r', label='fast_closest_pair')
    plt.plot(xs, ys_slow, '-b', label='slow_closest_pairs')
    plt.title('Running time of *closest_pair functions (desktop Python)')
    plt.xlabel('Number of initial clusters')
    plt.ylabel('Running time, seconds')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(filename)
    print('Saved plot to %s' % filename)


def question2(filename):
    visualize('data/unifiedCancerData_3108.csv', filename,
              lambda x: hierarchical_clustering(x, 15))


def question3(filename):
    visualize('data/unifiedCancerData_3108.csv', filename,
              lambda x: kmeans_clustering(x, 15, 5))


def distortion(clusters, table):
    return sum([x.cluster_error(table) for x in clusters])


def question5(filename):
    data = 'data/unifiedCancerData_111.csv'
    dist = distortion(visualize(data, filename,
                                lambda x: hierarchical_clustering(x, 9)),
                      load_data_table(data))
    print('Distortion in question5, hierarchical_clustering = %f (%s)' % (dist, dist))


def question6(filename):
    data = 'data/unifiedCancerData_111.csv'
    dist = distortion(visualize(data, filename,
                                lambda x: kmeans_clustering(x, 9, 5)),
                      load_data_table(data))
    print('Distortion in question6, kmeans = %f (%s)' % (dist, dist))


def question10(data, filename):
    table = load_data_table(data)
    clusters = Cluster.load_as_list(data)
    xs = range(6, 21)
    ys_hier = []

    def dist(clusters):
        ys_hier.append(distortion(clusters, table))

    hierarchical_clustering(clusters, 6, dist, set(xs))
    ys_hier.reverse()
    ys_kmeans = [distortion(kmeans_clustering(clusters, x, 5), table) for x in xs]

    plt.cla()
    plt.plot(xs, ys_hier, '-r', label='Hierarchical clustering distortion')
    plt.plot(xs, ys_kmeans, '-b', label='K-means clustering distortion')
    plt.title('Clustering distortion (%s)' % data)
    plt.xlabel('Number of output clusters')
    plt.ylabel('Distortion')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(filename)
    print('Saved plot to %s' % filename)


def main():
    # question1('pic/question1.png')
    #question2('pic/question2.png')
    #question3('pic/question3.png')
    #question5('pic/question5.png')
    #question6('pic/question6.png')
    question10('./data/unifiedCancerData_111.csv', 'pic/question10-111.png')
    question10('./data/unifiedCancerData_290.csv', 'pic/question10-290.png')
    question10('./data/unifiedCancerData_896.csv', 'pic/question10-896.png')


if __name__ == '__main__':
    main()
