import sys
import random
import timeit

from matplotlib import pyplot as plt

import module2
import alg_upa_trial
import alg_application2_provided


def make_complete_graph(num_nodes):
    """Make undirected graph where each node is connected to all other nodes"""
    def all_but(num_n, num_i):
        """Make a list of all numbers upto n excluding ith"""
        return [num_x for num_x in xrange(num_n) if num_x != num_i]

    return {num_i: set(all_but(num_nodes, num_i))
            for num_i in xrange(num_nodes)}


def algorithm_er(n, p):
    graph = {key: set() for key in xrange(n)}
    for i in xrange(n):
        for j in xrange(n):
            if i == j:
                continue
            if random.random() < p:
                graph[i].add(j)
                graph[j].add(i)

    return graph


def algorithm_upa(n, m):
    graph = make_complete_graph(m)
    upa = alg_upa_trial.UPATrial(m)
    for i in xrange(m, n):
        neighbors = upa.run_trial(m)
        graph[i] = neighbors
        for neighbor in neighbors:
            graph[neighbor].add(i)
    return graph


def num_of_edges(ugraph):
    """Compute how many edges the graph contains"""
    return sum([len(v) for k, v in ugraph.iteritems()]) / 2


def avg(xs):
    return sum(xs) / len(xs)


def random_order(ugraph):
    nodes = ugraph.keys()
    random.shuffle(nodes)
    return nodes


def fast_targeted_order(ugraph):
    ugraph = alg_application2_provided.copy_graph(ugraph)
    N = len(ugraph)
    degree_sets = [set()] * N
    for node, neighbors in ugraph.iteritems():
        degree = len(neighbors)
        degree_sets[degree].add(node)
    order = []

    for k in range(N - 1, -1, -1):
        while degree_sets[k]:
            u = degree_sets[k].pop()
            for neighbor in ugraph[u]:
                d = len(ugraph[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d - 1].add(neighbor)

            order.append(u)
            module2.remove_node(ugraph, u)

    return order


def question1(network, er, upa, order_func, order_label, filename):
    N = len(network)
    order = order_func(network)
    network_res = module2.compute_resilience(network, order)
    er_res = module2.compute_resilience(er, order)
    upa_res = module2.compute_resilience(upa, order)

    xs = range(N + 1)
    plt.plot(xs, network_res, '-r', label='Network graph')
    plt.plot(xs, er_res, '-b', label='ER-generated (p = 0.00171)')
    plt.plot(xs, upa_res, '-g', label='UPA-generated (m = 2)')
    plt.title('Graph resilience (%s)' % order_label)
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Size of the largest connected component')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(filename)
    print('Saved plot to %s' % filename)
    # plt.show()


def measure_targeted_order(n, m, func):
    graph = algorithm_upa(n, m)
    return timeit.timeit(lambda: func(graph), number=1)


def question3(filename):
    xs = range(10, 1000, 10)
    m = 5
    ys_tagreted = [measure_targeted_order(n, m, alg_application2_provided.targeted_order) for n in xs]
    ys_fast_targeted = [measure_targeted_order(n, m, fast_targeted_order) for n in xs]

    plt.plot(xs, ys_tagreted, '-r', label='targeted_order')
    plt.plot(xs, ys_fast_targeted, '-b', label='fast_targeted_order')
    plt.title('Targeted order functions performance (desktop Python)')
    plt.xlabel('Number of nodes in the graph')
    plt.ylabel('Execution time')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(filename)
    print('Saved plot to %s' % filename)
    # plt.show()


def main():
    if len(sys.argv) < 2:
        print('Usage: application2.py <graph.txt>')
        return

    network_graph = alg_application2_provided.load_graph(sys.argv[1])
    print('network_grap has %d edges', num_of_edges(network_graph))

    N = len(network_graph)
    p = 0.00171
    # trials = 10
    # print('avg # of edges %d' % avg([num_of_edges(algorithm_er(N, p)) for _ in range(trials)]))
    er_graph = algorithm_er(N, p)
    print('# of edges in er_graph %d' % num_of_edges(er_graph))

    m = 2
    upa_graph = algorithm_upa(N, m)
    print('# of edges in upa_graph %d' % num_of_edges(upa_graph))

    question1(network_graph, er_graph, upa_graph, random_order,
              'random order attack', 'pic/1-resilience-random.png')

    plt.cla()
    question3('pic/3-performance.png')

    plt.cla()
    question1(network_graph, er_graph, upa_graph, fast_targeted_order,
              'targeted order attack', 'pic/4-resilience-targeted.png')
    plt.show()


if __name__ == '__main__':
    main()
