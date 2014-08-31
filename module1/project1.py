"""Compute indegree of a graph and degree distibution."""
EX_GRAPH0 = {
    0: set([1, 2]),
    1: set(),
    2: set()
}

EX_GRAPH1 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3]),
    3: set([0]),
    4: set([1]),
    5: set([2]),
    6: set()
}

EX_GRAPH2 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3, 7]),
    3: set([7]),
    4: set([1]),
    5: set([2]),
    6: set(),
    7: set([3]),
    8: set([1, 2]),
    9: set([0, 3, 4, 5, 6, 7])
}


def make_complete_graph(num_nodes):
    """Make graph where each node is connected to all other nodes"""
    def all_but(num_n, num_i):
        """Make a list of all numbers upto n excluding ith"""
        return [num_x for num_x in xrange(num_n) if num_x != num_i]

    return {num_i: set(all_but(num_nodes, num_i))
            for num_i in xrange(num_nodes)}


def compute_in_degrees(digraph):
    """Compute how many nodes enter current node"""
    degrees = {key: 0 for key in digraph.iterkeys()}
    for _, adjacent in digraph.iteritems():
        for adj in adjacent:
            degrees[adj] += 1
    return degrees


def in_degree_distribution(digraph):
    """How many different indegrees we have in the graph"""
    num_n = len(digraph.keys())
    num_nlarge = num_n * (num_n - 1) / 2
    distr = {key: 0 for key in xrange(num_nlarge)}
    in_degrees = compute_in_degrees(digraph)
    for _, indegree in in_degrees.iteritems():
        distr[indegree] += 1
    return {key: value for key, value in distr.iteritems() if value > 0}
