import sys
import alg_project3_solution as sol

path = 'data/unifiedCancerData_111.csv'
if len(sys.argv) > 1:
    path = sys.argv[1]

s = sol.Cluster.load_as_list(path)


def hier():
    sol.hierarchical_clustering(s, 9)


def kmeans():
    sol.kmeans_clustering(s, 9, 10)


from timeit import timeit
print('data %s' % path)
print('hier %s' % timeit('hier()', setup='from __main__ import hier', number=1))
print('kmeans %s' % timeit('kmeans()', setup='from __main__ import kmeans', number=1))
