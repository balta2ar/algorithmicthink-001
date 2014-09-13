''' Module 2. Topics include:
    - Breadth-First search
    - Connected components
    - Graph resilience
'''
from collections import deque


def bfs_visited(ugraph, start_node):
    '''Run Breadth-First search from start_node on the undirected graph.
    Return a set of nodes that were visited.'''
    visited = set()
    queue = deque()

    visited.add(start_node)
    queue.append(start_node)

    while queue:
        node = queue.popleft()
        for neighbor in ugraph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited


def cc_visited(ugraph):
    '''Return a set of sets. Child sets are connected components
    of the undirected graph.'''
    connected_components = []
    remaining_nodes = set(ugraph.keys())

    while remaining_nodes:
        node = remaining_nodes.pop()
        visited = bfs_visited(ugraph, node)
        connected_components.append(visited)
        remaining_nodes -= visited

    return connected_components


def largest_cc_size(ugraph):
    '''Return size of the largest connected component of the given
    undirected graph.'''
    if not len(ugraph):
        return 0
    return max(map(len, cc_visited(ugraph)))


def remove_node(ugraph, node):
    '''Remove node from the graph. This also includes removal of the node
    from its neighbors.'''
    print('removing', node, 'from', ugraph)
    for neighbor in ugraph[node]:
        ugraph[neighbor].remove(node)
    del ugraph[node]


def compute_resilience(ugraph, attack_order):
    '''Compute graph resilience (size of the largest connected component)
    after removing each of provided nodes.'''
    resilience = [largest_cc_size(ugraph)]
    for node in attack_order:
        remove_node(ugraph, node)
        resilience.append(largest_cc_size(ugraph))
    return resilience


def test_run():
    '''Testing routines.'''
    graph = {
        0: set([1, 3, 4, 5]),
        1: set([0, 2, 4, 6]),
        2: set([1, 3, 5]),
        3: set([0, 2]),
        4: set([0, 1]),
        5: set([0, 2]),
        6: set([1])
    }

    print('graph')
    print(graph)

    print('cc_visited')
    print(cc_visited(graph))

    print('largest_cc_size')
    print(largest_cc_size(graph))

    print('compute_resilience')
    print(compute_resilience(graph, range(7)))
