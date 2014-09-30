"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

from math import ceil
from alg_cluster import Cluster


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2

    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pairs(cluster_list, order=None):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm

    Returns the set of all tuples of the form (dist, idx1, idx2)
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.

    """
    if order is None:
        order = range(len(cluster_list))

    min_dist, idx_i, idx_j = float('+inf'), -1, -1
    closest = set()
    for idx_i in range(len(order)):
        for idx_j in range(len(order)):
            if order[idx_i] == order[idx_j]:
                continue
            # dist = dist_matrix[idx_i][idx_j]
            dist = cluster_list[order[idx_i]].distance(cluster_list[order[idx_j]])
            if dist < min_dist:
                min_dist = dist
                closest = set([(dist,
                                min(idx_i, idx_j),
                                max(idx_i, idx_j))])
            elif dist == min_dist:
                closest.add((dist,
                             min(idx_i, idx_j),
                             max(idx_i, idx_j)))
    # print('slow closest %s for %s' % (closest, cluster_list))

    # if 27 in order:
    #     print('27 in order! printing cluster_list', order)
    #     for x in order:
    #         print(x, cluster_list[x])
    #     print('slow_closest_pairs, closest', closest)

    return closest


# def specific_slow_closest_pairs(cluster_list):
#     """Version for cluster_list of max length 3"""
#     idx_N = len(cluster_list)
#     if idx_N <= 1:
#         raise ValueError('Invalid cluster_list size: %d' % idx_N)
#     elif idx_N == 2:
#         return cluster_list[0].distance(cluster_list[1]), 0, 1
#     elif idx_N == 3:
#         items = [(cluster_list[0].distance(cluster_list[1]), 0, 1),
#                  (cluster_list[0].distance(cluster_list[2]), 0, 2),
#                  (cluster_list[1].distance(cluster_list[2]), 1, 2),]
#         return sorted(items, key=lambda x: x[0])[0]
#     else:
#         raise ValueError('Invalid cluster_list size: %d' % idx_N)


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm

    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """

    # return list(slow_closest_pairs(cluster_list))[0]

    # idx_N = len(cluster_list)
    # dist_matrix = []
    # for idx_i in range(idx_N):
    #     dist_matrix.append(
    #         [cluster_list[idx_i].distance(cluster_list[idx_j])
    #          for idx_j in range(idx_N)])

    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))

        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically

        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters

        """
        # base case
        n_items = len(horiz_order)
        if n_items <= 3:
            # temp_list = [cluster_list[val] for val in horiz_order]
            # return specific_slow_closest_pairs(temp_list)
            #return list(slow_closest_pairs(dist_matrix, cluster_list))[0]
            # r = list(slow_closest_pairs(temp_list, horiz_order))[0]
            result = list(slow_closest_pairs(cluster_list, horiz_order))[0]
            # print('returning slow', r)
            dist, idx_a, idx_b = result
            idx_a, idx_b = horiz_order[idx_a], horiz_order[idx_b]

            return dist, min(idx_a, idx_b), max(idx_a, idx_b)
            #return dist, \
            #    cluster_list.index(temp_list[idx_a]), \
            #    cluster_list.index(temp_list[idx_b])
            #idx_a, idx_b = horiz_order[idx_a], horiz_order[idx_b]
            #r = dist, idx_a, idx_b
            # print('fixed returning slow', r)
            #return r
            # return list(slow_closest_pairs(cluster_list))[0]

        # divide
        idx_m = int(ceil(n_items / 2.0))
        mid = (cluster_list[horiz_order[idx_m - 1]].horiz_center() +
               cluster_list[horiz_order[idx_m]].horiz_center()) / 2
        horiz_left = horiz_order[:idx_m]
        horiz_right = horiz_order[idx_m:]

        left_set = set(horiz_left)
        right_set = set(horiz_right)
        vert_left = [idx_i for idx_i in vert_order if idx_i in left_set]
        vert_right = [idx_i for idx_i in vert_order if idx_i in right_set]

        left = fast_helper(cluster_list, horiz_left, vert_left)
        right = fast_helper(cluster_list, horiz_right, vert_right)
        dist, idx_i, idx_j = min([left, right], key=lambda x: x[0])
        closest = dist, idx_i, idx_j
        # print('left %s, right %s, closest %s' % (left, right, closest))

        # conquer
        set_s = [v_item for v_item in vert_order
                 if abs(cluster_list[v_item].horiz_center() - mid) < dist]
        num_k = len(set_s)
        for idx_u in range(num_k - 1):
            for idx_v in range(idx_u + 1, min(idx_u + 4, num_k)):
                cur_dist = cluster_list[set_s[idx_u]].distance(cluster_list[set_s[idx_v]])
                # cur_dist = dist_matrix[set_s[idx_u]][set_s[idx_v]]
                current = cur_dist, set_s[idx_u], set_s[idx_v]
                closest = min([closest, current], key=lambda x: x[0])

        # print('returning fast', closest)
        return closest

    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx)
                        for idx in range(len(cluster_list))]
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]

    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx)
                        for idx in range(len(cluster_list))]
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order)
    return (answer[0], min(answer[1:]), max(answer[1:]))


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list

    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    clusters = [item.copy() for item in cluster_list]
    while len(clusters) > num_clusters:
        # print('--- new iteration, current size and clusters', len(clusters))
        # for x in clusters:
            # print(x)
        _, idx_i, idx_j = fast_closest_pair(clusters)
        # print('merging', idx_i, idx_j)
        clusters[idx_i].merge_clusters(clusters[idx_j])
        del clusters[idx_j]
        # print('---')
    return clusters


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters

    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """

    def nearest_to(point, clusters):
        """Find index of the nearest cluster to the point"""
        nearest, dist = 0, point.distance(clusters[0])
        for idx_i, cluster in enumerate(clusters):
            if point.distance(cluster) < dist:
                dist = point.distance(cluster)
                nearest = idx_i
        return nearest

    # initialize k-means clusters to be initial clusters with largest populations
    num_n = len(cluster_list)
    centers = sorted([idx_x.copy() for idx_x in cluster_list],
                     key=lambda arg_x: arg_x.total_population(),
                     reverse=True)[:num_clusters]

    for _ in range(num_iterations):
        set_k = [Cluster(set(), 0, 0, 0, 0) for _ in range(num_clusters)]

        for idx_j in range(num_n):
            nearest = nearest_to(cluster_list[idx_j], centers)
            set_k[nearest].merge_clusters(cluster_list[idx_j])

        for idx_j, cluster in enumerate(set_k):
            centers[idx_j] = cluster.copy()

    return centers
