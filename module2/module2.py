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
    connected_components = set()
    remaining_nodes = set(ugraph.keys())

    while remaining_nodes:
        node = remaining_nodes.pop()
        visited = bfs_visited(ugraph, node)
        connected_components.add(visited)
        remaining_nodes -= visited

    return connected_components


def largest_cc_size(ugraph):
    '''Return size of the largest connected component of the given
    undirected graph.'''
    return max(map(len, cc_visited(ugraph)))
