import random

import module2
import alg_upa_trial


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
    upa = alg_upa_trial.DPATrial(m)
    for i in xrange(m, n):
        graph[i] = upa.run_trial(m)
    return graph


if __name__ == '__main__':
    pass
