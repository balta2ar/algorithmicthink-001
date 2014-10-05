from random import random
from timeit import timeit
from matplotlib import pyplot as plt
from alg_cluster import Cluster
from alg_project3_solution import slow_closest_pairs
from alg_project3_solution import fast_closest_pair


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
    plt.title('Targeted order functions performance (desktop Python)')
    plt.xlabel('Number of nodes in the graph')
    plt.ylabel('Execution time')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(filename)
    print('Saved plot to %s' % filename)


def main():
    question1('pic/question1.png')


if __name__ == '__main__':
    main()
