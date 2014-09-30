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
    return closest


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm

    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """

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
        if len(horiz_order) <= 3:
            result = list(slow_closest_pairs(cluster_list, horiz_order))[0]
            dist, idx_a, idx_b = result
            idx_a, idx_b = horiz_order[idx_a], horiz_order[idx_b]

            return dist, min(idx_a, idx_b), max(idx_a, idx_b)

        # divide
        idx_m = int(ceil(len(horiz_order) / 2.0))
        mid = (cluster_list[horiz_order[idx_m - 1]].horiz_center() +
               cluster_list[horiz_order[idx_m]].horiz_center()) / 2
        horiz_left = horiz_order[:idx_m]
        horiz_right = horiz_order[idx_m:]

        left_set, right_set = set(horiz_left), set(horiz_right)

        left = fast_helper(
            cluster_list, horiz_left,
            [idx_i for idx_i in vert_order if idx_i in left_set])
        right = fast_helper(
            cluster_list, horiz_right,
            [idx_i for idx_i in vert_order if idx_i in right_set])
        dist, idx_i, idx_j = min([left, right], key=lambda x: x[0])
        closest = dist, idx_i, idx_j

        # conquer
        set_s = [v_item for v_item in vert_order
                 if abs(cluster_list[v_item].horiz_center() - mid) < dist]
        num_k = len(set_s)
        for idx_u in range(num_k - 1):
            for idx_v in range(idx_u + 1, min(idx_u + 4, num_k)):
                cur_dist = cluster_list[set_s[idx_u]].distance(cluster_list[set_s[idx_v]])
                current = cur_dist, set_s[idx_u], set_s[idx_v]
                closest = min([closest, current], key=lambda x: x[0])

        return closest

    # compute list of indices for the clusters ordered in the horizontal direction
    temp = sorted([(cluster_list[idx].horiz_center(), idx)
                  for idx in range(len(cluster_list))])
    horiz_order = [temp[idx][1] for idx in range(len(temp))]

    # compute list of indices for the clusters ordered in vertical direction
    temp = sorted([(cluster_list[idx].vert_center(), idx)
                  for idx in range(len(cluster_list))])
    vert_order = [temp[idx][1] for idx in range(len(temp))]

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
        _, idx_i, idx_j = fast_closest_pair(clusters)
        clusters[idx_i].merge_clusters(clusters[idx_j])
        del clusters[idx_j]
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
